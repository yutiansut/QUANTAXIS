import datetime

import pandas as pd
from pandas import DataFrame

from QUANTAXIS.QAData import (QA_data_make_hfq, QA_data_make_qfq,
                              QA_DataStruct_Index_day, QA_DataStruct_Index_min,
                              QA_DataStruct_Stock_block,
                              QA_DataStruct_Stock_day, QA_DataStruct_Stock_min,
                              QA_DataStruct_Stock_transaction)
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_indexlist_day,
                                       QA_fetch_stocklist_day,
                                       QA_fetch_stocklist_min)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_log_info,
                              QA_util_time_stamp)
from QUANTAXIS.QAUtil import QA_util_sql_async_mongo_setting
import asyncio
data = []


"""
获取数据的部分做原子化处理


IO密集/网络密集型---- 异步并发
计算密集型  ---- 批量集中处理 单线程
"""


class worker:
    def __init__(self, *args, **kwargs):
        self.job = {}

    @asyncio.coroutine()
    def worker(self, work):
        yield


class pipeline:
    def __init__(self, *args, **kwargs):
        pass


class processor():
    def __init__(self, *args, **kwargs):
        pass


async def QA_fetch_stock_day_adv(code, __start, __end,
                                 if_drop_index=False,
                                 collections=QA_util_sql_async_mongo_setting().quantaxis.stock_day):
    '获取股票日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    data = [[str(item['code']), float(item['open']), float(item['high']), float(
        item['low']), float(item['close']), float(item['vol']), item['date']] async for item in collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": QA_util_date_stamp(__end),
                "$gte": QA_util_date_stamp(__start)}})]


loop = asyncio.get_event_loop()
# task=asyncio.ensure_future(QA_fetch_stock_day_adv(['000001','000002','000004','000007'],'2017-01-01','2017-07-31'))
"""
event = [asyncio.ensure_future(QA_fetch_stock_day_adv(
    _code, '2017-01-01', '2017-07-31')) for _code in ['000001', '000002', '000004', '000007']]
loop.run_until_complete(event)
print(data)


    __data = DataFrame(__data, columns=[
        'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
    __data['date'] = pd.to_datetime(__data['date'])
    data.extend(QA_DataStruct_Stock_day(__data.query(
        'volume>1').set_index(['date', 'code'], drop=if_drop_index)))
loop.stop()
"""

event = asyncio.ensure_future(QA_fetch_stock_day_adv(
    '000001', '2017-01-01', '2017-07-31'))
loop.run_until_complete(asyncio.wait([event]))
print(data)
