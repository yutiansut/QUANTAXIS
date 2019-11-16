# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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
import datetime
import pandas as pd

from QUANTAXIS.QAARP.market_preset import MARKET_PRESET
from QUANTAXIS.QAMarket.common import exchange_code
from QUANTAXIS.QAUtil import (
    QA_util_log_info,
    QA_util_random_with_topic,
    QA_util_to_json_from_pandas
)
from QUANTAXIS.QAUtil.QADate import QA_util_stamp2datetime
from QUANTAXIS.QAUtil.QAParameter import (
    AMOUNT_MODEL,
    MARKET_TYPE,
    ORDER_DIRECTION,
    ORDER_MODEL,
    ORDER_STATUS
)
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

    def __init__(
            self,
            price=None,
            date=None,
            datetime=None,
            sending_time=None,
            trade_time=False,
            amount=0,
            market_type=None,
            frequence=None,
            towards=None,
            code=None,
            user_cookie=None,
            account_cookie=None,
            strategy=None,
            order_model=None,
            money=None,
            amount_model=AMOUNT_MODEL.BY_AMOUNT,
            broker=None,
            order_id=None,
            trade_id=False,
            _status=ORDER_STATUS.NEW,
            callback=False,
            commission_coeff=0.00025,
            tax_coeff=0.001,
            exchange_id=None,
            position_id=None,
            *args,
            **kwargs
    ):
        '''




        QA_Order 对象表示一个委托业务， 有如下字段
        - price 委托价格 (限价单用)
        - date 委托日期 (一般日线级别回测用)
        - datetime 当前时间 (分钟线级别和实时用)
        - sending_time 委托时间 (分钟线级别和实时用)
        - trade_time 成交时间 [list] (分钟/日线/实盘时用, 一笔订单多次成交会不断append进去)
        - amount 委托数量
        - frequence 频率 (回测用 DAY/1min/5min/15min/30min/...)
        - towards 买卖方向
        - code  订单的品种
        - user_cookie  订单发起者
        - account_cookie 订单发起账户的标识
        - stratgy 策略号
        - order_model  委托方式(限价/市价/下一个bar/)  type str eg 'limit'
        - money  订单金额
        - amount_model 委托量模式(按量委托/按总成交额委托) type str 'by_amount'
        - order_id   委托单id
        - trade_id   成交单id
        - _status    内部维护的订单状态
        - callback   当订单状态改变的时候 主动回调的函数(可以理解为自动执行的OnOrderAction)
        - commission_coeff 手续费系数
        - tax_coeff  印花税系数(股票)
        - exchange_id  交易所id (一般用于实盘期货)


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

        self.trade_time = trade_time if trade_time else []  # 成交时间
        self.amount = amount                               # 委托数量
        self.trade_amount = 0                              # 成交数量
        self.cancel_amount = 0                             # 撤销数量
        self.towards = towards                             # side
        self.code = code                                   # 委托证券代码
        self.user_cookie = user_cookie                     # 委托用户
        self.market_type = market_type                     # 委托市场类别
        self.frequence = frequence                         # 委托所在的频率(回测用)
        self.account_cookie = account_cookie
        self.strategy = strategy
        self.type = market_type                            # see below
        self.order_model = order_model
        self.amount_model = amount_model
        self.order_id = QA_util_random_with_topic(
            topic='Order'
        ) if order_id is None else order_id
        self.realorder_id = self.order_id
        self.commission_coeff = commission_coeff
        self.tax_coeff = tax_coeff
        self.trade_id = trade_id if trade_id else []
        self.market_preset = MARKET_PRESET().get_code(self.code)

        self.trade_price = 0                                       # 成交均价
        self.broker = broker
        self.callback = callback                                   # 委托成功的callback
        self.money = money                                         # 委托需要的金钱
        self.reason = None                                         # 原因列表
        self.exchange_id = exchange_id
        self.time_condition = 'GFD'                                # 当日有效
        self._status = _status
        self.exchange_code = exchange_code
        self.position_id = position_id
        # 增加订单对于多账户以及多级别账户的支持 2018/11/12
        self.mainacc_id = None if 'mainacc_id' not in kwargs.keys(
        ) else kwargs['mainacc_id']
        self.subacc_id = None if 'subacc_id' not in kwargs.keys(
        ) else kwargs['subacc_id']
        self.direction = 'BUY' if self.towards in [
            ORDER_DIRECTION.BUY,
            ORDER_DIRECTION.BUY_OPEN,
            ORDER_DIRECTION.BUY_CLOSE
        ] else 'SELL'
        self.offset = 'OPEN' if self.towards in [
            ORDER_DIRECTION.BUY,
            ORDER_DIRECTION.BUY_OPEN,
            ORDER_DIRECTION.SELL_OPEN
        ] else 'CLOSE'

    @property
    def pending_amount(self):
        return self.amount - self.cancel_amount - self.trade_amount

    @property
    def __dict__(self):
        return {
            'price': self.price,
            'datetime': self.datetime,
            'date': self.date,
            'sending_time': self.sending_time,
            'trade_time': self.trade_time,
            'amount': self.amount,
            'trade_amount': self.trade_amount,
            'cancel_amount': self.cancel_amount,
            'towards': self.towards,
            'code': self.code,
            'user_cookie': self.user_cookie,
            'market_type': self.market_type,
            'frequence': self.frequence,
            'account_cookie': self.account_cookie,
            'strategy': self.strategy,
            'type': self.market_type,
            'order_model': self.order_model,
            'amount_model': self.amount_model,
            'order_id': self.order_id,
            'realorder_id': self.realorder_id,
            'commission_coeff': self.commission_coeff,
            'tax_coeff': self.tax_coeff,
            'trade_id': self.trade_id,
            'trade_price': self.trade_price,
            'broker': self.broker,
            'callback': self.callback,
            'money': self.money,
            'reason': self.reason,
            'exchange_id': self.exchange_id,
            'time_condition': self.time_condition,
            '_status': self.status,
            'direction': self.direction,
            'offset': self.offset
        }

    def __repr__(self):
        '''
        输出格式化对象
        :return:  字符串
        '''
        return '< QA_Order realorder_id {} datetime:{} code:{} amount:{} price:{} towards:{} btype:{} order_id:{} account:{} status:{} >'.format(
            self.realorder_id,
            self.datetime,
            self.code,
            self.amount,
            self.price,
            self.towards,
            self.type,
            self.order_id,
            self.account_cookie,
            self.status
        )

    def transform_dt(self, times):
        if isinstance(times, str):
            tradedt = datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S') if len(
                times) == 19 else datetime.datetime.strptime(times, '%Y-%m-%d %H:%M:%S.%f')
            return tradedt.timestamp()*1000000000
        elif isinstance(times, datetime.datetime):
            return tradedt.timestamp()*1000000000

    @property
    def status(self):

        # 以下几个都是最终状态 并且是外部动作导致的
        if self._status in [ORDER_STATUS.FAILED,
                            ORDER_STATUS.NEXT,
                            ORDER_STATUS.SETTLED,
                            ORDER_STATUS.CANCEL_ALL,
                            ORDER_STATUS.CANCEL_PART]:
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

    def calc_commission(self, trade_price, trade_amount):

        if self.market_type == MARKET_TYPE.FUTURE_CN:
            value = trade_price * trade_amount * \
                self.market_preset.get('unit_table', 1)
            if self.towards in [ORDER_DIRECTION.BUY_OPEN,
                                ORDER_DIRECTION.BUY_CLOSE,
                                ORDER_DIRECTION.SELL_CLOSE,
                                ORDER_DIRECTION.SELL_OPEN]:
                commission_fee = self.market_preset['commission_coeff_pervol'] * trade_amount + \
                    self.market_preset['commission_coeff_peramount'] * \
                    abs(value)
            elif self.towards in [ORDER_DIRECTION.BUY_CLOSETODAY,
                                  ORDER_DIRECTION.SELL_CLOSETODAY]:
                commission_fee = self.market_preset['commission_coeff_today_pervol'] * trade_amount + \
                    self.market_preset['commission_coeff_today_peramount'] * \
                    abs(value)
            return commission_fee
        elif self.market_type == MARKET_TYPE.STOCK_CN:
            commission_fee = trade_price * trade_amount * self.commission_coeff

            return max(commission_fee, 5)

    def get_exchange(self, code):
        return self.exchange_code.get(code.lower(), 'Unknown')

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
        if self.status in [ORDER_STATUS.SUCCESS_PART, ORDER_STATUS.QUEUED]:
            trade_amount = int(trade_amount)
            trade_id = str(trade_id)

            if trade_amount < 1:

                self._status = ORDER_STATUS.NEXT
                return False
            else:
                if trade_id not in self.trade_id:
                    trade_price = float(trade_price)

                    trade_time = str(trade_time)

                    self.trade_id.append(trade_id)
                    self.trade_price = (
                        self.trade_price * self.trade_amount +
                        trade_price * trade_amount
                    ) / (
                        self.trade_amount + trade_amount
                    )
                    self.trade_amount += trade_amount
                    self.trade_time.append(trade_time)
                    res = self.callback(
                        self.code,
                        trade_id,
                        self.order_id,
                        self.realorder_id,
                        trade_price,
                        trade_amount,
                        self.towards,
                        trade_time
                    )
                    if res == 0:
                        return self.trade_message(
                            trade_id,
                            trade_price,
                            trade_amount,
                            trade_time
                        )
                    else:
                        return False
                else:
                    return False
        else:
            print(
                RuntimeError(
                    'ORDER STATUS {} CANNNOT TRADE'.format(self.status)
                )
            )
            return False

    def trade_message(self, trade_id, trade_price, trade_amount, trade_time):
        return {
            "user_id": self.account_cookie,  # //用户ID
            "order_id": self.order_id,  # //交易所单号
            "trade_id": trade_id,  # //委托单ID, 对于一个USER, trade_id 是永远不重复的
            "exchange_id": self.exchange_id,  # //交易所
            "instrument_id": self.code,  # //在交易所中的合约代码
            "exchange_trade_id": trade_id,  # //交易所单号
            "direction": self.direction,  # //下单方向
            "offset": self.offset,  # //开平标志
            "volume": trade_amount,  # //成交手数
            "price": trade_price,  # //成交价格
            "trade_date_time":  trade_time,  # //成交时间, epoch nano
            # //成交手续费
            "commission": self.calc_commission(trade_price, trade_amount),
            "seqno": ''}

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
        return pd.DataFrame([
            vars(self),
        ])

    # 🛠todo 建议取消，直接调用var？

    def to_dict(self):
        '''
        把对象中的属性转变成字典类型
        :return: dict
        '''
        return vars(self)

    def to_otgdict(self):
        """{
                "aid": "insert_order",                  # //必填, 下单请求
                # //必填, 需要与登录用户名一致, 或为登录用户的子账户(例如登录用户为user1, 则报单 user_id 应当为 user1 或 user1.some_unit)
                "user_id": account_cookie,
                # //必填, 委托单号, 需确保在一个账号中不重复, 限长512字节
                "order_id": order_id if order_id else QA.QA_util_random_with_topic('QAOTG'),
                "exchange_id": exchange_id,  # //必填, 下单到哪个交易所
                "instrument_id": code,               # //必填, 下单合约代码
                "direction": order_direction,                      # //必填, 下单买卖方向
                # //必填, 下单开平方向, 仅当指令相关对象不支持开平机制(例如股票)时可不填写此字段
                "offset":  order_offset,
                "volume":  volume,                             # //必填, 下单手数
                "price_type": "LIMIT",  # //必填, 报单价格类型
                "limit_price": price,  # //当 price_type == LIMIT 时需要填写此字段, 报单价格
                "volume_condition": "ANY",
                "time_condition": "GFD",
            }
        """
        return {
            "aid": "insert_order",                  # //必填, 下单请求
            # //必填, 需要与登录用户名一致, 或为登录用户的子账户(例如登录用户为user1, 则报单 user_id 应当为 user1 或 user1.some_unit)
            "user_id": self.account_cookie,
            # //必填, 委托单号, 需确保在一个账号中不重复, 限长512字节
            "order_id": self.order_id,
            "exchange_id": self.exchange_id,  # //必填, 下单到哪个交易所
            "instrument_id": self.code,               # //必填, 下单合约代码
            "direction": self.direction,                      # //必填, 下单买卖方向
            # //必填, 下单开平方向, 仅当指令相关对象不支持开平机制(例如股票)时可不填写此字段
            "offset":  self.offset,
            "volume":  self.amount,                             # //必填, 下单手数
            "price_type": self.order_model,  # //必填, 报单价格类型
            "limit_price": self.price,  # //当 price_type == LIMIT 时需要填写此字段, 报单价格
            "volume_condition": "ANY",
            "time_condition": "GFD",
        }

    def to_qatradegatway(self):
        """[summary]
        {'topic': 'sendorder', 
        'account_cookie': '100004', 
        'strategy_id': None, 
        'order_direction': 'SELL', 
        'order_offset': 'OPEN', 
        'code': 'rb1910', 
        'price': 3745.0, 
        'order_time': '2019-05-08 13:55:38.000000', 
        'exchange_id': 'SHFE', 
        'volume': 1.0, 
        'order_id': '5ab55219-adf6-432f-90db-f1bc5f29f4e5'}


        'topic': 'sendorder',
        'account_cookie': acc,
        'strategy_id': 'test',
        'code': code,
        'price': price[code],
        'order_direction': 'SELL',
        'order_offset': 'CLOSE',
        'volume': 1,
        'order_time': str(datetime.datetime.now()),
        'exchange_id': 'SHFE'
        """
        return {
            'topic': 'sendorder',
            'account_cookie': self.account_cookie,
            'strategy_id': self.strategy,
            'order_direction': self.direction,
            'order_offset': self.offset,
            'code': self.code.lower(),
            'price': self.price,
            'order_time': self.sending_time,
            'exchange_id': self.get_exchange(self.code),
            'volume': int(self.amount),
            'order_id': self.order_id
        }

    def to_qifi(self):

        return {
            "account_cookie": self.account_cookie,
            "user_id": self.account_cookie,
            "instrument_id": self.code,
            "towards": self.towards,
            "exchange_id": self.exchange_id,
            "order_time": self.datetime,
            "volume": self.amount,
            "price": self.price,
            "order_id": self.order_id,
            "seqno": 1,
            "direction": self.direction,                      # //
            "offset": self.offset,  # //
            "volume_orign": self.amount,
            "price_type": self.order_model,
            "limit_price": self.price,
            "time_condition": "GFD",
            "volume_condition": "ANY",
            "insert_date_time": self.transform_dt(self.datetime),
            "exchange_order_id": self.realorder_id,
            "status": self.status,
            "volume_left": self.pending_amount,
            "last_msg": "",
            "topic": "send_order"
        }

    def from_otgformat(self, otgOrder):
        """[summary]

        Arguments:
            otgOrder {[type]} -- [description]


        {'seqno': 6,
        'user_id': '106184',
        'order_id': 'WDRB_QA01_FtNlyBem',
        'exchange_id': 'SHFE',
        'instrument_id': 'rb1905',
        'direction': 'SELL',
        'offset': 'OPEN',
        'volume_orign': 50, #(总报单手数)
        'price_type': 'LIMIT', # "LIMIT" (价格类型, ANY=市价, LIMIT=限价)
        'limit_price': 3432.0, # 4500.0 (委托价格, 仅当 price_type = LIMIT 时有效)
        'time_condition': 'GFD',#  "GFD" (时间条件, IOC=立即完成，否则撤销, GFS=本节有效, GFD=当日有效, GTC=撤销前有效, GFA=集合竞价有效)
        'volume_condition': 'ANY', # "ANY" (手数条件, ANY=任何数量, MIN=最小数量, ALL=全部数量)
        'insert_date_time': 1545656460000000000,# 1501074872000000000 (下单时间(按北京时间)，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数)
        'exchange_order_id': '        3738',
        'status': 'FINISHED', # "ALIVE" (委托单状态, ALIVE=有效, FINISHED=已完)
        'volume_left': 0,
        'last_msg': '全部成交报单已提交'} # "报单成功" (委托单状态信息)
        """
        self.order_id = otgOrder.get('order_id')
        self.account_cookie = otgOrder.get('user_id')
        self.exchange_id = otgOrder.get('exchange_id')
        self.code = str(otgOrder.get('instrument_id')).upper()
        self.offset = otgOrder.get('offset')
        self.direction = otgOrder.get('direction')
        self.towards = eval(
            'ORDER_DIRECTION.{}_{}'.format(self.direction,
                                           self.offset)
        )
        self.amount = otgOrder.get('volume_orign')
        self.trade_amount = self.amount - otgOrder.get('volume_left')
        self.price = otgOrder.get('limit_price')
        self.order_model = eval(
            'ORDER_MODEL.{}'.format(otgOrder.get('price_type'))
        )
        self.time_condition = otgOrder.get('time_condition')
        if otgOrder.get('insert_date_time') == 0:
            self.datetime = 0
        else:
            self.datetime = QA_util_stamp2datetime(
                int(otgOrder.get('insert_date_time'))
            )
        self.sending_time = self.datetime
        self.volume_condition = otgOrder.get('volume_condition')
        self.message = otgOrder.get('last_msg')

        self._status = ORDER_STATUS.NEW
        if '拒绝' in self.message or '仓位不足' in self.message:
            # 仓位不足:  一般是平今/平昨仓位不足
            self._status = ORDER_STATUS.FAILED
        if '已撤单' in self.message:
            self._status = ORDER_STATUS.CANCEL_ALL
        self.realorder_id = otgOrder.get('exchange_order_id')
        return self

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
            self.user_cookie = order_dict['user_cookie']
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


class QA_OrderQueue():  # also the order tree ？？ what's the tree means?
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
        return '< QA_OrderQueue >'
        # return '< QA_OrderQueue AMOUNT {} WAITING TRADE {} >'.format(len(self.queue_df), len(self.pending))

    def __call__(self):
        return self.order_list

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
        if self.order_list[order.order_id].status != order.status:
            self.order_list[order.order_id] = order
            return True
        else:
            if self.order_list[order.order_id
                               ].trade_amount != order.trade_amount:
                slef.order_list[order.order_id] = order
                return True
            else:
                return False

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
            return [
                item for item in self.order_list.values() if item.status in [
                    ORDER_STATUS.QUEUED,
                    ORDER_STATUS.NEXT,
                    ORDER_STATUS.SUCCESS_PART
                ]
            ]
        except:
            return []

    @property
    def failed(self):
        try:
            return [
                item for item in self.order_list.values()
                if item.status in [ORDER_STATUS.FAILED]
            ]
        except:
            return []

    @property
    def canceled(self):
        try:
            return [
                item for item in self.order_list.values() if item.status in
                [ORDER_STATUS.CANCEL_ALL,
                 ORDER_STATUS.CANCEL_PART]
            ]
        except:
            return []

    @property
    def untrade(self):
        try:
            return [
                item for item in self.order_list.values()
                if item.status in [ORDER_STATUS.QUEUED]
            ]
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

    def to_df(self):
        try:
            return pd.concat([x.to_df() for x in self.order_list.values()])
        except:
            pass

    @property
    def order_qifi(self):
        return dict(zip(self.order_list.keys(), [item.to_qifi() for item in self.order_list.values()]))


if __name__ == '__main__':
    ax = QA_Order()

    print(ax.info())
    print(ax.to_df())
