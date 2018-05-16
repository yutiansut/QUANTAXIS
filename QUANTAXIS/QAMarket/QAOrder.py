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

from QUANTAXIS.QAUtil import (QA_util_log_info, QA_util_random_with_topic,
                              QA_util_to_json_from_pandas)
from QUANTAXIS.QAUtil.QAParameter import AMOUNT_MODEL, ORDER_STATUS


"""
重新定义Order模式

在2017-12-15的Account-remake-version 分支中

Bid类全部被更名为Order类

用于和 bid_ask 区分

by yutiansut@2017/12/15


@2018/1/9
需要重新考虑 order的重复创建耗时问题

order_frame 是一个管理性面板  但是还是需要一个缓存dict

"""


class QA_Order():
    def __init__(self, price=None, date=None, datetime=None, sending_time=None, transact_time=None, amount=None, market_type=None, frequence=None,
                 towards=None, code=None, user=None, account_cookie=None, strategy=None, order_model=None, money=None, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                 order_id=None, trade_id=None, status='100', callback=False, commission_coeff=0.00025, tax_coeff=0.001, *args, **kwargs):
        """委托字段
        price 委托的价格
        date 委托的日期
        datetime 委托的时间
        sending_time 发送委托单的时间
        transact_time 委托成交的时间
        amount 委托量
        market_type 委托的市场
        frequence 频率
        towards 委托方向
        code 委托代码
        user 委托股东
        account_cookie 委托账户的cookie
        strategy 策略名
        order_model 委托方式(限价/市价/下一个bar/)
        amount_model 委托量模式(按量委托/按总成交额委托)
        order_id 委托单id
        trade_id 成交id
        status 订单状态
        callback 回调函数
        """

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
            pass
        self.sending_time = self.datetime if sending_time is None else sending_time  # 下单时间
        self.transact_time = transact_time
        self.amount = amount
        self.towards = towards  # side
        self.code = code
        self.user = user
        self.market_type = market_type
        self.frequence = frequence
        self.account_cookie = account_cookie
        self.strategy = strategy
        self.type = market_type  # see below
        self.order_model = order_model
        self.amount_model = amount_model
        self.order_id = QA_util_random_with_topic(
            topic='Order') if order_id is None else order_id
        self.commission_coeff = commission_coeff
        self.tax_coeff = tax_coeff
        self.trade_id = trade_id
        self.status = status
        self.callback = callback
        self.money = money

    def __repr__(self):
        return '< QA_Order datetime:{} code:{} amount:{} price:{} towards:{} btype:{} order_id:{} account:{} status:{} >'.format(
            self.datetime, self.code, self.amount, self.price, self.towards, self.type, self.order_id, self.account_cookie, self.status)

    def info(self):
        return vars(self)

    def to_df(self):
        return pd.DataFrame([vars(self), ])

    def to_dict(self):
        return vars(self)

    def from_dict(self, order):
        try:
            # QA_util_log_info('QA_ORDER CHANGE: from {} change to {}'.format(
            #     self.order_id, order['order_id']))
            self.price = order['price']
            self.date = order['date']
            self.datetime = order['datetime']
            self.sending_time = order['sending_time']  # 下单时间
            self.transact_time = order['transact_time']
            self.amount = order['amount']
            self.frequence = order['frequence']
            self.market_type = order['market_type']
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
            self.callback = order['callback']
            self.commission_coeff = order['commission_coeff']
            self.tax_coeff = order['tax_coeff']
            return self
        except Exception as e:
            QA_util_log_info('Failed to tran from dict {}'.format(e))


class QA_OrderQueue():   # also the order tree
    """
    一个待成交队列
    这里面都是对于方法的封装

    """

    def __init__(self):
        self.order_list = []
        self.queue = pd.DataFrame()
        self._queue = {}

    def __repr__(self):
        return '< QA_OrderQueue AMOUNT {} WAITING TRADE {} >'.format(len(self.queue), len(self.pending))

    def __call__(self):
        return self.queue

    def _from_dataframe(self, dataframe):
        try:
            self.order_list = [QA_Order().from_dict(item)
                               for item in QA_util_to_json_from_pandas(dataframe)]
            return self.order_list
        except:
            pass

    def insert_order(self, order):
        order.status = ORDER_STATUS.QUEUED
        self.queue = self.queue.append(
            order.to_df(), ignore_index=True)
        self.queue.set_index('order_id', drop=False, inplace=True)
        self._queue[order.order_id] = order
        return order

    @property
    def order_ids(self):
        return self.queue.index

    def settle(self):
        """结算

        清空订单簿
        """
        self.queue = pd.DataFrame()
        self._queue = {}

    @property
    def pending(self):
        """选择待成交列表

        [description]

        Returns:
            dataframe
        """
        try:
            return self.queue.query('status!=200').query('status!=500').query('status!=400')
        except:
            return pd.DataFrame()

    @property
    def trade_list(self):
        """批量交易

        [description]

        Returns:
            list of orders
        """

        return [self._queue[order_id] for order_id in self.pending.index]

    def query_order(self, order_id):

        return self.queue.get(order_id, None)

    def set_status(self, order_id, new_status):
        try:
            if order_id in self.order_ids:
                self.queue.loc[order_id, 'status'] = new_status
                self._queue[order_id].status = new_status
            else:
                pass
        except:
            return None


if __name__ == '__main__':
    ax = QA_Order()

    print(ax.info())
    print(ax.to_df())
