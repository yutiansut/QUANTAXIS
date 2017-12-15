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

from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAMarket.QAOrder import QA_Order, QA_Order_list
# 2017/6/4修改: 去除总资产的动态权益计算


class QA_Account():
    """
    账户类:    
    记录回测的时候的账户情况(持仓列表,交易历史,利润,报单,可用资金)


    新增一个  已委托待成交队列,以及在途资金
    """
    # 一个hold改成list模式

    def __init__(self, strategy_name='', user='', market_type='0x01',
                 hold=[['date', 'code', 'price', 'amount', 'order_id', 'trade_id']],
                 sell_available=[['date', 'code', 'price',
                                  'amount', 'order_id', 'trade_id']],
                 init_assest=1000000, order_queue=pd.DataFrame(),
                 cash=[], history=[], detail=[], assets=None,
                 account_cookie=None):

        self.hold = hold
        self.sell_available = sell_available
        self.init_assest = init_assest
        self.strategy_name = strategy_name
        self.user = user
        self.market_type = market_type

        self.cash = [self.init_assest] if len(cash) < 1 else cash
        self.cash_available = self.cash[-1]  # 可用资金
        self.order_queue = order_queue  # 已委托待成交队列
        self.history = history
        self.detail = detail
        self.assets = [self.init_assest] if assets is None else assets
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
                'date_stamp': datetime.datetime.now().timestamp()
            }
        }

    def __repr__(self):
        return '<QA_Account {} Assets:{}>'.format(self.account_cookie, self.assets[-1])

    def init(self, init_assest=None):
        self.hold = [['date', 'code', 'price',
                      'amount', 'order_id', 'trade_id']]
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
                'date_stamp': datetime.datetime.now().timestamp()
            }
        }

    def QA_account_update(self, update_message):
        if str(update_message['status'])[0] == '2':

            # towards>1 买入成功
            # towards<1 卖出成功

            (__new_code, __new_amount, __new_trade_date, __new_towards,
                __new_price, __new_order_id,
                __new_trade_id, __new_trade_fee) = (str(update_message['bid']['code']),
                                                    float(update_message['bid']['amount']), str(
                                                        update_message['bid']['datetime']),
                                                    int(update_message['bid']['towards']), float(
                                                        update_message['bid']['price']),
                                                    str(update_message['order_id']), str(
                                                        update_message['trade_id']),
                                                    float(update_message['fee']['commission']))
            if int(update_message['status']) == 203:
                '委托成功 待交易'
                self.order_queue.append(
                    [__new_trade_date, __new_code, __new_price, __new_amount,
                     __new_order_id, __new_trade_id])

                # 如果是买入的waiting  那么要减少可用资金,增加在途资金
                # 如果是卖出的waiting 则减少hold_list
            elif int(update_message['status']) == 200:
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

                        if len(self.hold) > 1:
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
                    for __hold_id in range(1, len(self.hold)):
                        if int(self.hold[__hold_id][3]) == 0:
                            __del_id.append(__hold_id)
                    __del_id.sort()
                    __del_id.reverse()

                    for __item in __del_id:
                        self.hold.pop(__item)

            # 将交易记录插入历史交易记录
        else:
            pass
        self.QA_account_calc_profit(update_message)
        self.message = {
            'header': {
                'source': 'account',
                'cookie': self.account_cookie,
                'session': {
                    'user': update_message['user'],
                    'strategy': update_message['strategy'],
                    'code': update_message['bid']['code']
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

    def QA_account_calc_profit(self, update_message):
        if update_message['status'] == 200 and update_message['bid']['towards'] == 1:
            # 买入/
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值

            # 买入的部分在update_message

            # 可用资金=上一期可用资金-买入的资金
            self.cash.append(float(self.cash[-1]) - float(
                update_message['bid']['price']) * float(
                    update_message['bid']['amount']) * update_message['bid']['towards'] - float(update_message['fee']['commission']))

        elif update_message['status'] == 200 and update_message['bid']['towards'] == -1:
            # success trade,sell
            # 证券价值=买入的证券价值+持有到结算(收盘价)的价值
            # 买入的部分在update_message

            # 卖出的时候,towards=-1,所以是加上卖出的资产
            # 可用资金=上一期可用资金+卖出的资金
            self.cash.append(float(self.cash[-1]) - float(
                update_message['bid']['price']) * float(
                    update_message['bid']['amount']) * update_message['bid']['towards'] - float(update_message['fee']['commission']))

            # 更新可用资金历史

            # hold
        market_value = 0
        for i in range(1, len(self.hold)):
            market_value += (float(self.hold[i][2]) * float(self.hold[i][3]))
        self.assets.append(self.cash[-1] + market_value)

    def QA_account_receive_deal(self, _message):
        # 主要是把从market拿到的数据进行解包,一个一个发送给账户进行更新,再把最后的结果反回
        __data = self.QA_account_update({
            'code': _message['header']['code'],
            'status': _message['header']['status'],
            'user': _message['header']['session']['user'],
            'strategy': _message['header']['session']['strategy'],
            'trade_id': _message['header']['trade_id'],
            'order_id': _message['header']['order_id'],
            'date_stamp': str(time.mktime(datetime.datetime.now().timetuple())),
            'bid': _message['body']['bid'],
            'market': _message['body']['market'],
            'fee': _message['body']['fee'],
        })
        return __data

    def QA_account_receive_order(self, _message):

        # 主要是把从market拿到的数据进行解包,一个一个发送给账户进行更新,再把最后的结果反回
        __data = self.QA_account_update({
            'code': _message['header']['code'],
            'status': _message['header']['status'],
            'user': _message['header']['session']['user'],
            'strategy': _message['header']['session']['strategy'],
            'trade_id': _message['header']['trade_id'],
            'order_id': _message['header']['order_id'],
            'date_stamp': str(time.mktime(datetime.datetime.now().timetuple())),
            'bid': _message['body']['bid'],
            'market': _message['body']['market'],
            'fee': _message['body']['fee'],
        })
        return __data

    def QA_account_calc_assets(self):
        'get the real assets [from cash and market values]'

        return self.cash[-1] + sum([float(self.hold[i][2]) * float(self.hold[i][3]) for i in range(1, len(self.hold))])

    def send_order(self, code, amount, time, towards, order_type):

        date= str(time)[0:10] if len(str(time))==19 else str(time)
            
        _order = QA_Order()  # init
        (_order.user, _order.strategy, _order.account_cookie,
         _order.code, _order.date, _order.datetime,
         _order.sending_time,
         _order.amount, _order.towards) = (self.user, self.strategy_name, self.account_cookie,
                                       code, date, time,
                                       time, amount, towards)
        return _order

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
