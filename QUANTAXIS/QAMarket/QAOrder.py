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

import time
import queue
import pandas as pd

from QUANTAXIS.QAUtil import (QA_util_log_info, QA_util_random_with_topic,
                              QA_util_to_json_from_pandas)


"""
重新定义Order模式

在2017-12-15的Account-remake-version 分支中

Bid类全部被更名为Order类

用于和 bid_ask 区分

by yutiansut@2017/12/15

"""


class QA_Order():
    def __init__(self, price=None, date=None, datetime=None, sending_time=None, transact_time=None, amount=None,
                 towards=None, code=None, user=None, account_cookie=None, strategy=None, btype=None, order_model=None, amount_model=None,
                 order_id=QA_util_random_with_topic(topic='Order'), trade_id=None, status='100'):
        self.price = price
        self.datetime = None
        if datetime is None and date is not None:
            self.date = date
            self.datetime = '{} 09:31:00'.format(self.date)

        elif date is None and datetime is not None:
            self.date = datetime[0:10]
            self.datetime = datetime

        elif date is not None and datetime is not None:
            self.date = date
            self.datetime = datetime
        else:
            QA_util_log_info('QA_ORDER WRONG: NO DATE OR DATETIME INIT')
        self.sending_time = self.datetime if sending_time is None else sending_time  # 下单时间

        self.transact_time = transact_time
        self.amount = amount
        self.towards = towards  # side
        self.code = code
        self.user = user
        self.account_cookie = account_cookie
        self.strategy = strategy
        self.type = btype  # see below
        self.order_model = order_model
        self.amount_model = amount_model
        self.order_id = order_id
        self.trade_id = trade_id
        self.status = status

    def __repr__(self):
        return '< QA_Order datetime:{} code:{} price:{} towards:{} btype:{} order_id:{} account:{} status:{} >'.format(
            self.datetime, self.code, self.price, self.towards, self.type, self.order_id, self.account_cookie, self.status)

    def stock_day(self):
        self.type = '0x01'
        return self

    def stock_min(self):
        self.type = '0x02'
        return self

    def index_day(self):
        self.type = '0x03'
        return self

    def index_min(self):
        self.type = '0x04'
        return self

    def stock_transaction(self):
        self.type = '0x05'
        return self

    def index_transaction(self):
        self.type = '0x06'
        return self

    def future_day(self):
        self.type = '1x01'
        return self

    def info(self):
        return vars(self)

    def to_df(self):
        return pd.DataFrame([vars(self), ])

    def to_dict(self):
        return vars(self)

    def from_dict(self, order):
        try:
            self.price = order['price']
            self.date = order['date']
            self.datetime = order['datetime']
            self.sending_time = order['sending_time']  # 下单时间
            self.transact_time = order['transact_time']
            self.amount = order['amount']
            self.towards = order['towards']
            self.code = order['code']
            self.user = order['user']
            self.account_cookie = order['account_cookie']
            self.strategy = order['strategy']
            self.type = order['type']
            self.order_model = order['order_model']
            self.amount_model = order['amount_model']
            self.order_id = order['order_id']
            self.trade_id = order['trade_id']
            return self
        except Exception as e:
            QA_util_log_info('Failed to tran from dict')

    def from_dataframe(self, dataframe):
        bid_list = []
        for item in QA_util_to_json_from_pandas(dataframe):
            bid_list.append(self.from_dict(item))
        return bid_list

    def apply(self, order):
        try:
            self.price = order['price']
            self.date = order['date']
            self.datetime = order['datetime']
            self.sending_time = order['sending_time']  # 下单时间
            self.transact_time = order['transact_time']
            self.amount = order['amount']
            self.towards = order['towards']
            self.code = order['code']
            self.user = order['user']
            self.strategy = order['strategy']
            self.account_cookie = order['account_cookie']
            self.type = order['type']
            self.order_model = order['order_model']
            self.amount_model = order['amount_model']
            self.order_id = order['order_id']
            self.trade_id = order['trade_id']
            return self
        except:
            QA_util_log_info('Failed to tran from dict')


class QA_Order_list():   # also the order tree
    """
    一个待成交列表

    """

    def __init__(self, _list=[]):
        self.list = _list
        self.order_queue = queue.Queue()

    def from_dataframe(self, dataframe):
        try:
            self.list = [QA_Order().from_dict(item)
                         for item in QA_util_to_json_from_pandas(dataframe)]
            return self.list
        except:
            pass


if __name__ == '__main__':
    ax = QA_Order().stock_day()

    print(ax.info())
    print(ax.to_df())
