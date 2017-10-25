# coding: utf-8
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


"""
按要求从数据库取数据，并转换成numpy结构

"""


def QA_fetch_stock_day_adv(
        code,
        __start, __end,
        if_drop_index=False,
        collections=QA_Setting.client.quantaxis.stock_day):
    '获取股票日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]
    
    if isinstance(code, str):
        print(code)
        if QA_util_date_valid(__end) == True:
            __data = []
            for item in collections.find({
                'code': str(code)[0:6], "date_stamp": {
                    "$lte": QA_util_date_stamp(__end),
                    "$gte": QA_util_date_stamp(__start)}}):
                __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                    item['low']), float(item['close']), float(item['vol']), item['date']])
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            return QA_DataStruct_Stock_day(__data.query('volume>1').set_index(['date', 'code'], drop=if_drop_index))
        else:
            QA_util_log_info('something wrong with date')
    elif isinstance(code, list):
        return QA_DataStruct_Stock_day(pd.concat(QA_fetch_stocklist_day(code, [__start, __end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))


def QA_fetch_stocklist_day_adv(
        code,
        __start, __end,
        if_drop_index=False,
        collections=QA_Setting.client.quantaxis.stock_day):
    '获取股票日线'
    return QA_DataStruct_Stock_day(pd.concat(QA_fetch_stocklist_day(code, [__start, __end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))


def QA_fetch_index_day_adv(
        code,
        __start, __end,
        if_drop_index=False,
        collections=QA_Setting.client.quantaxis.index_day):
    '获取指数日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]
    if isinstance(code, str):
        if QA_util_date_valid(__end) == True:
            __data = []
            for item in collections.find({
                'code': str(code)[0:6], "date_stamp": {
                    "$lte": QA_util_date_stamp(__end),
                    "$gte": QA_util_date_stamp(__start)}}):
                __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                    item['low']), float(item['close']), float(item['vol']), item['date']])
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            return QA_DataStruct_Index_day(__data.query('volume>1').set_index(['date', 'code'], drop=if_drop_index))
        else:
            QA_util_log_info('something wrong with date')

    elif isinstance(code, list):
        return QA_DataStruct_Index_day(pd.concat(QA_fetch_indexlist_day(code, [__start, __end])).query('volume>1').set_index(['date', 'code'], drop=if_drop_index))


def QA_fetch_index_min_adv(
        code,
        start, end,
        type_='1min',
        if_drop_index=False,
        collections=QA_Setting.client.quantaxis.index_min):
    '获取股票分钟线'
    if type_ in ['1min', '1m']:
        type_ = '1min'
    elif type_ in ['5min', '5m']:
        type_ = '5min'
    elif type_ in ['15min', '15m']:
        type_ = '15min'
    elif type_ in ['30min', '30m']:
        type_ = '30min'
    elif type_ in ['60min', '60m']:
        type_ = '60min'
    __data = []
    if isinstance(code, str):
        for item in collections.find({
            'code': str(code), "time_stamp": {
                "$gte": QA_util_time_stamp(start),
                "$lte": QA_util_time_stamp(end)
            }, 'type': type_
        }):

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

        __data = DataFrame(__data, columns=[
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

        __data['datetime'] = pd.to_datetime(__data['datetime'])
        return QA_DataStruct_Index_min(__data.query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))

    elif isinstance(code, list):
        return QA_DataStruct_Index_min(pd.concat([QA_fetch_index_min_adv(code_, start, end, type_, if_drop_index).data for code_ in code]).set_index(['datetime', 'code'], drop=if_drop_index))


def QA_fetch_stock_min_adv(
        code,
        start, end,
        type_='1min',
        if_drop_index=False,
        collections=QA_Setting.client.quantaxis.stock_min):
    '获取股票分钟线'
    if type_ in ['1min', '1m']:
        type_ = '1min'
    elif type_ in ['5min', '5m']:
        type_ = '5min'
    elif type_ in ['15min', '15m']:
        type_ = '15min'
    elif type_ in ['30min', '30m']:
        type_ = '30min'
    elif type_ in ['60min', '60m']:
        type_ = '60min'
    __data = []

    if isinstance(code, str):

        for item in collections.find({
            'code': str(code), "time_stamp": {
                "$gte": QA_util_time_stamp(start),
                "$lte": QA_util_time_stamp(end)
            }, 'type': type_
        }):

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['datetime'], item['time_stamp'], item['date']])

        __data = DataFrame(__data, columns=[
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])

        __data['datetime'] = pd.to_datetime(__data['datetime'])
        return QA_DataStruct_Stock_min(__data.query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))
    elif isinstance(code, list):
        '新增codelist的代码'
        return QA_DataStruct_Stock_min(pd.concat([QA_fetch_stock_min_adv(code_, start, end, type_, if_drop_index).data for code_ in code]).set_index(['datetime', 'code'], drop=if_drop_index))


def QA_fetch_stocklist_min_adv(
        code,
        start, end,
        type_='1min',
        if_drop_index=False,  collections=QA_Setting.client.quantaxis.stock_min):
    return QA_DataStruct_Stock_min(pd.concat(QA_fetch_stocklist_min(code, [start, end], type_)).query('volume>1').set_index(['datetime', 'code'], drop=if_drop_index))


def QA_fetch_stock_transaction_adv(
        code,
        start, end,
        if_drop_index=False,
        collections=QA_Setting.client.quantaxis.stock_transaction):
    data = DataFrame([item for item in collections.find({
        'code': str(code), "date": {
            "$gte": start,
            "$lte": end
        }})]).drop('_id', axis=1, inplace=False)
    data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])
    return QA_DataStruct_Stock_transaction(data.set_index('datetime', drop=if_drop_index))

def QA_fetch_security_list_adv(collections=QA_Setting.client.quantaxis.stock_list):
    '获取股票列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)
def QA_fetch_stock_list_adv(collections=QA_Setting.client.quantaxis.stock_list):
    '获取股票列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False)

def QA_fetch_stock_block_adv(code=None, collections=QA_Setting.client.quantaxis.stock_block):
    if code is not None:
        data = pd.DataFrame([item for item in collections.find(
            {'code': code})]).drop(['_id'], axis=1)
        return QA_DataStruct_Stock_block(data.set_index('code', drop=False))
    else:
        data = pd.DataFrame([item for item in collections.find()]).drop(['_id'], axis=1)
        return QA_DataStruct_Stock_block(data.set_index('code', drop=False))
