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


import pandas as pd

from QUANTAXIS.QAEngine.QAEvent import QA_Worker
from QUANTAXIS.QAMarket.QAOrder import QA_Order
from QUANTAXIS.QAUtil.QAParameter import (ACCOUNT_EVENT, AMOUNT_MODEL,
                                          BROKER_TYPE, ENGINE_EVENT,
                                          MARKET_TYPE, ORDER_DIRECTION,
                                          TRADE_STATUS)
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic

# 2017/6/4修改: 去除总资产的动态权益计算


class QA_Account(QA_Worker):
    """[QA_Account]

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


    """

    def __init__(self, strategy_name=None, user=None, account_type=MARKET_TYPE.STOCK_DAY,
                 broker=BROKER_TYPE.BACKETEST, portfolio=None, account_cookie=None,
                 sell_available=None, init_assets=None, cash=None, history=None,
                 margin_level=False, allow_t0=False, allow_sellopen=False):
        super().__init__()
        self._history_headers = ['datetime', 'code', 'price',
                                 'amount', 'order_id', 'trade_id', 'commission_fee']
        # 信息类:
        self.strategy_name = strategy_name
        self.user = user
        self.account_type = account_type
        self.portfolio = portfolio
        self.account_cookie = QA_util_random_with_topic(
            'Acc') if account_cookie is None else account_cookie
        self.broker = broker
        self.market_data = None
        self._currenttime = None
        # 资产类
        self.init_assets = 1000000 if init_assets is None else init_assets
        self.cash = [self.init_assets] if cash is None else cash
        self.cash_available = self.cash[-1]  # 可用资金
        self.sell_available = sell_available
        self.history = [] if history is None else history

        # 规则类
        # 两个规则
        # 1.是否允许t+0 及买入及结算
        # 2.是否允许卖空开仓
        # 3.是否允许保证金交易
        self.allow_t0 = allow_t0
        self.allow_sellopen = allow_sellopen
        self.margin_level = margin_level

    def __repr__(self):
        return '< QA_Account {}>'.format(self.account_cookie)

    @property
    def message(self):
        return {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'portfolio': self.portfolio,
                'user': self.user,
                'strategy_name': self.strategy_name,
                'current_time': self._currenttime
            },
            'body': {
                'account': {
                    'cash': self.cash,
                    'history': self.history,
                }
            }
        }

    @property
    def hold(self):
        return pd.DataFrame(data=self.history, columns=self._history_headers).groupby('code').amount.sum()

    @property
    def latest_cash(self):
        'return the lastest cash'
        return self.cash[-1]

    @property
    def current_time(self):
        return self._currenttime

    def reset_assets(self, init_assets=None):
        'reset_history/cash/'
        self.sell_available = None
        self.history = []
        self.init_assets = init_assets
        self.cash = [self.init_assets]
        self.cash_available = self.cash[-1]  # 在途资金

    def receive_deal(self, message):
        """[用于更新账户]

        [description]

        update history and cash
        """

        if message['header']['status'] is TRADE_STATUS.SUCCESS:
            self.history.append(
                [str(message['body']['order']['datetime']), str(message['body']['order']['code']),
                 float(message['body']['order']['price']), int(message['body']['order']['towards']) *
                 float(message['body']['order']['amount']), str(
                     message['header']['order_id']),
                 str(message['header']['trade_id']), float(message['body']['fee']['commission'])])
            self.cash.append(float(self.cash[-1]) - float(message['body']['order']['price']) *
                             float(message['body']['order']['amount']) * message['body']['order']['towards'] -
                             float(message['body']['fee']['commission']))

        return self.message

    def send_order(self, code, amount, time, towards, price, order_model, amount_model, data_type, market_type):
        """[summary]

        [description]

        Arguments:
            code {[type]} -- [description]
            amount {[type]} -- [description]
            time {[type]} -- [description]
            towards {[type]} -- [description]
            order_model {[type]} -- [description]
            amount_model {[type]} -- [description]

        Returns:
            [type] -- [description]
        """
        flag = False
        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        time = str(time) if len(
            str(time)) == 19 else '{} 09:31:00'.format(str(time)[0:10])
        if towards in [ORDER_DIRECTION.BUY] and amount_model is AMOUNT_MODEL.BY_AMOUNT:
            if self.cash_available > amount * price:
                self.cash_available -= amount * price
                flag = True
        if towards in [ORDER_DIRECTION.BUY] and amount_model is AMOUNT_MODEL.BY_PRICE:
            if self.cash_available > amount:
                self.cash_available -= amount
                flag = True
        elif towards in [ORDER_DIRECTION.SELL] and amount_model is AMOUNT_MODEL.BY_AMOUNT:
            if self.sell_available[code] > amount:
                self.sell_available[code] -= amount
                flag = True
        elif towards in [ORDER_DIRECTION.SELL] and amount_model is AMOUNT_MODEL.BY_PRICE:

            if self.allow_sellopen:
                flag = True

            if self.sell_available.get(code, 0) > amount:
                self.sell_available[code] -= int(amount / price * 100) * 100
                flag = True
        if flag:
            return QA_Order(user=self.user, strategy=self.strategy_name, data_type=data_type,
                            account_cookie=self.account_cookie, code=code, market_type=market_type,
                            date=date, datetime=time, sending_time=time,
                            btype=self.account_type, amount=amount, price=price,
                            order_model=order_model, towards=towards, amount_model=amount_model)  # init
        else:
            return flag

    def settle(self):
        '同步可用资金/可卖股票'
        self.cash_available = self.cash[-1]
        self.sell_available = self.hold
        # self.sell_available = pass

    def on_bar(self, event):
        'while updating the market data'
        print(event.market_data)

    def on_tick(self, event):
        'on tick event'
        pass

    def from_message(self, message):
        """resume the account from standard message
        这个是从数据库恢复账户时需要的"""
        self.portfolio = message.get('portfolio', None)
        self.user = message.get('user', None)
        self.account_cookie = message.get('account_cookie', None)
        self.history = message['body']['account']['history']
        self.cash = message['body']['account']['cash']
        return self

    def run(self, event):
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
                                   price=event.price, order_model=event.order_model,
                                   data_type=event.data_type,
                                   market_type=event.market_type)
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
                self.market_data.append(event.market_data)
            self.on_bar(event)

            if event.callback:
                event.callback(event)


if __name__ == '__main__':
    account = QA_Account()
    # 创建一个account账户
