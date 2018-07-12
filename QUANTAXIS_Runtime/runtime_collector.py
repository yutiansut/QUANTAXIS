import datetime
import time

import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
from QUANTAXIS.QAFetch.QATdx_adv import QA_Tdx_Executor
from QUANTAXIS.QAUtil.QADate_trade import QA_util_if_tradetime
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QASql import (QA_util_sql_mongo_sort_ASCENDING,
                                    QA_util_sql_mongo_sort_DESCENDING)

_time1 = datetime.datetime.now()

code = QA_fetch_get_stock_list().code.tolist()
print(len(code))
x = QA_Tdx_Executor()
print(x._queue.qsize())
print(x.get_available())

database = DATABASE.get_collection(
    'realtime_{}'.format(datetime.date.today()))

print(database)
database.create_index([('code', QA_util_sql_mongo_sort_ASCENDING),
                       ('datetime', QA_util_sql_mongo_sort_ASCENDING)])

for i in range(100000):
    _time = datetime.datetime.now()
    if QA_util_if_tradetime(_time):  # 如果在交易时间
        data = x.get_realtime_concurrent(code)

        data[0]['datetime'] = data[1]
        x.save_mongo(data[0])

        print('Time {}'.format(
            (datetime.datetime.now() - _time).total_seconds()))
        time.sleep(1)
        print('Connection Pool NOW LEFT {} Available IP'.format(
            x._queue.qsize()))
        print('Program Last Time {}'.format(
            (datetime.datetime.now() - _time1).total_seconds()))
    else:
        print('Not Trading time {}'.format(_time))
        time.sleep(1)
