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

import concurrent
import datetime
import queue
from collections import deque
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event, Timer
from multiprocessing import Process,Pool
import numpy as np
import pandas as pd
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API


from QUANTAXIS.QAUtil.QASetting import info_ip_list
from QUANTAXIS.QAUtil.QADate import QA_util_calc_time
"""
准备做一个多连接的连接池执行器Executor

当持续获取数据/批量数据的时候,可以减小服务器的压力,并且可以更快的进行并行处理

"""


class QA_Tdx_Executor():
    def __init__(self, *args, **kwargs):
        self._queue = queue.LifoQueue(maxsize=200)
        self._api_worker = Thread(
            target=self.api_worker(), args=(), name='API Worker')
        self._api_worker.start()

    def _queue_clean(self):
        self._queue = queue.LifoQueue(maxsize=200)

    def _test_speed(self, ip, port=7709):

        api = TdxHq_API()
        _time = datetime.datetime.now()
        try:
            with api.connect(ip, port, time_out=0.05):
                if len(api.get_security_list(0, 1)) > 800:
                    return (datetime.datetime.now() - _time).total_seconds()
        except:
            return datetime.timedelta(9, 9, 0).total_seconds()

    def get_available(self):

        if self._queue.empty() is False:
            return self._queue.get_nowait()

        else:
            # print('x')
            Timer(0, self.api_worker).start()
            return self._queue.get()

    def api_worker(self):
        data = []

        if self._queue.qsize() < 80:
            for item in info_ip_list:
                _sec = self._test_speed(item)
                if _sec < 0.1:
                    self._queue.put(
                        TdxHq_API(heartbeat=False).connect(ip=item))
        else:
            pass
        Timer(5, self.api_worker).start()


if __name__ == '__main__':
    import time
    x = QA_Tdx_Executor()
    print(x._queue.qsize())
    print(x.get_available())
    for i in range(100):
        # print(threading.enumerate())
        print(x.get_available())
        print('Current Available IP {}'.format(x._queue.qsize()))

        time.sleep(1)
