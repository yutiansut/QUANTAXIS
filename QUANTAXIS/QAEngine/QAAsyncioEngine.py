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
        r=self.job.result(0.05)
        print(len(r))


QAE=QAAsync()

time=datetime.datetime.now()
QAE.submit(QA_fetch_stock_day,'000001','2018-01-01', '2018-01-31')
QAE.submit(QA_fetch_stock_day,'000003','2018-01-01', '2018-01-31')
QAE.submit(QA_fetch_stock_day,'000007','2018-01-01', '2018-01-31')
QAE.submit(QA_fetch_stock_day,'000004','2018-01-01', '2018-01-31')
QAE.submit(QA_fetch_stock_day,'000005','2018-01-01', '2018-01-31')
print(datetime.datetime.now()-time)

import QUANTAXIS as QA
time=datetime.datetime.now()
r=QA.QA_fetch_stock_day('000008','2018-01-01', '2018-01-31')
print(len(r))
print(datetime.datetime.now()-time)
r=QA.QA_fetch_stock_day('000009','2018-01-01', '2018-01-31')
print(len(r))
r=QA.QA_fetch_stock_day('600000','2018-01-01', '2018-01-31')
print(len(r))
r=QA.QA_fetch_stock_day('600014','2018-01-01', '2018-01-31')
print(len(r))
r=QA.QA_fetch_stock_day('600010','2018-01-01', '2018-01-31')
print(len(r))
print(datetime.datetime.now()-time)
