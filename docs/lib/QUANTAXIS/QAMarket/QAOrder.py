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

from QUANTAXIS.QAUtil import (QA_util_log_info, QA_util_random_with_topic,QA_util_to_json_from_pandas)
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
    def __init__(self, price=None , date=None, datetime=None, sending_time=None, transact_time=None, amount=None, market_type=None, frequence=None,
                 towards=None, code=None, user=None, account_cookie=None, strategy=None, order_model=None, money=None, amount_model=AMOUNT_MODEL.BY_AMOUNT,
                 order_id=None, trade_id=None, status='100', callback=False, commission_coeff=0.00025, tax_coeff=0.001, *args, **kwargs):
        '''
        QA_Order 对象表示一个委托业务， 有如下字段
        :param price:           委托的价格        type float
        :param date:            委托的日期        type str , eg 2018-11-11
        :param datetime:        委托的时间        type str , eg 2018-11-11 00:00:00
        :param sending_time:    发送委托单的时间   type str , eg 2018-11-11 00:00:00
        :param transact_time:   委托成交的时间
        :param amount:          委托量               type int
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
        :param status:          订单状态   type str '100' '200' '300'
        :param callback:        回调函数   type bound method  eg  QA_Account.receive_deal
        :param commission_coeff: 默认 0.00025  type float
        :param tax_coeff:        默认 0.0015  type float
        :param args: type tuple
        :param kwargs: type dict
        '''

        self.price = price
        self.datetime = None

        #🛠todo 移动到 Util 类中 时间处理函数
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
        '''
        输出格式化对象
        :return:  字符串
        '''
        return '< QA_Order datetime:{} code:{} amount:{} price:{} towards:{} btype:{} order_id:{} account:{} status:{} >'.format(
            self.datetime, self.code, self.amount, self.price, self.towards, self.type, self.order_id, self.account_cookie, self.status)

    #🛠todo 建议取消，直接调用var
    def info(self):
        '''
        :return:
        '''
        return vars(self)

    #对象转变成 dfs
    def to_df(self):
        return pd.DataFrame([vars(self), ])


    #🛠todo 建议取消，直接调用var？
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
            self.transact_time = order_dict['transact_time']
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
            self.trade_id = order_dict['trade_id']
            self.callback = order_dict['callback']
            self.commission_coeff = order_dict['commission_coeff']
            self.tax_coeff = order_dict['tax_coeff']

            self.money = order_dict['money']
            self.status = order_dict['status']

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

        self.order_list = []

        #🛠 todo 是为了速度快把order对象转换成 df 对象的吗？
        #🛠 todo 维护两个变量queue，代价很大
        #🛠 todo 建议直接保存 QA_Order， 速度慢？
        self.queue_df = pd.DataFrame()
        self._queue_dict = {}

    def __repr__(self):
        return '< QA_OrderQueue AMOUNT {} WAITING TRADE {} >'.format(len(self.queue_df), len(self.pending))

    def __call__(self):
        return self.queue_df

    def _from_dataframe(self, dataframe):
        try:
            self.order_list = [QA_Order().from_dict(item) for item in QA_util_to_json_from_pandas(dataframe)]
            return self.order_list
        except:
            pass

    def insert_order(self, order):
        '''
        :param order: QA_Order类型
        :return:
        '''
        #print("     *>> QAOrder!insert_order  {}".format(order))
        order.status = ORDER_STATUS.QUEUED #    QUEUED = 300  # queued 用于表示在order_queue中 实际表达的意思是订单存活 待成交
        #🛠 todo 是为了速度快把order对象转换成 df 对象的吗？
        self.queue_df = self.queue_df.append(order.to_df(), ignore_index=True)
        self.queue_df.set_index('order_id', drop=False, inplace=True)
        self._queue_dict[order.order_id] = order
        return order

    @property
    def order_ids(self):
        return self.queue_df.index

    def settle(self):
        """结算
        清空订单簿
        """
        self.queue_df = pd.DataFrame()
        self._queue_dict = {}

    @property
    def pending(self):
        '''
        200 委托成功,完全交易
        203 委托成功,未完全成功
        300 刚创建订单的时候
        400 已撤单
        500 服务器撤单/每日结算
        订单生成(100) -- 进入待成交队列(300) -- 完全成交(200) -- 每日结算(500)-- 死亡
        订单生成(100) -- 进入待成交队列(300) -- 部分成交(203) -- 未成交(300) -- 每日结算(500) -- 死亡
        订单生成(100) -- 进入待成交队列(300) -- 主动撤单(400) -- 每日结算(500) -- 死亡
        选择待成交列表
        :return: dataframe
        '''
        try:
            return self.queue_df.query('status!=200').query('status!=500').query('status!=400')
        except:
            return pd.DataFrame()

    @property
    def trade_list(self):
        '''
        批量交易
        :return:
        '''
        return [self._queue_dict[order_id] for order_id in self.pending.index]


    def query_order(self, order_id):
        '''
        @modified by JerryW 2018/05/25
        根据 order_id 查询队列中的记录， 并且转换成 order 对象
        :param order_id:  str 类型 Order_开头的随机数  eg：Order_KQymhXWu
        :return QA_Order类型:
        '''
        anOrderRec = self.queue_df.loc[[order_id]]
        rec_dict = anOrderRec.to_dict('records')
        anOrderObj = QA_Order()
        anOrderObj.from_dict(rec_dict[0])
        return anOrderObj

    #🛠todo 订单队列
    def set_status(self, order_id, new_status):
        try:
            if order_id in self.order_ids:
                self.queue_df.loc[order_id, 'status'] = new_status
                self._queue_dict[order_id].status = new_status
            else:
                pass
        except:
            return None


if __name__ == '__main__':
    ax = QA_Order()

    print(ax.info())
    print(ax.to_df())
