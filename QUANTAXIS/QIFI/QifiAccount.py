import datetime
import traceback
import uuid

import bson
import numpy as np
import pandas as pd
import pymongo
from qaenv import mongo_ip
from QUANTAXIS.QAMarket.market_preset import MARKET_PRESET
from QUANTAXIS.QAMarket.QAOrder import ORDER_DIRECTION
from QUANTAXIS.QAMarket.QAPosition import QA_Position


def parse_orderdirection(od):
    direction = ''
    offset = ''

    if od in [1, 2, 3, 4]:
        direction = 'BUY'
    elif od in [-1, -2, -3, -4]:
        direction = 'SELL'
    if abs(od) == 2 or od == 1:
        offset = 'OPEN'
    elif abs(od) == 3 or od == -1:
        offset = 'CLOSE'
    elif abs(od) == 4:
        offset = 'CLOSETODAY'

    return direction, offset


class QIFI_Account():

    def __init__(self, username, password, model="SIM", broker_name="QAPaperTrading", trade_host=mongo_ip, init_cash=1000000, taskid=str(uuid.uuid4()), nodatabase=False):
        """Initial
        QIFI Account是一个基于 DIFF/ QIFI/ QAAccount后的一个实盘适用的Account基类


        1. 兼容多持仓组合
        2. 动态计算权益

        使用 model = SIM/ REAL来切换

        qifiaccount 不去区分你的持仓是股票还是期货, 因此你可以实现跨市场的交易持仓管理
        nodatabase 离线模式
        """
        self.user_id = username
        self.username = username
        self.password = password

        self.source_id = "QIFI_Account"  # 识别号
        self.market_preset = MARKET_PRESET()
        # 指的是 Account所属的账户编组(实时的时候的账户观察组)
        self.portfolio = "QAPaperTrade"
        self.model = model

        self.broker_name = broker_name    # 所属期货公司/ 模拟的组
        self.investor_name = ""  # 账户所属人(实盘的开户人姓名)
        self.bank_password = ""
        self.capital_password = ""
        self.wsuri = ""

        self.bank_id = "QASIM"
        self.bankname = "QASIMBank"

        self.trade_host = trade_host
        if model == 'BACKTEST':
            self.db = pymongo.MongoClient(trade_host).quantaxis
        else:
            self.db = pymongo.MongoClient(trade_host).QAREALTIME

        self.pub_host = ""
        self.trade_host = ""
        self.last_updatetime = ""
        self.status = 200
        self._trading_day = ""
        self.init_cash = init_cash
        self.pre_balance = 0
        self.datetime = ""
        self.static_balance = 0

        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.close_profit = 0
        self.premium = 0  # 本交易日内交纳的期权权利金
        self.event_id = 0
        self.taskid = taskid
        self.money = 0
        # QIFI 协议
        self.transfers = {}
        self.schedule = {}

        self.banks = {}

        self.frozen = {}

        self.event = {}
        self.positions = {}
        self.trades = {}
        self.orders = {}
        self.market_preset = MARKET_PRESET()
        self.nodatabase = nodatabase

    def initial(self):

        self.reload()

        if self.pre_balance == 0 and self.balance == 0 and self.model != "REAL":
            self.log('Create new Account')
            self.create_simaccount()

        self.sync()

    @property
    def trading_day(self):
        if self.model == "BACKTEST":
            return str(self.datetime)[0:10]
        else:
            return self._trading_day

    def reload(self):
        if self.model.upper() in ['REAL', 'SIM']:
            message = self.db.account.find_one(
                {'account_cookie': self.user_id, 'password': self.password})

            time = datetime.datetime.now()
            # resume/settle

            if time.hour <= 15:
                self._trading_day = time.date()
            else:
                if time.weekday() in [0, 1, 2, 3]:
                    self._trading_day = time.date() + datetime.timedelta(days=1)
                elif time.weekday() in [4, 5, 6]:
                    self._trading_day = time.date() + datetime.timedelta(days=(7-time.weekday()))
            if message is not None:
                accpart = message.get('accounts')

                self.money = message.get('money')
                self.source_id = message.get('sourceid')

                self.pre_balance = accpart.get('pre_balance')
                self.deposit = accpart.get('deposit')
                self.withdraw = accpart.get('withdraw')
                self.withdrawQuota = accpart.get('WithdrawQuota')
                self.close_profit = accpart.get('close_profit')
                self.static_balance = accpart.get('static_balance')
                self.event = message.get('event')
                self.trades = message.get('trades')
                self.transfers = message.get('transfers')
                self.orders = message.get('orders')
                self.taskid = message.get('taskid', str(uuid.uuid4()))

                positions = message.get('positions')
                for position in positions.values():
                    p = QA_Position(
                    ).loadfrommessage(position)

                    self.positions[position.get('exchange_id')+'.'+position.get('instrument_id')] = QA_Position(
                    ).loadfrommessage(position)

                for order in self.open_orders:
                    self.log('try to deal {}'.format(order))
                    self.make_deal(order)

                self.banks = message.get('banks')

                self.status = message.get('status')
                self.wsuri = message.get('wsuri')

                self.on_reload()

                if message.get('trading_day', '') == str(self._trading_day):
                    # reload
                    pass

                else:
                    # settle
                    self.settle()

    def create_fromQIFI(self, message):
        pass

    def order_rule(self):
        """
        订单流控
        """
        pass

    def batch_buy(self, codedf: pd.Series, datetime: str, totalamount: float = 1000000, model: enumerate = 'avg_money'):
        """
        批量调仓接口

        codedf: pd.Series

            Series.index -> code
            Series.value -> price


        totalamount: 总买入金额

        model Enum
            'avg_money': 等市值买入
            'avg_amount': 等股数买入(买入总金额==totalamount)
        """
        if model == 'avg_money':
            moneyper = totalamount / len(codedf)
            amount = (moneyper/codedf).apply(lambda x: (int(100/x)*100)
                                             if int(100/x) > 0 else 100)
        elif model == 'avg_amount':
            amountx = int(totalamount/(100*codedf.sum()))
            if amountx == 0:
                return False
            else:
                amount = codedf.apply(lambda x: amountx*100)
        orderres = pd.concat([codedf, amount], axis=1)
        orderres.columns = ['price', 'amount']
        res = orderres.assign(datetime=datetime).apply(lambda x: self.send_order(
            code=x.index, amount=x.amount, price=x.price, towards=1, datetime=x.datetime))
        return res

    def sync(self):
        self.on_sync()
        try:
            if not self.nodatabase:
                if self.model == "BACKTEST":
                    ## 数据库: quantaxis.history
                    self.db.history.update({'account_cookie': self.user_id, 'trading_day': self.trading_day}, {
                        '$set': self.message}, upsert=True)
                else:
                    ## 数据库: QAREALTIME.account
                    self.db.account.update({'account_cookie': self.user_id, 'password': self.password}, {
                        '$set': self.message}, upsert=True)

                    self.db.hisaccount.insert_one(
                        {'updatetime': self.dtstr, 'account_cookie': self.user_id, 'accounts': self.account_msg})
            else:
                print(
                    'pretend to save to database {}/{}'.format(self.user_id, self.trading_day))
                print(self.message)
                return self.message
        except:
            traceback.print_exc()

    def settle(self):
        self.log('settle')
        self.sync()

        self.pre_balance += (self.deposit - self.withdraw + self.close_profit)
        self.static_balance = self.pre_balance

        self.close_profit = 0
        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.premium = 0
        self.money += self.frozen_margin

        self.orders = {}
        self.frozen = {}
        self.trades = {}
        self.transfers = {}
        self.event = {}
        self.event_id = 0

        for item in self.positions.values():
            item.settle()

        # sell first >> second buy ==> for make sure have enough cash
        buy_order_sche = []
        for order in self.schedule.values():
            if order['towards'] > 0:
                # buy order
                buy_order_sche.append(order)
            else:
                self.send_order(order['code'], order['amount'],
                                order['price'], order['towards'], order['order_id'])
        for order in buy_order_sche:
            self.send_order(order['code'], order['amount'],
                            order['price'], order['towards'], order['order_id'])
        self.schedule = {}

    def on_sync(self):
        pass

    def on_reload(self):
        pass

    @property
    def dtstr(self):
        if self.model == "BACKTEST":
            return self.datetime.replace('.', '_')
        else:
            return str(datetime.datetime.now()).replace('.', '_')

    def ask_deposit(self, money):

        self.deposit += money
        self.money += money
        self.transfers[str(self.event_id)] = {
            "datetime": 433241234123,  # // 转账时间, epoch nano
            "currency": "CNY",  # 币种
            "amount": money,  # 涉及金额
            "error_id": 0,  # 转账结果代码
            "error_msg": "成功",  # 转账结果代码
        }
        self.event[self.dtstr] = "转账成功 {}".format(money)

    def ask_withdraw(self, money):
        if self.withdrawQuota > money:
            self.withdrawQuota -= money
            self.withdraw += money
            self.transfers[str(self.event_id)] = {
                "datetime": 433241234123,  # // 转账时间, epoch nano
                "currency": "CNY",  # 币种
                "amount": -money,  # 涉及金额
                "error_id": 0,  # 转账结果代码
                "error_msg": "成功",  # 转账结果代码
            }
            self.event[self.dtstr] = "转账成功 {}".format(-money)
        else:
            self.event[self.dtstr] = "转账失败: 余额不足 left {}  ask {}".format(
                self.withdrawQuota, money)

    def create_simaccount(self):
        self._trading_day = str(datetime.date.today())
        self.wsuri = "ws://www.yutiansut.com:7988"
        self.pre_balance = 0
        self.static_balance = 0
        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.user_id = self.user_id
        self.password = self.password
        self.money = 0
        self.close_profit = 0
        self.event_id = 0
        self.transfers = {}
        self.banks = {}
        self.event = {}
        self.positions = {}
        self.trades = {}
        self.orders = {}
        self.banks[str(self.bank_id)] = {
            "id": self.bank_id,
            "name": self.bankname,
            "bank_account": "",
            "fetch_amount": 0.0,
            "qry_count": 0
        }
        self.ask_deposit(self.init_cash)

    def create_backtestaccount(self):
        """
        生成一个回测的账户

        回测账户的核心事件轴是数据的datetime, 基于数据的datetime来进行账户的更新


        """
        self._trading_day = ""
        self.pre_balance = self.init_cash
        self.static_balance = self.init_cash
        self.deposit = 0  # 入金
        self.withdraw = 0  # 出金
        self.withdrawQuota = 0  # 可取金额
        self.user_id = self.user_id
        self.password = self.password
        self.money = self.init_cash
        self.close_profit = 0
        self.event_id = 0
        self.transfers = {}
        self.banks = {}
        self.event = {}
        self.positions = {}
        self.trades = {}
        self.orders = {}
        self.banks[str(self.bank_id)] = {
            "id": self.bank_id,
            "name": self.bankname,
            "bank_account": "",
            "fetch_amount": 0.0,
            "qry_count": 0
        }

        # self.ask_deposit(self.init_cash)

    def add_position(self, position):

        if position.instrument_id not in self.positions.keys():
            self.positions[position.exchange_id +
                           '.'+position.instrument_id] = position
            return 0
        else:
            return 1

    def drop_position(self, position):
        pass

    def log(self, message):
        print(message)
        #self.event[self.dtstr] = message

    @property
    def open_orders(self):
        return [item for item in self.orders.values() if item['volume_left'] > 0]

    @property
    def message(self):
        return {
            # // 账户号(兼容QUANTAXIS QAAccount)// 实盘的时候是 账户id
            "account_cookie": self.user_id,
            "password": self.password,
            "databaseip": self.trade_host,
            "model": self.model,
            "ping_gap": 5,
            "portfolio": self.portfolio,
            "broker_name": self.broker_name,  # // 接入商名称
            "capital_password": self.capital_password,  # // 资金密码 (实盘用)
            "bank_password": self.bank_password,  # // 银行密码(实盘用)
            "bankid": self.bank_id,  # // 银行id
            "investor_name": self.investor_name,  # // 开户人名称
            "money": self.money,         # // 当前可用现金
            "pub_host": self.pub_host,
            "trade_host": self.trade_host,
            "taskid": self.taskid,
            "sourceid": self.source_id,
            "updatetime": str(self.last_updatetime),
            "wsuri": self.wsuri,
            "bankname": self.bankname,
            "trading_day": str(self.trading_day),
            "status": self.status,
            "accounts": self.account_msg,
            "trades": self.trades,
            "positions": self.position_msg,
            "orders": self.orders,
            "event": self.event,
            "transfers": self.transfers,
            "banks": self.banks,
            "frozen": self.frozen,
            "settlement": {},
        }

    @property
    def account_msg(self):
        return {
            "user_id": self.user_id,
            "currency": "CNY",
            "pre_balance": self.pre_balance,
            "deposit": self.deposit,
            "withdraw": self.withdraw,
            "WithdrawQuota": self.withdrawQuota,
            "close_profit": self.close_profit,
            "commission": self.commission,
            "premium": self.premium,
            "static_balance": self.static_balance,
            "position_profit": self.position_profit,
            "float_profit": self.float_profit,
            "balance": self.balance,
            "margin": self.margin,
            "frozen_margin": self.frozen_margin,
            "frozen_commission": 0.0,
            "frozen_premium": 0.0,
            "available": self.available,
            "risk_ratio": 1 - self.available/self.balance
        }

    @property
    def position_msg(self):
        return dict(zip(self.positions.keys(), [item.message for item in self.positions.values()]))

    @property
    def position_profit(self):
        return sum([position.position_profit for position in self.positions.values()])

    @property
    def float_profit(self):
        return sum([position.float_profit for position in self.positions.values()])

    @property
    def frozen_margin(self):
        return sum([item.get('money') for item in self.frozen.values()])

    def transform_dt(self, times):
        if isinstance(times, str):

            if len(times)==10:
                times = times+' 00:00:00'
            tradedt = datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S') if len(
                times) == 19 else datetime.datetime.strptime(times.replace('_', '.'), '%Y-%m-%d %H:%M:%S.%f')
            return bson.int64.Int64(tradedt.timestamp()*1000000000)
        elif isinstance(times, datetime.datetime):
            return bson.int64.Int64(times.timestamp()*1000000000)


# 惰性计算


    @property
    def available(self):
        return self.money

    @property
    def margin(self):
        """保证金
        """
        return sum([position.margin for position in self.positions.values()])

    @property
    def commission(self):
        """本交易日内交纳的手续费
        """
        return sum([position.commission for position in self.positions.values()])

    @property
    def balance(self):
        """动态权益

        Arguments:
            self {[type]} -- [description]
        """

        return self.static_balance + self.deposit - self.withdraw + self.float_profit + self.close_profit

    def order_check(self, code: str, amount: int, price: float, towards: int, order_id: str) -> bool:
        """
        order_check是账户自身的逻辑, 你可以重写这个代码

        Attention: 需要注意的是 如果你修改了此部分代码 请注意如果你做了对于账户的资金的预操作请在结束的时候恢复

        :::如: 下单失败-> 请恢复账户的资金和仓位

        --> return  Bool
        """
        res = False
        qapos = self.get_position(code)

        #res = qapos.order_check(amount, price, towards, order_id)
        print('account order_check')
        self.log(qapos.curpos)
        self.log(qapos.close_available)
        if towards == ORDER_DIRECTION.BUY_CLOSE:
            # self.log("buyclose")
            # self.log(self.volume_short - self.volume_short_frozen)
            # self.log(amount)
            if (qapos.volume_short - qapos.volume_short_frozen) >= amount:
                # check
                qapos.volume_short_frozen_today += amount
                #qapos.volume_short_today -= amount
                res = True
            else:
                self.log("BUYCLOSE 仓位不足")

        elif towards == ORDER_DIRECTION.BUY_CLOSETODAY:
            if (qapos.volume_short_today - qapos.volume_short_frozen_today) >= amount:
                qapos.volume_short_frozen_today += amount
                #qapos.volume_short_today -= amount
                res = True
            else:
                self.log("BUYCLOSETODAY 今日仓位不足")
        elif towards in [ORDER_DIRECTION.SELL_CLOSE]:
            # self.log("sellclose")
            # self.log(self.volume_long - self.volume_long_frozen)
            # self.log(amount)
            if (qapos.volume_long - qapos.volume_long_frozen) >= amount:
                qapos.volume_long_frozen_today += amount
                #qapos.volume_long_today -= amount
                res = True
            else:
                self.log("SELL CLOSE 仓位不足")
        elif towards == ORDER_DIRECTION.SELL:

            """
            only for stock
            """
            if (qapos.volume_long_his - qapos.volume_long_frozen_today) >= amount:

                qapos.volume_long_frozen_today += amount
                return True
            else:
                print('SELLCLOSE 今日仓位不足')
        elif towards == ORDER_DIRECTION.SELL_CLOSETODAY:
            if (qapos.volume_long_today - qapos.volume_long_frozen_today) >= amount:
                # self.log("sellclosetoday")
                # self.log(self.volume_long_today - self.volume_long_frozen)
                # self.log(amount)
                qapos.volume_long_frozen_today += amount
                #qapos.volume_long_today -= amount
                return True
            else:
                self.log("SELLCLOSETODAY 今日仓位不足")
        elif towards in [ORDER_DIRECTION.BUY_OPEN,
                         ORDER_DIRECTION.SELL_OPEN,
                         ORDER_DIRECTION.BUY]:
            """
            冻结的保证金
            """
            coeff = float(price) * float(
                self.market_preset.get_code(code).get("unit_table",
                                                      1)
            ) * float(self.market_preset.get_code(code).get("buy_frozen_coeff",
                                                            1))
            moneyneed = coeff * amount
            if self.available > moneyneed:
                self.money -= moneyneed
                self.frozen[order_id] = {
                    'amount': amount,
                    'coeff': coeff,
                    'money': moneyneed
                }
                res = True
            else:
                self.log("开仓保证金不足 TOWARDS{} Need{} HAVE{}".format(
                    towards, moneyneed, self.available))
        # self.order_rule()
        return res

    def send_order(self, code: str, amount: float, price: float, towards: int, order_id: str = '', datetime: str = ''):

        if datetime:
            self.on_price_change(code, price, datetime)
        order_id = str(uuid.uuid4()) if order_id == '' else order_id
        if self.order_check(code, amount, price, towards, order_id):
            self.log("order check success")
            direction, offset = parse_orderdirection(towards)
            self.event_id += 1
            order = {
                "account_cookie": self.user_id,
                "user_id": self.user_id,
                "instrument_id": code,
                "towards": int(towards),
                "exchange_id": self.market_preset.get_exchange(code),
                "order_time": self.dtstr,
                "volume": int(amount),
                "price": float(price),
                "order_id": order_id,
                "seqno": self.event_id,
                "direction": direction,
                "offset": offset,
                "volume_orign": int(amount),
                "price_type": "LIMIT",
                "limit_price": float(price),
                "time_condition": "GFD",
                "volume_condition": "ANY",
                "insert_date_time": self.transform_dt(self.dtstr),
                'order_time': self.dtstr,
                "exchange_order_id": str(uuid.uuid4()),
                "status": "ALIVE",
                "volume_left": int(amount),
                "last_msg": "已报"
            }
            self.orders[order_id] = order
            self.log('下单成功 {}'.format(order_id))
            if self.model != 'BACKTEST':
                self.sync()
            self.on_ordersend(order)
            return order
        else:
            self.log(RuntimeError("ORDER CHECK FALSE: {}".format(code)))
            return False

    def on_ordersend(self, order):
        pass

    def cancel_order(self, order_id):
        """Initial
        撤单/ 释放冻结/

        """
        od = self.orders[order_id]
        od['last_msg'] = '已撤单'
        od['status'] = "CANCEL"
        od['volume_left'] = 0

        if od['offset'] in ['CLOSE', 'CLOSETODAY']:
            pos = self.positions[od['exchange_id'] + '.' + od['instrument_id']]
            if od['direction'] == 'BUY':
                pos.volume_short_frozen_today += od['volume_left']
            else:
                pos.volume_long_frozen_today += od['volume_left']
        else:
            frozen = self.frozen[order_id]
            self.money += frozen['money']
            frozen['amount'] = 0
            frozen['money'] = 0
            self.frozen[order_id] = frozen

        self.orders[order_id] = od

        self.log('撤单成功 {}'.format(order_id))

    def make_deal(self, order: dict):
        if isinstance(order, dict):
            self.receive_deal(order["instrument_id"], trade_price=order["limit_price"], trade_time=self.dtstr,
                              trade_amount=order["volume_left"], trade_towards=order["towards"],
                              order_id=order['order_id'], trade_id=str(uuid.uuid4()))

    def receive_deal(self,
                     code,
                     trade_price,
                     trade_amount,
                     trade_towards,
                     trade_time,
                     message=None,
                     order_id=None,
                     trade_id=None,
                     realorder_id=None):
        if order_id in self.orders.keys():

            # update order
            od = self.orders[order_id]
            frozen = self.frozen.get(
                order_id, {'order_id': order_id, 'money': 0, 'price': 0})
            vl = od.get('volume_left', 0)
            if trade_amount == vl:

                self.money += frozen['money']
                frozen['amount'] = 0
                frozen['money'] = 0
                od['last_msg'] = '全部成交'
                od["status"] = "FINISHED"
                self.log('全部成交 {}'.format(order_id))

            elif trade_amount < vl:
                frozen['amount'] = vl - trade_amount
                release_money = trade_amount * frozen.get('coeff', 1)
                self.money += release_money

                frozen['money'] -= release_money

                od['last_msg'] = '部分成交'
                od["status"] = "ALIVE"
                self.log('部分成交 {}'.format(order_id))

            od['volume_left'] -= trade_amount

            self.orders[order_id] = od
            self.frozen[order_id] = frozen
            # update trade
            self.event_id += 1
            trade_id = str(uuid.uuid4()) if trade_id is None else trade_id

            self.trades[trade_id] = {
                "seqno": self.event_id,
                "user_id":  self.user_id,
                "trade_id": trade_id,
                "exchange_id": od['exchange_id'],
                "instrument_id": od['instrument_id'],
                "order_id": order_id,
                "exchange_trade_id": trade_id,
                "direction": od['direction'],
                "offset": od['offset'],
                "volume": trade_amount,
                "price": trade_price,
                "trade_time": trade_time,
                "commission": float(0),
                "trade_date_time": self.transform_dt(trade_time)}

            # update accounts
            print('update trade')

            margin, close_profit = self.get_position(code).update_pos(
                trade_price, trade_amount, trade_towards)

            self.money -= (margin - close_profit)
            self.close_profit += close_profit
            if self.model != "BACKTEST":
                self.sync()

    def get_position(self, code: str = None) -> QA_Position:

        """
        兼容 code.XSHE 诸如
        
        """

        


        if code is None:
            return list(self.positions.values())[0]
        else:
            code = self.format_code(code)
            if code not in self.positions.keys():
                pos = QA_Position(code=code)
                self.positions[code] = pos

            return self.positions[code]

    def query_trade(self):
        pass

    def on_tick(self, tick):
        pass

    def on_bar(self, bar):
        pass

    def format_code(self, code):
        
        if '.' in code:
            return code
        else:
            return self.market_preset.get_exchange(code) + '.' + code

    def on_price_change(self, code, price, datetime=None):
        code = self.format_code(code)

        if code in self.positions.keys():
            try:
                pos = self.get_position(code.split('.')[1])
                if pos.last_price == price:
                    pass
                else:
                    pos.last_price = price

                if self.model != 'BACKTEST':
                    self.sync()
            except Exception as e:

                self.log(e)

        if datetime:
            self.datetime = datetime

    def order_schedule(self, code: str, amount: float, price: float, towards: int, order_id: str = ''):
        """
        预调仓接口
        """
        if order_id == '':
            order_id = str(uuid.uuid4())
        orderx = {
            'code': code,
            'amount': amount,
            'price': price,
            'towards': towards,
            'order_id': order_id
        }
        self.schedule[order_id] = orderx


if __name__ == "__main__":
    # acc = QIFI_Account("x1", "x1")
    # acc.initial()

    # acc.log(acc.message)

    # r = acc.send_order('RB2001', 10, 5000, ORDER_DIRECTION.BUY_OPEN)
    # acc.log(r)

    # acc.receive_deal(r['instrument_id'], 4500, r['volume'], r['towards'],
    #                  acc.dtstr, order_id=r['order_id'], trade_id=str(uuid.uuid4()))

    # acc.log(acc.message)

    # acc.sync()

    # this is a stock account

    acc2 = QIFI_Account("x1", "x1")
    print('test for initial')
    acc2.initial()

    acc2.log(acc2.message)

    print('test for buy order')

    r = acc2.send_order('000001', 10, 12, ORDER_DIRECTION.BUY)
    acc2.log(r)

    print('test for receivedeal')

    acc2.receive_deal(r['instrument_id'], 11.8, r['volume'], r['towards'],
                      acc2.dtstr, order_id=r['order_id'], trade_id=str(uuid.uuid4()))

    acc2.log(acc2.message)

    print('test for sync')
    acc2.sync()

    print('test for settle')
