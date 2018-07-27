import asyncio
import future
import traceback
import time
import datetime
import threading


from QUANTAXIS.QAFetch.QAQuery_Async import QA_fetch_stock_day

l=asyncio.get_event_loop()
z=threading.Thread(target=l.run_forever)

z.start()


data_job=asyncio.run_coroutine_threadsafe(QA_fetch_stock_day('000001','2018-01-01','2018-01-31'),l)



while not data_job.done():
    print('waiting')

    if data_job.done():
        print(data_job.result())
        break

