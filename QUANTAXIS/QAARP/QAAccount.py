# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
import random
import time

import numpy as np
import pandas as pd

from QUANTAXIS.QAMarket.QAOrder import QA_Order, QA_OrderQueue
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, ORDER_DIRECTION, AMOUNT_MODEL, ORDER_MODEL
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic

# 2017/6/4修改: 去除总资产的动态权益计算


class QA_Account():
    """[QA_Account]

    [description]
    QA_Account 是QUANTAXIS的最小不可分割单元之一

    QA_Account
    """

    # 一个hold改成list模式

    def __init__(self, strategy_name='', user='', account_type=MARKET_TYPE.STOCK_DAY,
                 hold=None,
                 sell_available=None,
                 init_assest=None, order_queue=None,
                 cash=None, history=None, detail=None, assets=None,
                 account_cookie=None):
        self._history_headers = ['datetime', 'code', 'price',
                                 'towards', 'amount', 'order_id', 'trade_id', 'commission_fee']
        self._detail_headers = ['datetime', 'code', 'price', 'towards', 'amount', 'order_id', 'trade_id',
                                'match_price', 'match_order_id', 'match_trade_id', 'commission_fee', 'match_commission']
        self._hold_headers = ['datetime', 'code',
                              'price', 'amount', 'order_id', 'trade_id']

        self.hold = [] if hold is None else hold

        self.init_assest = 1000000 if init_assest is None else init_assest
        self.strategy_name = strategy_name
        self.user = user
        self.account_type = account_type

        self.cash = [self.init_assest] if cash is None else cash
        self.assets = [self.init_assest] if assets is None else assets

        self.cash_available = self.cash[-1]  # 可用资金
        self.sell_available = [['datetime', 'code', 'price',
                                'amount', 'order_id', 'trade_id']] if sell_available is None else sell_available
        self.order_queue = pd.DataFrame() if order_queue is None else order_queue  # 已委托待成交队列

        self.history = [] if history is None else history
        self.detail = [] if detail is None else detail

        self.account_cookie = QA_util_random_with_topic(
            'Acc') if account_cookie is None else account_cookie
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': self.user,
                    'strategy': self.strategy_name
                }
            },
            'body': {
                'account': {
                    'hold': self.hold,
                    'cash': self.cash,
                    'assets': self.cash,
                    'history': self.history,
                    'detail': self.detail
                },
                'running_time': str(datetime.datetime.now())
            }
        }

    def __repr__(self):
        return '<QA_Account {} Assets:{}>'.format(self.account_cookie, self.assets[-1])

    @property
    def latest_assets(self):
        return self.assets[-1]
    @property
    def latest_cash(self):
        return self.cash[-1]

    @property
    def latest_hold(self):
        return self.hold
    
    def init(self, init_assest=None):
        self.hold = []
        self.sell_available = [['date', 'code', 'price',
                                'amount', 'order_id', 'trade_id']]
        self.history = []

        self.account_cookie = QA_util_random_with_topic(topic='Acc')
        self.assets = [self.init_assest]
        self.cash = [self.init_assest]
        self.cash_available = self.cash[-1]  # 在途资金
        self.order_queue = pd.DataFrame()   # 已委托待成交队列
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': '',
                    'strategy': ''
                }
            },
            'body': {
                'account': {
                    'hold': self.hold,
                    'cash': self.cash,
                    'assets': self.cash,
                    'history': self.history,
                    'detail': self.detail
                },
                'running_time': str(datetime.datetime.now())
            }
        }

    def update(self, message):
        """[用于更新账户]

        [description]

        Arguments:
            message {json/dict} -- message_from_deal

        Returns:
            {json} -- message of account
        """

        if str(message['header']['status'])[0] == '2':

            # towards>1 买入成功
            # towards<1 卖出成功

            (__new_code, __new_amount, __new_trade_date, __new_towards,
                __new_price, __new_order_id,
                __new_trade_id, __new_trade_fee) = (str(message['body']['bid']['code']),
                                                    float(message['body']['bid']['amount']), str(
                                                        message['body']['bid']['datetime']),
                                                    int(message['body']['bid']['towards']), float(
                                                        message['body']['bid']['price']),
                                                    str(message['header']['order_id']), str(
                                                        message['header']['trade_id']),
                                                    float(message['body']['fee']['commission']))
            if int(message['header']['status']) == 203:
                '委托成功 待交易'
                self.order_queue.append(
                    [__new_trade_date, __new_code, __new_price, __new_amount,
                     __new_order_id, __new_trade_id])

                # 如果是买入的waiting  那么要减少可用资金,增加在途资金
                # 如果是卖出的waiting 则减少hold_list
            elif int(message['header']['status']) == 200:
                '交易成功的处理'
                self.history.append(
                    [__new_trade_date, __new_code, __new_price, __new_towards,
                     __new_amount, __new_order_id, __new_trade_id, __new_trade_fee])
                # 先计算收益和利润

                # 修改持仓表
                if int(__new_towards) > 0:
                    # 买入
                    self.hold.append(
                        [__new_trade_date, __new_code, __new_price, __new_amount,
                         __new_order_id, __new_trade_id])
                    self.detail.append([__new_trade_date, __new_code, __new_price,
                                        __new_amount, __new_order_id, __new_trade_id,
                                        [], [], [], [], __new_amount, __new_trade_fee])
                # 将交易记录插入历史交易记录
                else:
                    # 卖出
                    __pop_list = []
                    while __new_amount > 0:

                        if len(self.hold) > 0:
                            for i in range(0, len(self.hold)):

                                if __new_code in self.hold[i]:
                                    if float(__new_amount) > (self.hold[i][3]):

                                        __new_amount = __new_amount - \
                                            self.hold[i][3]

                                        __pop_list.append(i)

                                    elif float(__new_amount) < float(self.hold[i][3]):
                                        self.hold[i][3] = self.hold[i][3] - \
                                            __new_amount

                                        for __item_detail in self.detail:
                                            if __item_detail[5] == self.hold[i][5] and \
                                                    __new_trade_id not in __item_detail[7]:
                                                __item_detail[6].append(
                                                    __new_price)
                                                __item_detail[7].append(
                                                    __new_order_id)
                                                __item_detail[8].append(
                                                    __new_trade_id)
                                                __item_detail[9].append(
                                                    __new_trade_date)
                                                __item_detail[10] = self.hold[i][3] - \
                                                    __new_amount
                                                __item_detail[11] += __new_trade_fee
                                        __new_amount = 0
                                    elif float(__new_amount) == float(self.hold[i][3]):

                                        __new_amount = 0
                                        __pop_list.append(i)

                    __pop_list.sort()
                    __pop_list.reverse()
                    for __id in __pop_list:

                        for __item_detail in self.detail:
                            if __item_detail[5] == self.hold[__id][5] and \
                                    __new_trade_id not in __item_detail[7]:
                                __item_detail[6].append(__new_price)
                                __item_detail[7].append(__new_order_id)
                                __item_detail[8].append(__new_trade_id)
                                __item_detail[9].append(__new_trade_date)
                                __item_detail[10] = 0
                                __item_detail[11] += __new_trade_fee

                        self.hold.pop(__id)
                    __del_id = []
                    for __hold_id in range(0, len(self.hold)):
                        if int(self.hold[__hold_id][3]) == 0:
                            __del_id.append(__hold_id)
                    __del_id.sort()
                    __del_id.reverse()

                    for __item in __del_id:
                        self.hold.pop(__item)

            # 将交易记录插入历史交易记录
        else:
            pass
        self.calc_profit(message)
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': message['header']['session']['user'],
                    'strategy': message['header']['session']['strategy'],
                    'code': message['body']['bid']['code']
                }

            },
            'body': {
                'account': {
                    'hold': self.hold,
                    'history': self.history,
                    'cash': self.cash,
                    'assets': self.assets,
                    'detail': self.detail
                },
                'time': str(datetime.datetime.now()),
                'date_stamp': datetime.datetime.now().timestamp()
            }
        }

        return self.message

    def calc_profit(self, message):
        """用于计算profit

        [description]

        Arguments:
            message {[type]} -- [description]
        """

        if message['header']['status'] == 200 and message['body']['bid']['towards'] == 1:
            # 买入/
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值

            # 买入的部分在update_message

            # 可用资金=上一期可用资金-买入的资金
            self.cash.append(float(self.cash[-1]) - float(
                message['body']['bid']['price']) * float(
                    message['body']['bid']['amount']) * message['body']['bid']['towards'] - float(message['body']['fee']['commission']))

        elif message['header']['status'] == 200 and message['body']['bid']['towards'] == -1:
            # success trade,sell
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值
            # 买入的部分在update_message

            # 卖出的时候,towards=-1,所以是加上卖出的资产
            # 可用资金=上一期可用资金+卖出的资金
            self.cash.append(float(self.cash[-1]) - float(
                message['body']['bid']['price']) * float(
                    message['body']['bid']['amount']) * message['body']['bid']['towards'] - float(message['body']['fee']['commission']))

            # 更新可用资金历史

            # hold
        market_value = 0
        for i in range(0, len(self.hold)):
            market_value += (float(self.hold[i][2]) * float(self.hold[i][3]))
        self.assets.append(self.cash[-1] + market_value)

    def receive_deal(self, _message):
        """[主要是把从market拿到的数据进行解包,一个一个发送给账户进行更新,再把最后的结果反回]

        [description]

        Arguments:
            _message {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.update(_message)

    def calc_assets(self):
        'get the real assets [from cash and market values]'

        return self.cash[-1] + sum([float(self.hold[i][2]) * float(self.hold[i][3]) for i in range(0, len(self.hold))])

    def send_order(self, code, amount, time, towards, order_model, amount_model):
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

        date = str(time)[0:10] if len(str(time)) == 19 else str(time)
        time = str(time) if len(
            str(time)) == 19 else '{} 09:31:00'.format(str(time)[0:10])

        return QA_Order(user=self.user, strategy=self.strategy_name,
                          account_cookie=self.account_cookie, code=code,
                          date=date, datetime=time, sending_time=time,
                          btype=self.account_type, amount=amount,
                          order_model=order_model, towards=towards,amount_model=amount_model)  # init


    def from_message(self, message):

        self.account_cookie = message['header']['cookie']
        self.hold = message['body']['account']['hold']
        self.history = message['body']['account']['history']
        self.cash = message['body']['account']['cash']
        self.assets = message['body']['account']['assets']
        self.detail = message['body']['account']['detail']
        return self


class QA_Account_min(QA_Account):
    pass


if __name__ == '__main__':
    account = QA_Account()
    # 创建一个account账户
