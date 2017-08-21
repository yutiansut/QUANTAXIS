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

import numpy
import pandas as pd
from bson.objectid import ObjectId
from pandas import DataFrame
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_log_info,
                              QA_util_time_stamp)


"""
按要求从数据库取数据，并转换成numpy结构

"""


def QA_fetch_stock_day(code, __start, __end, type_='numpy', collections=QA_Setting.client.quantaxis.stock_day):
    '获取股票日线'
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if QA_util_date_valid(__end) == True:

        __data = []

        for item in collections.find({
            'code': str(code)[0:6], "date_stamp": {
                "$lte": QA_util_date_stamp(__end),
                "$gte": QA_util_date_stamp(__start)}}):
            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date']])
        # 多种数据格式
        if type_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif type_ in ['list', 'l', 'L']:
            __data = __data
        elif type_ in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])

            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date')
        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_trade_date(collections):
    '获取交易日期'
    __data = []
    for item in collections.find({}):
        __data.append(item['date'])
    return __data


def QA_fetch_stock_list(collections=QA_Setting.client.quantaxis.stock_list):
    '获取股票列表'
    __data = []
    for item in collections.find_one()['stock']['code']:
        __data.append(item)

    return __data


def QA_fetch_stock_full(date_, type_='numpy', collections=QA_Setting.client.quantaxis.stock_day):
    '获取全市场的某一日的数据'
    #__start = str(__start)[0:10]
    Date = str(date_)[0:10]
    if QA_util_date_valid(Date) == True:

        __data = []

        for item in collections.find({
            "date_stamp": {
                "$lte": QA_util_date_stamp(Date),
                "$gte": QA_util_date_stamp(Date)}}):
            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date']])
        # 多种数据格式
        if type_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif type_ in ['list', 'l', 'L']:
            __data = __data
        elif type_ in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date', drop=True)
        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_stock_info(code, collections):
    '获取股票信息'
    pass


def QA_fetch_stocklist_day(stock_list, collections, date_range):
    '获取多个股票的日线'
    __data = []
    for item in stock_list:
        __data.append(QA_fetch_stock_day(
            item, date_range[0], date_range[-1], 'numpy', collections))
    return __data


def QA_fetch_index_day(code, __start, __end, type_='numpy', collections=QA_Setting.client.quantaxis.stock_day):
    '获取指数日线'
    # print(datetime.datetime.now())
    __start = str(__start)[0:10]
    __end = str(__end)[0:10]

    if QA_util_date_valid(__end) == True:

        __data = []

        for item in collections.find({
            'code': str(code), "date_stamp": {
                "$lte": QA_util_date_stamp(__end),
                "$gte": QA_util_date_stamp(__start)
            }
        }):
            # print(item['code'])

            __data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date']])
        if type_ in ['n', 'N', 'numpy']:
            __data = numpy.asarray(__data)
        elif type_ in ['list', 'l', 'L']:
            __data = __data
        elif type_ in ['P', 'p', 'pandas', 'pd']:
            __data = DataFrame(__data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            __data['date'] = pd.to_datetime(__data['date'])
            __data = __data.set_index('date')

        return __data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_stock_min(code, startTime, endTime, type_='numpy', collections=QA_Setting.client.quantaxis.stock_min_five):
    '获取股票分钟线'
    __data = []
    __data_fq = []
    for item in collections.find({
        'code': str(code), "time_stamp": {
            "$gte": QA_util_time_stamp(startTime),
            "$lte": QA_util_time_stamp(endTime)
        }
    }):

        __data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['volume']), item['datetime'], item['time_stamp'], item['date']])

    
    for item in QA_Setting.client.quantaxis.stock_day.find({
        'code': str(code), "time_stamp": {
            "$gte": QA_util_time_stamp(startTime),
            "$lte": QA_util_time_stamp(endTime)
        }
    }):
        __data_fq.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['volume']), item['date']])

    
    if type_ in ['numpy', 'np', 'n']:
        return numpy.asarray(__data)
    elif type_ in ['list', 'l', 'L']:
        return __data
    elif type_ in ['P', 'p', 'pandas', 'pd']:
        __data = DataFrame(__data, columns=[
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'time_stamp', 'date'])
        __data.set_index('datetime')
        return __data




def QA_fetch_future_day():
    pass


def QA_fetch_future_min():
    pass


def QA_fetch_future_tick():
    pass
