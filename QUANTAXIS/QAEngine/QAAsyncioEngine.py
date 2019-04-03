import asyncio
import datetime
import threading
import time
import traceback

import future

from QUANTAXIS.QAFetch.QAQuery_Async import QA_fetch_stock_day


"""quantaxis 异步引擎


"""


class QAAsync():
    def __init__(self):
        self.event_loop = asyncio.new_event_loop()
        self.elthread = threading.Thread(target=self.event_loop.run_forever)

        self.elthread.setDaemon(True)
        self.elthread.start()

    def run(self, func, callback, *args, **kwargs):
        # schedule a task

        return self.submit(func(*args, **kwargs)).add_done_callback(callback)

    def submit(self, coro):
        """

        future = asyncio.run_coroutine_threadsafe(coro, loop)

        Arguments:
            coro {[type]} -- [description]

        Returns:
            Future -- [description]
        """

        return asyncio.run_coroutine_threadsafe(coro, self.event_loop)
        #self.event_loop.call_soon_threadsafe()


def callback(result):
    r = result
    print(r.result())
    print(type(r))
    print(datetime.datetime.now()-time)
    return r


"""

run_until_complete 

"""


if __name__ == '__main__':
    time = datetime.datetime.now()
    QAE = QAAsync()

    print(datetime.datetime.now()-time)
    QAE.run(QA_fetch_stock_day, callback,
            '000001', '1990-01-01', '2018-01-31')
    QAE.run(QA_fetch_stock_day, callback,
            '000002', '1990-01-01', '2018-01-31')
    QAE.run(QA_fetch_stock_day, callback,
            '000007', '1990-01-01', '2018-01-31')
    QAE.run(QA_fetch_stock_day, callback,
            '000004', '1990-01-01', '2018-01-31')
    QAE.run(QA_fetch_stock_day, callback,
            '000005', '1990-01-01', '2018-01-31')
    print(datetime.datetime.now()-time)