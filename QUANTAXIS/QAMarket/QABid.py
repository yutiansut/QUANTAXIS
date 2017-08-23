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


class QA_QAMarket_bid():
    def __init__(self):
        self.price = 16
        self.date = '2015-01-05'
        self.datetime = '2015-01-05 09:01:00'
        self.sending_time = '2015-01-05 09:01:00'  # 下单时间
        self.transact_time = ''
        self.amount = 10
        self.towards = 1
        self.code = str('000001')
        self.user = 'root'
        self.strategy = 'example01'
        self.status = '0x01'
        self.bid_model = 'strategy'
        self.amount_model = 'amount'
        self.order_id = str(random.random())
        self.trade_id = ''

    def stock_day(self):
        self.status = '0x01'

    def stock_min(self):
        self.status = '0x02'

    def future_day(self):
        self.status = '1x01'


if __name__ == '__main__':
    ax = QA_QAMarket_bid()
    ax.stock_day()
    print(ax.status)
