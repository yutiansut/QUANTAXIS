# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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

import numpy
import pandas as pd
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorCursor)

from QUANTAXIS.QAUtil import (QA_Setting, QA_util_code_tolist,
                              QA_util_date_stamp, QA_util_date_str2int,
                              QA_util_date_valid, QA_util_dict_remove_key,
                              QA_util_log_info,
                              QA_util_sql_mongo_sort_DESCENDING,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse)
from QUANTAXIS.QAUtil.QASetting import DATABASE, DATABASE_ASYNC




async def QA_fetch_stock_day(code, start, end, format='numpy', frequence='day', collections=DATABASE_ASYNC.stock_day):

    '获取股票日线'
    start = str(start)[0:10]
    end = str(end)[0:10]

    # code checking
    code = QA_util_code_tolist(code)

    if QA_util_date_valid(end):

        __data = []
        cursor = collections.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}})
        try:
            res = pd.DataFrame([item async for item in cursor])
        except SyntaxError:
            print('THIS PYTHON VERSION NOT SUPPORT "async for" function')
            pass
        try:
            res = res.drop('_id', axis=1).assign(volume=res.vol).query('volume>1').assign(date=pd.to_datetime(
                res.date, utc=False)).drop_duplicates((['date', 'code'])).set_index('date', drop=False)
            res = res.ix[:, ['code', 'open', 'high', 'low',
                             'close', 'volume', 'amount', 'date']]
        except:
            res = None
        if format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif format in ['json', 'dict']:
            return QA_util_to_json_from_pandas(res)
        # 多种数据格式
        elif format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print("QA Error QA_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        QA_util_log_info(
            'QA Error QA_fetch_stock_day data parameter start=%s end=%s is not right' % (start, end))


async def QA_fetch_stock_min(code, start, end, format='numpy', frequence='1min', collections=DATABASE_ASYNC.stock_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    else:
        print("QA Error QA_fetch_stock_min parameter frequence=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m" % frequence)

    __data = []
    # code checking
    code = QA_util_code_tolist(code)

    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    })

    try:
        res = pd.DataFrame([item async for item in cursor])
    except SyntaxError:
        print('THIS PYTHON VERSION NOT SUPPORT "async for" function')
        pass
    try:
        res = res.drop('_id', axis=1).assign(volume=res.vol).query('volume>1').assign(datetime=pd.to_datetime(
            res.datetime, utc=False)).drop_duplicates(['datetime', 'code']).set_index('datetime', drop=False)
        # return res
    except:
        res = None
    if format in ['P', 'p', 'pandas', 'pd']:
        return res
    elif format in ['json', 'dict']:
        return QA_util_to_json_from_pandas(res)
    # 多种数据格式
    elif format in ['n', 'N', 'numpy']:
        return numpy.asarray(res)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(res).tolist()
    else:
        print("QA Error QA_fetch_stock_min format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
        return None


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    print(id(loop))
    res = loop.run_until_complete(asyncio.gather(
        QA_fetch_stock_day('000001', '2016-07-01', '2018-07-15'),
        QA_fetch_stock_min('000002', '2016-07-01', '2018-07-15')
    ))

    print(res)
