# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import datetime

import numpy as np
import pandas as pd

from QUANTAXIS.QAEngine.QAEvent import QA_Worker
from QUANTAXIS.QAMarket.QAOrder import QA_Order, QA_OrderQueue
from QUANTAXIS.QASU.save_account import save_account, update_account
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_trade_range
from QUANTAXIS.QAUtil.QAParameter import (ACCOUNT_EVENT, AMOUNT_MODEL,
                                          BROKER_TYPE, ENGINE_EVENT, FREQUENCE,
                                          MARKET_TYPE, TRADE_STATUS)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic

# 2017/6/4修改: 去除总资产的动态权益计算


# pylint: disable=old-style-class, too-few-public-methods
class QA_Account(QA_Worker):
    """QA_Account
    User-->Portfolio-->Account/Strategy

    :::::::::::::::::::::::::::::::::::::::::::::::::
    ::        :: Portfolio 1 -- Account/Strategy 1 ::
    ::  USER  ::             -- Account/Strategy 2 ::
    ::        :: Portfolio 2 -- Account/Strategy 3 ::
    :::::::::::::::::::::::::::::::::::::::::::::::::

    2018/1/5 再次修改 改版本去掉了多余的计算 精简账户更新
    ======================

    - 不再计算总资产/不再计算当前持仓/不再计算交易对照明细表
    - 不再动态计算账户股票/期货市值
    - 只维护 cash/history两个字段 剩下的全部惰性计算


    QA_Account 是QUANTAXIS的最小不可分割单元之一

    QA_Account是账户类 需要兼容股票/期货/指数
    QA_Account继承自QA_Worker 可以被事件驱动
    QA_Account可以直接被QA_Strategy继承

    有三类输入:
    信息类: 账户绑定的策略名/账户的用户名/账户类别/账户识别码/账户的broker
    资产类: 现金/可用现金/交易历史/交易对照表
    规则类: 是否允许卖空/是否允许t0结算

    方法:
    惰性计算:最新持仓/最新总资产/最新现金/持仓面板
    生成订单/接受交易结果数据
    接收新的数据/on_bar/on_tick方法/缓存新数据的market_data

    @royburns  1.添加注释
    2018/05/18
    """

    def __init__(self, strategy_name=None, user_cookie=None, market_type=MARKET_TYPE.STOCK_CN, frequence=FREQUENCE.DAY,
                 broker=BROKER_TYPE.BACKETEST, portfolio_cookie=None, account_cookie=None,
                 sell_available={}, init_assets=None, cash=None, history=None, commission_coeff=0.00025, tax_coeff=0.0015,
                 margin_level=False, allow_t0=False, allow_sellopen=False):
        """

        :param strategy_name:  策略名称
        :param user_cookie:   用户cookie
        :param market_type:   市场类别 默认QA.MARKET_TYPE.STOCK_CN A股股票
        :param frequence:     账户级别 默认日线QA.FREQUENCE.DAY
        :param broker:        BROEKR类 默认回测 QA.BROKER_TYPE.BACKTEST
        :param portfolio_cookie: 组合cookie
        :param account_cookie:   账户cookie
        :param sell_available:   可卖股票数
        :param init_assets:       初始资产  默认 1000000 元 （100万）
        :param cash:              可用现金  默认 是 初始资产  list 类型
        :param history:           交易历史
        :param commission_coeff:  交易佣金 :默认 万2.5   float 类型
        :param tax_coeff:         印花税   :默认 千1.5   float 类型
        :param margin_level:      保证金比例 默认False
        :param allow_t0:          是否允许t+0交易  默认False
        :param allow_sellopen:    是否允许卖空开仓  默认False
        """
        super().__init__()
        self._history_headers = ['datetime', 'code', 'price',
                                 'amount', 'order_id', 'trade_id',
                                 'account_cookie', 'commission', 'tax']
        ########################################################################
        # 信息类:
        self.strategy_name = strategy_name
        self.user_cookie = user_cookie
        self.market_type = market_type
        self.portfolio_cookie = portfolio_cookie
        self.account_cookie = QA_util_random_with_topic(
            'Acc') if account_cookie is None else account_cookie
        self.broker = broker
        self.frequence = frequence
        self.market_data = None
        self._currenttime = None
        self.commission_coeff = commission_coeff
        self.tax_coeff = tax_coeff
        self.running_time = datetime.datetime.now()
        ########################################################################
        # 资产类
        self.orders = QA_OrderQueue()  # 历史委托单
        self.init_assets = 1000000 if init_assets is None else init_assets
        self.cash = [self.init_assets] if cash is None else cash
        self.cash_available = self.cash[-1]    # 可用资金
        self.sell_available = sell_available
        self.history = [] if history is None else history
        self.time_index = []
        ########################################################################
        # 规则类
        # 两个规则
        # 1.是否允许t+0 及买入及结算
        # 2.是否允许卖空开仓
        # 3.是否允许保证金交易/ 如果不是false 就需要制定保证金比例(dict形式)
        self.allow_t0 = allow_t0
        self.allow_sellopen = allow_sellopen
        self.margin_level = margin_level

    def __repr__(self):
        return '< QA_Account {}>'.format(self.account_cookie)

    @property
    def message(self):
        'the standard message which can be transef'
        return {
            'source': 'account',
            'account_cookie': self.account_cookie,
            'portfolio_cookie': self.portfolio_cookie,
            'user_cookie': self.user_cookie,
            'broker': self.broker,
            'market_type': self.market_type,
            'strategy_name': self.strategy_name,
            'current_time': self._currenttime,
            'allow_sellopen': self.allow_sellopen,
            'allow_t0': self.allow_t0,
            'margin_level': self.margin_level,
            'init_assets': self.init_assets,
            'commission_coeff': self.commission_coeff,
            'tax_coeff': self.tax_coeff,
            'cash': self.cash,
            'history': self.history,
            'trade_index': self.time_index,
            'running_time': datetime.datetime.now()
        }

    @property
    def code(self):
        """
        该账户曾交易代码 用set 去重
        """
        return list(set([item[1] for item in self.history]))

    @property
    def start_date(self):
        return min(self.time_index)[0:10]

    @property
    def end_date(self):
        return max(self.time_index)[0:10]

    @property
    def trade_range(self):
        return QA_util_get_trade_range(self.start_date, self.end_date)

    @property
    def history_table(self):
        '交易历史的table'
        return pd.DataFrame(data=self.history, columns=self._history_headers).sort_index()

    @property
    def cash_table(self):
        '现金的table'
        _cash = pd.DataFrame(data=[self.cash[1::], self.time_index], index=[
                             'cash', 'datetime']).T
        _cash = _cash.assign(date=_cash.datetime.apply(lambda x: pd.to_datetime(str(x)[0:10]))).assign(
            account_cookie=self.account_cookie)
        return _cash.set_index(['datetime', 'account_cookie'], drop=False).sort_index()

    @property
    def hold(self):
        '持仓'
        return pd.DataFrame(data=self.history, columns=self._history_headers).groupby('code').amount.sum().sort_index()

    @property
    def order_table(self):
        """return order trade list"""
        return self.orders.trade_list

    @property
    def trade(self):
        '每次交易的pivot表'
        return self.history_table.pivot_table(index=['datetime', 'account_cookie'], columns='code', values='amount').fillna(0).sort_index()

    @property
    def daily_cash(self):
        '每日交易结算时的现金表'
        return self.cash_table.drop_duplicates(subset='date', keep='last').sort_index()

    @property
    def daily_hold(self):
        '每日交易结算时的持仓表'
        data = self.trade.cumsum()

        data = data.assign(account_cookie=self.account_cookie).assign(
            date=data.index.levels[0])
        data.date = data.date.apply(lambda x: str(x)[0:10])
        data=data.set_index(['date', 'account_cookie'])
        return data[~data.index.duplicated(keep='last')].sort_index()
    # 计算assets的时候 需要一个market_data=QA.QA_fetch_stock_day_adv(list(data.columns),data.index[0],data.index[-1])
    # (market_data.to_qfq().pivot('close')*data).sum(axis=1)+user_cookie.get_account(a_1).daily_cash.set_index('date').cash

    @property
    def latest_cash(self):
        'return the lastest cash 可用资金'
        return self.cash[-1]

    @property
    def current_time(self):
        'return current time (in backtest/real environment)'
        return self._currenttime

    def hold_table(self, datetime=None):
        "到某一个时刻的持仓 如果给的是日期,则返回当日开盘前的持仓"
        if datetime is None:
            return self.history_table.set_index('datetime').sort_index().groupby('code').amount.sum().sort_index()
        else:
            return self.history_table.set_index('datetime').sort_index().loc[:datetime].groupby('code').amount.sum().sort_index()

    def hold_price(self, datetime=None):
        "计算持仓成本  如果给的是日期,则返回当日开盘前的持仓"
        def weights(x):
            if sum(x['amount']) != 0:
                return np.average(x['price'], weights=x['amount'], returned=True)
            else:
                return (0, 0)
        if datetime is None:
            return self.history_table.set_index('datetime').sort_index().groupby('code').apply(weights)
        else:
            return self.history_table.set_index('datetime').sort_index().loc[:datetime].groupby('code').apply(weights)

    def reset_assets(self, init_assets=None):
        'reset_history/cash/'
        self.sell_available = {}
        self.history = []
        self.init_assets = init_assets
        self.cash = [self.init_assets]
        self.cash_available = self.cash[-1]  # 在途资金

    def receive_deal(self, message):
        """
        用于更新账户
        update history and cash
        :param message:
        :return:
        """
        if message['header']['status'] is TRADE_STATUS.SUCCESS:
            trade_amount = float(float(message['body']['order']['price']) *
                                 float(message['body']['order']['amount']) * message['body']['order']['towards'] +
                                 float(message['body']['fee']['commission']) +
                                 float(message['body']['fee']['tax']))

            if self.cash[-1] > trade_amount:
                self.time_index.append(
                    str(message['body']['order']['datetime']))
                self.history.append(
                    [str(message['body']['order']['datetime']), str(message['body']['order']['code']),
                     float(message['body']['order']['price']), int(message['body']['order']['towards']) *
                     float(message['body']['order']['amount']), str(
                        message['header']['order_id']), str(message['header']['trade_id']), str(self.account_cookie),
                     float(message['body']['fee']['commission']), float(message['body']['fee']['tax'])])
                self.cash.append(self.cash[-1]-trade_amount)
                self.cash_available = self.cash[-1]
                # 资金立刻结转
            else:
                print(message)
                print(self.cash[-1])
                self.cash_available = self.cash[-1]
                print('NOT ENOUGH MONEY FOR {}'.format(message['body']['order']))
        return self.message

    def send_order(self, code=None, amount=None, time=None, towards=None, price=None, money=None, order_model=None, amount_model=None):
        """
        ATTENTION CHANGELOG 1.0.28
        修改了Account的send_order方法, 区分按数量下单和按金额下单两种方式

        - AMOUNT_MODEL.BY_PRICE ==> AMOUNT_MODEL.BY_MONEY # 按金额下单
        - AMOUNT_MODEL.BY_AMOUNT # 按数量下单

        在按金额下单的时候,应给予 money参数
        在按数量下单的时候,应给予 amount参数

        python code:
        Account=QA.QA_Account()

        Order_bymoney=Account.send_order(code='000001',
                                        price=11,
                                        money=0.3*Account.cash_available,
                                        time='2018-05-09',
                                        towards=QA.ORDER_DIRECTION.BUY,
                                        order_model=QA.ORDER_MODEL.MARKET,
                                        amount_model=QA.AMOUNT_MODEL.BY_MONEY
                                        )

        Order_byamount=Account.send_order(code='000001',
                                        price=11,
                                        amount=100,
                                        time='2018-05-09',
                                        towards=QA.ORDER_DIRECTION.BUY,
                                        order_model=QA.ORDER_MODEL.MARKET,
                                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                                        )

        :param code: 证券代码
        :param amount: 买卖 数量多数股
        :param time:  Timestamp 对象 下单时间
        :param towards: int , towards>0 买入 towards<0 卖出
        :param price: 买入，卖出 标的证券的价格
        :param money: 买卖 价格
        :param order_model: 类型 QA.ORDER_MODE
        :param amount_model:类型 QA.AMOUNT_MODEL
        :return:
        """

        assert code is not None and time is not None and towards is not None and order_model is not None and amount_model is not None

        #todo 移到Utils类中，  时间转换
        # date 字符串 2011-10-11 长度10
        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        # time 字符串 20011-10-11 09:02:00  长度 19
        time = str(time) if len(str(time)) == 19 else '{} 09:31:00'.format(str(time)[0:10])

        #todo 移到Utils类中，  amount_to_money 成交量转金额
        # BY_MONEY :: amount --钱 如10000元  因此 by_money里面 需要指定价格,来计算实际的股票数
        # by_amount :: amount --股数 如10000股
        amount = amount if amount_model is AMOUNT_MODEL.BY_AMOUNT else int(
            money / (price*(1+self.commission_coeff)))

        #todo 移到Utils类中，  money_to_amount 金额转成交量
        money = amount * price * \
            (1+self.commission_coeff) if amount_model is AMOUNT_MODEL.BY_AMOUNT else money

        # amount_model = AMOUNT_MODEL.BY_AMOUNT

        # flag 判断买卖 数量和价格以及买卖方向是否正确
        flag = False

        assert (int(towards) != 0)
        if int(towards) > 0:
            # 是买入的情况(包括买入.买开.买平)
            if self.cash_available >= money:
                self.cash_available -= money
                if self.market_type is MARKET_TYPE.STOCK_CN:  # 如果是股票 买入的时候有100股的最小限制
                    amount = int(amount / 100) * 100
                flag = True
            else:
                print('可用资金不足')
        elif int(towards) < 0:
            # 是卖出的情况(包括卖出，卖出开仓allow_sellopen如果允许. 卖出平仓)
            if self.sell_available.get(code, 0) >= amount:
                self.sell_available[code] -= amount
                flag = True
            elif self.allow_sellopen:
                if self.cash_available > money:  # 卖空的市值小于现金（有担保的卖空）， 不允许裸卖空
                    flag = True
                else:
                    print("卖空资金不足/不允许裸卖空")
            else:
                print('资金股份不足/不允许卖空开仓')

        if flag and amount > 0:
            _order = QA_Order(user_cookie=self.user_cookie, strategy=self.strategy_name, frequence=self.frequence,
                              account_cookie=self.account_cookie, code=code, market_type=self.market_type,
                              date=date, datetime=time, sending_time=time, callback=self.receive_deal,
                              amount=amount, price=price, order_model=order_model, towards=towards, money=money,
                              amount_model=amount_model, commission_coeff=self.commission_coeff, tax_coeff=self.tax_coeff)  # init
            self.orders.insert_order(_order)  # 历史委托order状态存储， 保存到 QA_Order 对象中的队列中
            return _order
        else:
            print('ERROR : amount=0')
            return False

    def settle(self):
        '同步可用资金/可卖股票'
        self.sell_available = self.hold

    def on_bar(self, event):
        '''
        策略事件
        :param event:
        :return:
        '''
        'while updating the market data'
        print("on_bar ",event.market_data)

    def on_tick(self, event):
        '''
        策略事件
        :param event:
        :return:
        '''
        'on tick event'
        print("on_tick ",event.market_data)
        pass

    def from_message(self, message):
        """resume the account from standard message
        这个是从数据库恢复账户时需要的"""
        self.account_cookie = message.get('account_cookie', None)
        self.portfolio_cookie = message.get('portfolio_cookie', None)
        self.user_cookie = message.get('user_cookie', None)
        self.broker = message.get('broker', None)
        self.market_type = message.get('market_type', None)
        self.strategy_name = message.get('strategy_name', None)
        self._currenttime = message.get('current_time', None)
        self.allow_sellopen = message.get('allow_sellopen', False)
        self.allow_t0 = message.get('allow_t0', False)
        self.margin_level = message.get('margin_level', False)
        self.init_assets = message['init_assets']
        self.commission_coeff = message.get('commission_coeff', 0.00015)
        self.tax_coeff = message.get('tax_coeff', 0.0015)
        self.history = message['history']
        self.cash = message['cash']
        self.time_index = message['trade_index']
        self.running_time = message.get('running_time', None)
        self.settle()
        return self

    @property
    def table(self):
        """
        打印出account的内容
        """
        return pd.DataFrame([self.message, ]).set_index('account_cookie', drop=False).T

    def run(self, event):
        '''
        这个方法是被 QA_ThreadEngine 处理队列时候调用的， QA_Task 中 do 方法调用 run （在其它线程中）
 -      'QA_WORKER method 重载'
        :param event: 事件类型 QA_Event
        :return:
        '''
        'QA_WORKER method'
        if event.event_type is ACCOUNT_EVENT.SETTLE:
            self.settle()

        elif event.event_type is ACCOUNT_EVENT.UPDATE:
            self.receive_deal(event.message)
        elif event.event_type is ACCOUNT_EVENT.MAKE_ORDER:
            """generate order
            if callback callback the order
            if not return back the order
            """
            data = self.send_order(code=event.code, amount=event.amount, time=event.time,
                                   amount_model=event.amount_model, towards=event.towards,
                                   price=event.price, order_model=event.order_model)
            if event.callback:
                event.callback(data)
            else:
                return data
        elif event.event_type is ENGINE_EVENT.UPCOMING_DATA:
            """update the market_data
            1. update the inside market_data struct
            2. tell the on_bar methods
            """
            self._currenttime = event.market_data.datetime[-1]
            if self.market_data is None:
                self.market_data = event.market_data
            else:
                self.market_data = self.market_data + event.market_data
            self.on_bar(event)

            if event.callback:
                event.callback(event)

    def save(self):
        """
        存储账户信息
        """
        save_account(self.message)

    def change_cash(self, money):
        """
        外部操作|高危|
        """
        res = self.cash[-1]+money
        if res >= 0:
            # 高危操作
            self.cash[-1] = res

    def get_orders(self, if_today=True):
        '''
        返回当日委托/历史委托
        :param if_today: true 只返回今天的订单
        :return: QA_OrderQueue
        '''
        #todo 筛选其它不是今天的订单返回
        return self.orders


class Account_handler():
    def __init__(self):
        pass

    def get_account(self, message):
        pass


if __name__ == '__main__':
    account = QA_Account()
    # 创建一个account账户
