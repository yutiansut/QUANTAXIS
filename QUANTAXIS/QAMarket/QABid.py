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
import threading
import time

from six.moves import queue
from QUANTAXIS.QATask import QA_Queue


"""
重新定义bid模式



"""
class QA_QAMarket_order():
    
    def __init__(self):
        self.strategy_id = ''                 ## 策略ID
        self.account_id = ''                  ## 交易账号

        self.cl_ord_id = ''                   ## 客户端订单ID
        self.order_id = ''                    ## 柜台订单ID
        self.ex_ord_id = ''                   ## 交易所订单ID

        self.exchange = ''                    ## 交易所代码
        self.sec_id = ''                      ## 证券ID

        self.position_effect = 0              ## 开平标志
        self.side = 0                         ## 买卖方向
        self.order_type = 0                   ## 订单类型
        self.order_src = 0                    ## 订单来源
        self.status = 0                       ## 订单状
        self.ord_rej_reason = 0               ## 订单拒绝原因
        self.ord_rej_reason_detail = ''       ## 订单拒绝原因描述

        self.price = 0.0                      ## 委托价
        self.stop_price = 0.0;                ## 止损价
        self.volume = 0.0                     ## 委托量
        self.filled_volume = 0.0              ## 已成交量
        self.filled_vwap = 0.0                ## 已成交均价
        self.filled_amount = 0.0              ## 已成交额

        self.sending_time = 0.0               ## 委托下单时间
        self.transact_time = 0.0              ## 最新一次成交时间


class QA_QAMarket_bid():
    def __init__(self):
        self.bid = {
            'price': float(16),
            'date': str('2015-01-05'),
            'time': str(time.mktime(datetime.datetime.now().timetuple())),
            'amount': int(10),
            'towards': int(1),
            'code': str('000001'),
            'user': str('root'),
            'strategy': str('example01'),
            'status': '0x01',
            'bid_model': 'strategy',
            'amount_model': 'amount',
            'order_id': str(random.random())
        }
        
        # 报价队列  插入/取出/查询
        self.bid_queue = queue.Queue(maxsize=20)

    def QA_bid_insert(self, __bid):
        self.bid_queue.put(__bid)

    def QA_bid_pop(self):
        return self.bid_queue.get()

    def QA_bid_status(self):
        lens = len(self.bid_queue)
        return {'status': lens}


class bid_server(QA_Queue):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def select_market(self, bid):
        pass

    def push_bid(self):

        while self.bid_queue.empty():
            print(self.bid_queue.queue)


if __name__ == '__main__':
    pass
