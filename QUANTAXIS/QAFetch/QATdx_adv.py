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

import asyncio
import concurrent
import datetime
import logging
import queue
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Process
from threading import Event, Thread, Timer

import numpy as np
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient

from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API
from QUANTAXIS.QAUtil.QADate import QA_util_calc_time
from QUANTAXIS.QAUtil.QASetting import info_ip_list


"""
准备做一个多连接的连接池执行器Executor

当持续获取数据/批量数据的时候,可以减小服务器的压力,并且可以更快的进行并行处理

"""


class QA_Tdx_Executor():
    def __init__(self, *args, **kwargs):
        self._queue = queue.Queue(maxsize=200)
        self.api_no_connection = TdxHq_API()
        self._api_worker = Thread(
            target=self.api_worker, args=(), name='API Worker')
        self._api_worker.start()

    def _queue_clean(self):
        self._queue = queue.Queue(maxsize=200)

    def _test_speed(self, ip, port=7709):
        
        api = TdxHq_API(raise_exception=True, auto_retry=False)
        #api.need_setup = False
        _time = datetime.datetime.now()
        try:
            with api.connect(ip, port, time_out=0.05):
                if len(api.get_security_list(0, 1)) > 800:
                    return (datetime.datetime.now() - _time).total_seconds()
                else:
                    return datetime.timedelta(9, 9, 0).total_seconds()
        except Exception as e:
            #print('BAD IP {}, DEL for Reason{}'.format(ip,e))
            return datetime.timedelta(9, 9, 0).total_seconds()

    @property
    def ipsize(self):
        return len(self._queue.qsize())

    @property
    def api(self):
        return self.get_available()


    def get_available(self):

        if self._queue.empty() is False:
            return self._queue.get_nowait()
        else:
            Timer(0, self.api_worker).start()
            return self._queue.get()

    def api_worker(self):
        data = []
        if self._queue.qsize() < 80:
            for item in info_ip_list:
                _sec = self._test_speed(item)
                if _sec < 0.1:
                    self._queue.put(
                        TdxHq_API(heartbeat=False).connect(ip=item, time_out=0.05))
        else:
            self._queue_clean()
            Timer(0, self.api_worker).start()
        Timer(300, self.api_worker).start()

    def singal_job(self, context, id_, time_out=0.5):
        try:
            _api = self.get_available()

            __data = context.append(self.api_no_connection.to_df(_api.get_security_quotes(
                [(self._select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
            self._queue.put(_api)  # 加入注销
            return __data
        except:
            return self.singal_job(context, id_)

    def get_realtime(self, code):
        context = pd.DataFrame()

        code = [code] if type(code) is str else code
        try:
            for id_ in range(int(len(code) / 80) + 1):
                context = self.singal_job(context, id_)

            data = context[['datetime', 'code', 'open', 'high', 'low', 'price', 'ask1', 'ask_vol1',
                            'ask2', 'ask_vol2', 'ask3', 'ask_vol3', 'ask4', 'ask_vol4', 'ask5', 'ask_vol5']]
            return data.set_index('code', drop=False, inplace=False)
        except:
            return None

    def _select_market_code(self, code):
        code = str(code)
        if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
            return 1
        return 0


    def save_mongo(self):
        pass


if __name__ == '__main__':
    import time
    _time1 = datetime.datetime.now()
    from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_block_adv
    code = QA_fetch_stock_block_adv().code
    x = QA_Tdx_Executor()
    print(x._queue.qsize())
    print(x.get_available())
    for i in range(100000):
        _time = datetime.datetime.now()
        data = x.get_realtime(code)
        if data is not None:
            print(len(data))
        print('Time {}'.format((datetime.datetime.now() - _time).total_seconds()))
        time.sleep(1)
        print('Connection Pool NOW LEFT {} Available IP'.format(x._queue.qsize()))
        print('Program Last Time {}'.format(
            (datetime.datetime.now() - _time1).total_seconds()))
        # print(threading.enumerate())
