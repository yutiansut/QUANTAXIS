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

from six.moves import queue


"""
重新定义bid模式



"""


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
