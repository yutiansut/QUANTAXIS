# coding: utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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
import re
import pymongo
import pandas as pd
from pandas import DataFrame

from QUANTAXIS.QAData import (QA_DataStruct_Index_day, QA_DataStruct_Index_min,
                              QA_DataStruct_Stock_block,
                              QA_DataStruct_Stock_day, QA_DataStruct_Stock_min,
                              QA_DataStruct_Stock_transaction)
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_indexlist_day,
                                       QA_fetch_stock_full,
                                       QA_fetch_stocklist_day,
                                       QA_fetch_stocklist_min)
from QUANTAXIS.QAUtil import (DATABASE, QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_log_info,
                              QA_util_time_stamp)

"""
按要求从数据库取数据，并转换成numpy结构

"""
# start='1990-01-01',end=str(datetime.date.today())


def QA_fetch_stock_day_adv(
        code,
        start='all', end=None,
        if_drop_index=False,
        collections=DATABASE.stock_day):
    '获取股票日线'
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    if start == 'all':
        start = '1990-01-01'
        end = str(datetime.date.today())

    if isinstance(code, str):
        if QA_util_date_valid(end) == True:
            __data = []
            for item in collections.find({
                'code': str(code)[0:6], "date_stamp": {
                    "$lte": QA_util_date_stamp(end),
                    "$gte": QA_util_date_stamp(start)}}):
                __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                    item['low']), float(item['close']), float(item['vol']), float(item['amount']), item['date']])
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'amount', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            return QA_DataStruct_Stock_day(__data.query('volume>1').set_index(['date', 'code'], drop=if_drop_index).sort_index())
        else:
            QA_util_log_info('something wrong with date')
    elif isinstance(code, list):
        return QA_DataStruct_Stock_day(pd.concat(QA_fetch_stocklist_day(code, [start, end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))
        #print([Greenlet.get(item).data for item in gevent.joinall([gevent.spawn(QA_fetch_stock_day_adv,_code,start,end,if_drop_index) for _code in code])])
        # return QA_DataStruct_Stock_day(pd.concat([Greenlet.get(item).data for item in gevent.joinall([gevent.spawn(QA_fetch_stock_day_adv,_code,start,end,if_drop_index) for _code in code])]).set_index(['date', 'code'], drop=if_drop_index))


def QA_fetch_stocklist_day_adv(
        code,
        start='all', end=None,
        if_drop_index=False,
        collections=DATABASE.stock_day):
    '获取股票日线'

    if start == 'all':
        start = '1990-01-01'
        end = str(datetime.date.today())
    return QA_DataStruct_Stock_day(pd.concat(QA_fetch_stocklist_day(code, [start, end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index).sort_index())


def QA_fetch_stock_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=False,
        collections=DATABASE.stock_min):
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
    __data = []

    end = start if end is None else end
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)
    if len(end) == 10:
        end = '{} 15:00:00'.format(end)
    if isinstance(code, str):

        for item in collections.find({
            'code': str(code), "time_stamp": {
                "$gte": QA_util_time_stamp(start),
                "$lte": QA_util_time_stamp(end)
            }, 'type': frequence
        }):

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

        __data = DataFrame(__data, columns=[
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

        __data['datetime'] = pd.to_datetime(__data['datetime'])
        return QA_DataStruct_Stock_min(__data.query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))
    elif isinstance(code, list):
        '新增codelist的代码'
        return QA_DataStruct_Stock_min(pd.concat([QA_fetch_stock_min_adv(code_, start, end, frequence, if_drop_index).data for code_ in code]).set_index(['datetime', 'code'], drop=if_drop_index).sort_index())


def QA_fetch_stocklist_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=False,  collections=DATABASE.stock_min):
    return QA_DataStruct_Stock_min(pd.concat(QA_fetch_stocklist_min(code, [start, end], frequence)).query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index).sort_index())


def QA_fetch_stock_day_full_adv(date):
    '返回全市场某一天的数据'
    return QA_DataStruct_Stock_day(QA_fetch_stock_full(date, 'pd').set_index(['date', 'code'], drop=False))


def QA_fetch_index_day_adv(
        code,
        start, end=None,
        if_drop_index=False,
        collections=DATABASE.index_day):
    '获取指数日线'
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]
    if isinstance(code, str):
        if QA_util_date_valid(end) == True:
            __data = []
            for item in collections.find({
                'code': str(code)[0:6], "date_stamp": {
                    "$lte": QA_util_date_stamp(end),
                    "$gte": QA_util_date_stamp(start)}}):
                __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                    item['low']), float(item['close']), float(item['vol']), item['date']])
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            return QA_DataStruct_Index_day(__data.query('volume>1').set_index(['date', 'code'], drop=if_drop_index).sort_index())
        else:
            QA_util_log_info('something wrong with date')

    elif isinstance(code, list):
        return QA_DataStruct_Index_day(pd.concat(QA_fetch_indexlist_day(code, [start, end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index).sort_index())


def QA_fetch_index_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=False,
        collections=DATABASE.index_min):
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
    __data = []
    end = start if end is None else end
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)
    if len(end) == 10:
        end = '{} 15:00:00'.format(end)
    if isinstance(code, str):
        for item in collections.find({
            'code': str(code), "time_stamp": {
                "$gte": QA_util_time_stamp(start),
                "$lte": QA_util_time_stamp(end)
            }, 'type': frequence
        }):

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

        __data = DataFrame(__data, columns=[
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

        __data['datetime'] = pd.to_datetime(__data['datetime'])
        return QA_DataStruct_Index_min(__data.query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index).sort_index())

    elif isinstance(code, list):
        return QA_DataStruct_Index_min(pd.concat([QA_fetch_index_min_adv(code_, start, end, frequence, if_drop_index).data for code_ in code]).set_index(['datetime', 'code'], drop=if_drop_index).sort_index())


def QA_fetch_stock_transaction_adv(
        code,
        start, end=None,
        if_drop_index=False,
        collections=DATABASE.stock_transaction):
    end = start if end is None else end
    data = DataFrame([item for item in collections.find({
        'code': str(code), "date": {
            "$gte": start,
            "$lte": end
        }})])

    data['datetime'] = pd.to_datetime(data['datetime'])
    return QA_DataStruct_Stock_transaction(data.set_index('datetime', drop=if_drop_index))


def QA_fetch_security_list_adv(collections=DATABASE.stock_list):
    '获取股票列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)


def QA_fetch_stock_list_adv(collections=DATABASE.stock_list):
    '获取股票列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)


def QA_fetch_stock_block_adv(code=None, blockname=None, collections=DATABASE.stock_block):
    """返回板块

    Keyword Arguments:
        code {[type]} -- [description] (default: {None})
        blockname {[type]} -- [descrioption] (default : {None})
        collections {[type]} -- [description] (default: {DATABASE})

    Returns:
        [type] -- [description]
    """

    if code is not None and blockname is None:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        return QA_DataStruct_Stock_block(data.set_index('code', drop=False).drop_duplicates())
    elif blockname is not None and code is None:

        data = pd.DataFrame([item for item in collections.find(
            {'blockname': re.compile(blockname)})]).drop(['_id'], axis=1)
    else:
        data = pd.DataFrame(
            [item for item in collections.find()]).drop(['_id'], axis=1)
        return QA_DataStruct_Stock_block(data.set_index('code', drop=False).drop_duplicates())


def QA_fetch_stock_realtime_adv(code=None, num=1, collections=DATABASE.get_collection('realtime_{}'.format(datetime.date.today()))):
    """
    返回当日的上下五档, code可以是股票可以是list, num是每个股票获取的数量
    """
    if code is not None:
        if isinstance(code, str):
            code = list(code)

        elif isinstance(code, list):
            pass
        data = pd.DataFrame([item for item in collections.find(
            {'code': {'$in': code}}, limit=num*len(code), sort=[('datetime', pymongo.DESCENDING)])]).set_index(['datetime', 'code'], drop=False).drop(['_id'], axis=1)
        return data
    else:
        pass

if __name__ == '__main__':
    QA_fetch_stock_realtime_adv(['000001', '000002'], num=10)
