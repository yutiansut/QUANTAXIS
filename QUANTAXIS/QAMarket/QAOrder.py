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

import threading
import pandas as pd

from QUANTAXIS.QAUtil import (
    QA_util_log_info, QA_util_random_with_topic, QA_util_to_json_from_pandas)
from QUANTAXIS.QAUtil.QAParameter import AMOUNT_MODEL, ORDER_STATUS


"""
重新定义Order模式

在2017-12-15的Account-remake-version 分支中

Bid类全部被更名为Order类

用于和 bid_ask 区分

by yutiansut@2017/12/15


@2018/1/9
需要重新考虑 order的重复创建耗时问题？

order_frame 是一个管理性面板  但是还是需要一个缓存dict？


@2018/05/25
不建议保存两份变量， 维护起来很麻烦，容易出错。

"""


class QA_Order():
    '''
        记录order
    '''

    def __init__(self, price=None, date=None, datetime=None, sending_time=None, trade_time=False, amount=None, market_type=None, frequence=None,
                 towards=None, code=None, user=None, account_cookie=None, strategy=None, order_model=None, money=None, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                 order_id=None, trade_id=False, _status=ORDER_STATUS.NEW, callback=False, commission_coeff=0.00025, tax_coeff=0.001, *args, **kwargs):
        '''



        QA_Order 对象表示一个委托业务， 有如下字段
        :param price:           委托的价格        type float
        :param date:            委托的日期        type str , eg 2018-11-11
        :param datetime:        委托的时间        type str , eg 2018-11-11 00:00:00
        :param sending_time:    发送委托单的时间   type str , eg 2018-11-11 00:00:00
        :param trade_time:   委托成交的时间
        :param amount:          委托量               type int
        :param trade_amount     成交数量
        :param cancel_amount    撤销数量
        :param market_type:     委托的市场            type str eg 'stock_cn'
        :param frequence:       频率                 type str 'day'
        :param towards:         委托方向              type int
        :param code:            委托代码              type str
        :param user:            委托股东
        :param account_cookie:  委托账户的cookietype          type str eg 'Acc_4UckWFG3'
        :param strategy:        策略名                        type str
        :param order_model:     委托方式(限价/市价/下一个bar/)  type str eg 'limit'
        :param money:           金额                           type float
        :param amount_model:    委托量模式(按量委托/按总成交额委托) type str 'by_amount'
        :param order_id:        委托单id
        :param trade_id:        成交id
        :param _status:          订单状态   type str '100' '200' '300'
        :param callback:        回调函数   type bound method  eg  QA_Account.receive_deal
        :param commission_coeff: 默认 0.00025  type float
        :param tax_coeff:        默认 0.0015  type float
        :param args: type tuple
        :param kwargs: type dict

        # 2018-08-12 把order变成一个状态机>
        # 以前的order只是一个信息承载的工具,现在需要让他具备状态的方法

        NEW = 100
        SUCCESS_ALL = 200
        SUCCESS_PART = 203 # success_part 是部分成交 一个中间状态 剩余的订单还在委托队列中
        QUEUED = 300  # queued 用于表示在order_queue中 实际表达的意思是订单存活 待成交
        CANCEL = 400
        CANCEL_PART = 402 # cancel_part是部分撤单(及 下单后成交了一部分 剩余的被撤单 这是一个最终状态)
        SETTLED = 500
        FAILED = 600
        '''

        self.price = price
        self.datetime = None

        # 🛠todo 移动到 Util 类中 时间处理函数
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

        self.trade_time = trade_time if trade_time else [] # 成交时间
        self.amount = amount  # 委托数量
        self.trade_amount = 0  # 成交数量
        self.cancel_amount = 0  # 撤销数量
        self.towards = towards  # side
        self.code = code  # 委托证券代码
        self.user = user  # 委托用户
        self.market_type = market_type  # 委托市场类别
        self.frequence = frequence  # 委托所在的频率(回测用)
        self.account_cookie = account_cookie
        self.strategy = strategy
        self.type = market_type  # see below
        self.order_model = order_model
        self.amount_model = amount_model
        self.order_id = QA_util_random_with_topic(
            topic='Order') if order_id is None else order_id
        self.realorder_id = self.order_id
        self.commission_coeff = commission_coeff
        self.tax_coeff = tax_coeff
        self.trade_id = trade_id if trade_id else []

        self.trade_price = 0  # 成交均价
        self.callback = callback  # 委托成功的callback
        self.money = money  # 委托需要的金钱
        self.reason = None  # 原因列表

        self._status = _status

    @property
    def pending_amount(self):
        return self.amount-self.cancel_amount-self.trade_amount

    def __repr__(self):
        '''
        输出格式化对象
        :return:  字符串
        '''
        return '< QA_Order realorder_id {} datetime:{} code:{} amount:{} price:{} towards:{} btype:{} order_id:{} account:{} status:{} >'.format(
            self.realorder_id, self.datetime, self.code, self.amount, self.price, self.towards, self.type, self.order_id, self.account_cookie, self.status)

    @property
    def status(self):

        # 以下几个都是最终状态 并且是外部动作导致的
        if self._status in [ORDER_STATUS.FAILED, ORDER_STATUS.NEXT, ORDER_STATUS.SETTLED, ORDER_STATUS.CANCEL_ALL, ORDER_STATUS.CANCEL_PART]:
            return self._status

        if self.pending_amount <= 0:
            self._status = ORDER_STATUS.SUCCESS_ALL
            return self._status
        elif self.pending_amount > 0 and self.trade_amount > 0:
            self._status = ORDER_STATUS.SUCCESS_PART
            return self._status
        elif self.trade_amount == 0:
            self._status = ORDER_STATUS.QUEUED
            return self._status

    def create(self):
        """创建订单
        """
        # 创建一笔订单(未进入委托队列-- 在创建的时候调用)
        self._status = ORDER_STATUS.NEW

    def cancel(self):
        """撤单

        Arguments:
            amount {int} -- 撤单数量
        """

        self.cancel_amount = self.amount - self.trade_amount
        if self.trade_amount == 0:
            # 未交易  直接订单全撤
            self._status = ORDER_STATUS.CANCEL_ALL
        else:
            # 部分交易 剩余订单全撤
            self._status = ORDER_STATUS.CANCEL_PART

    def failed(self, reason=None):
        """失败订单(未成功创建入broker)

        Arguments:
            reason {str} -- 失败原因
        """
        # 订单创建失败(如废单/场外废单/价格高于涨停价/价格低于跌停价/通讯失败)
        self._status = ORDER_STATUS.FAILED
        self.reason = str(reason)

    def trade(self, trade_id, trade_price, trade_amount, trade_time):
        """trade 状态

        Arguments:
            amount {[type]} -- [description]
        """

        trade_amount = int(trade_amount)
        trade_id = str(trade_id)

        if trade_amount < 1:

            self._status = ORDER_STATUS.NEXT
        else:
            if trade_id not in self.trade_id:
                trade_price = float(trade_price)

                trade_time = str(trade_time)

                self.trade_id.append(trade_id)
                self.trade_price = (self.trade_price*self.trade_amount +
                                    trade_price*trade_amount)/(self.trade_amount+trade_amount)
                self.trade_amount += trade_amount
                self.trade_time.append(trade_time)
                self.callback(self.code, trade_id, self.order_id, self.realorder_id,
                              trade_price, trade_amount, self.towards, trade_time)
            else:
                pass

    def queued(self, realorder_id):
        self.realorder_id = realorder_id
        self._status = ORDER_STATUS.QUEUED

    def settle(self):
        self._status = ORDER_STATUS.SETTLED

    def get(self, key, exception=None):
        try:
            if key is None:
                print("key is none , return none!")
                return None
            return eval('self.{}'.format(key))
        except Exception as e:
            return exception
    # 🛠todo 建议取消，直接调用var

    def callingback(self):
        """回调函数

        Returns:
            [type] -- [description]
        """

        if self.callback:
            return self.callback

    def info(self):
        '''
        :return:
        '''
        return vars(self)

    # 对象转变成 dfs
    def to_df(self):
        return pd.DataFrame([vars(self), ])

    # 🛠todo 建议取消，直接调用var？

    def to_dict(self):
        '''
        把对象中的属性转变成字典类型
        :return: dict
        '''
        return vars(self)

    def from_dict(self, order_dict):
        '''
        从字段类型的字段 填充 对象的字段
        :param order_dict:  dict 类型
        :return: self QA_Order
        '''
        try:
            # QA_util_log_info('QA_ORDER CHANGE: from {} change to {}'.format(
            #     self.order_id, order['order_id']))
            self.price = order_dict['price']
            self.date = order_dict['date']
            self.datetime = order_dict['datetime']
            self.sending_time = order_dict['sending_time']  # 下单时间
            self.trade_time = order_dict['trade_time']
            self.amount = order_dict['amount']
            self.frequence = order_dict['frequence']
            self.market_type = order_dict['market_type']
            self.towards = order_dict['towards']
            self.code = order_dict['code']
            self.user = order_dict['user']
            self.account_cookie = order_dict['account_cookie']
            self.strategy = order_dict['strategy']
            self.type = order_dict['type']
            self.order_model = order_dict['order_model']
            self.amount_model = order_dict['amount_model']
            self.order_id = order_dict['order_id']
            self.realorder_id = order_dict['realorder_id']
            self.trade_id = order_dict['trade_id']
            self.callback = order_dict['callback']
            self.commission_coeff = order_dict['commission_coeff']
            self.tax_coeff = order_dict['tax_coeff']

            self.money = order_dict['money']
            self._status = order_dict['_status']

            self.cancel_amount = order_dict['cancel_amount']
            self.trade_amount = order_dict['trade_amount']
            self.trade_price = order_dict['trade_price']
            self.reason = order_dict['reason']

            return self
        except Exception as e:
            QA_util_log_info('Failed to tran from dict {}'.format(e))


class QA_OrderQueue():   # also the order tree ？？ what's the tree means?
    """
    一个待成交队列
    queue是一个dataframe
    这里面都是对于方法的封装
    queue_df 的意图
    对orderqueue进行管理 这是一个dataframe
    然后等到要恢复订单的时候 再去用orderid恢复他
    就好比 你下了个单子
    你就在小本本上记一笔
    然后成交了你打个勾
    撤单了你打个叉
    你看看你还有多少单子在委托你就数数小本子
    这个小本子 就是orderqueue的dataframe
    """

    def __init__(self):
        """重新修改 优化性能

        1. 维护两个dict
           order_list 是一天的所有订单
           deal_list 是历史的成交单(settle以后 , 把order_list append进去)
        """

        self.order_list = {}
        self.deal_list = {}

    def __repr__(self):
        return '<QA_ORDERQueue>'
        # return '< QA_OrderQueue AMOUNT {} WAITING TRADE {} >'.format(len(self.queue_df), len(self.pending))

    def __call__(self):
        return self.order_list

    # def _from_dataframe(self, dataframe):
    #     try:
    #         self.order_list = [QA_Order().from_dict(item)
    #                            for item in QA_util_to_json_from_pandas(dataframe)]
    #         return self.order_list
    #     except:
    #         pass

    def insert_order(self, order):
        '''
        :param order: QA_Order类型
        :return:
        '''
        #print("     *>> QAOrder!insert_order  {}".format(order))
        # QUEUED = 300  # queued 用于表示在order_queue中 实际表达的意思是订单存活 待成交
        #order.status = ORDER_STATUS.QUEUED
        # 🛠 todo 是为了速度快把order对象转换成 df 对象的吗？
        #self.queue_df = self.queue_df.append(order.to_df(), ignore_index=True)
        #self.queue_df.set_index('order_id', drop=True, inplace=True)
        if order is not None:
            self.order_list[order.order_id] = order
            return order
        else:
            print('QAERROR Wrong for get None type while insert order to Queue')

    def update_order(self, order):
        self.order_list[order.order_id] = order

    @property
    def order_ids(self):
        return list(self.order_list.keys())

    @property
    def len(self):
        return len(self.order_list)

    def settle(self):
        """结算
        清空订单簿
        """
        self.deal_list.update(self.order_list)
        self.order_list = {}

    @property
    def pending(self):
        '''
        600 废单 未委托成功
        200 委托成功,完全交易
        203 委托成功,未完全成功
        300 委托队列 待成交
        400 已撤单
        500 服务器撤单/每日结算


        订单生成(100) -- 废单(600)
        订单生成(100) -- 进入待成交队列(300) -- 完全成交(200) -- 每日结算(500)-- 死亡
        订单生成(100) -- 进入待成交队列(300) -- 部分成交(203) -- 未成交(300) -- 每日结算(500) -- 死亡
        订单生成(100) -- 进入待成交队列(300) -- 主动撤单(400) -- 每日结算(500) -- 死亡
        选择待成交列表
        :return: dataframe
        '''
        try:
            return [item for item in self.order_list.values() if item.status in [ORDER_STATUS.QUEUED, ORDER_STATUS.NEXT, ORDER_STATUS.SUCCESS_PART]]
        except:
            return []

    @property
    def failed(self):
        try:
            return [item for item in self.order_list.values() if item.status in [ORDER_STATUS.FAILED]]
        except:
            return []

    @property
    def canceled(self):
        try:
            return [item for item in self.order_list.values() if item.status in [ORDER_STATUS.CANCEL_ALL, ORDER_STATUS.CANCEL_PART]]
        except:
            return []

    @property
    def untrade(self):
        try:
            return [item for item in self.order_list.values() if item.status in [ORDER_STATUS.QUEUED]]
        except:
            return []

    # 🛠todo 订单队列

    def set_status(self, order_id, new_status):
        try:
            if order_id in self.order_ids:

                self.order_list[order_id].status = new_status
            else:
                pass
        except:
            return None


if __name__ == '__main__':
    ax = QA_Order()

    print(ax.info())
    print(ax.to_df())
