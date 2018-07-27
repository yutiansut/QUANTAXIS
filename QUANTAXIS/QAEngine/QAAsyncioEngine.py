import asyncio
import datetime
import threading
import time
import traceback

import future

from QUANTAXIS.QAFetch.QAQuery_Async import QA_fetch_stock_day


class QAAsync():
    def __init__(self):
        self.event_loop = asyncio.get_event_loop()
        self.elthread = threading.Thread(target=self.event_loop.run_forever)

        self.elthread.setDaemon(True)
        self.elthread.start()

    def submit(self,func,*args,**kwargs):
        self.job=asyncio.run_coroutine_threadsafe(func(*args,**kwargs),self.event_loop)
        self.callback()

    def callback(self):
        print(self.job.result(7))


QAE=QAAsync()
QAE.submit(QA_fetch_stock_day,'000001','2018-01-01', '2018-01-31')
