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




class bid_server(QA_QAMarket_bid):

    def __check_status(self):
        pass

    def dispath_center(self, __event):

        assert __event.type == 'bid'
        l = threading.Thread(target=self.do_job)
        l.start()
        l.join()

    def __check_type(self):
        pass

    def do_job(self):

        while self.bid_queue.empty():
            print(self.bid_queue.queue)


"""
所有的报价系统是独立的,每个回测框架模块都会继承一个报价模块

报价模块需要高度解耦,并在事件驱动的 位置上能够高度自定义

需要能同时接受不同频率的报价以及不同市场的报价

在这些事件未完成之前,bid的报价系统不能停止


好比: 

框架会设立一个status值,在status没有被false之前,bid是需要一直被检查和分发的


"""
if __name__ == '__main__':
    bs = bid_server()
    # try to start a new bid server
