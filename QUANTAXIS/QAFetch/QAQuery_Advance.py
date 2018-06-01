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
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day,
                                       QA_fetch_index_min,
                                       QA_fetch_stock_day,
                                       QA_fetch_stock_full,
                                       QA_fetch_stock_min)
from QUANTAXIS.QAUtil import (DATABASE, QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_log_info,
                              QA_util_time_stamp)

"""
按要求从数据库取数据，并转换成numpy结构

总体思路：
⚙️QA_fetch_***_adv
📍⚙️QA_fetch_*** 🐌 获取数据collections从mongodb中 🐌 返回DataFrame , 
📍📍⚙️用返回的 DataFrame 初始化 ️QA_DataStruct_***

类型***有
_Stock_day
_Stock_min
_Index_day
_Index_min
"""
# start='1990-01-01',end=str(datetime.date.today())


def QA_fetch_stock_day_adv(
        code,
        start='all', end=None,
        if_drop_index=False,
        # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.stock_day):
    '''

    :param code:  股票代码
    :param start: 开始日期
    :param end:   结束日期
    :param if_drop_index:
    :param collections: 默认数据库
    :return: 如果股票代码不存 或者开始结束日期不存在 在返回 None ，合法返回 QA_DataStruct_Stock_day 数据
    '''
    '获取股票日线'
    end = start if end is None else end
    start = str(start)[0:10]
    end = str(end)[0:10]

    if start == 'all':
        start = '1990-01-01'
        end = str(datetime.date.today())

    res = QA_fetch_stock_day(code, start, end, format='pd')
    if res is None:
        # 🛠 todo 报告是代码不合法，还是日期不合法
        print("💢 Error QA_fetch_stock_day_adv parameter code=%s , start=%s, end=%s call QA_fetch_stock_day return None"%(code,start,end))
        return None
    else:
        return QA_DataStruct_Stock_day(res.set_index(['date', 'code'], drop=if_drop_index))


def QA_fetch_stock_min_adv(
        code,
        start, end=None,
        frequence='1min',
        if_drop_index=False,
        # 🛠 todo collections 参数没有用到， 且数据库是固定的， 这个变量后期去掉
        collections=DATABASE.stock_min):
    '''
    '获取股票分钟线'
    :param code:  字符串str eg 600085
    :param start: 字符串str 开始日期 eg 2011-01-01
    :param end:   字符串str 结束日期 eg 2011-05-01
    :param frequence: 字符串str 分钟线的类型 支持 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m 类型
    :param if_drop_index: Ture False ， dataframe drop index or not
    :param collections: mongodb 数据库
    :return:
    '''
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
        print("💢 Error QA_fetch_stock_min_adv parameter frequence=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m"%frequence)
        return None

    #__data = [] 未使用

    end = start if end is None else end
    if len(start) == 10:
        start = '{} 09:30:00'.format(start)

    if len(end) == 10:
        end = '{} 15:00:00'.format(end)

    if start == end:
        print("💢 Error QA_fetch_stock_min_adv parameter code=%s , start=%s, end=%s is equal, should have time span! "%(code,start,end))
        return None

    res = QA_fetch_stock_min(code, start, end, format='pd', frequence=frequence)
    if res is None:
        print("💢 Error QA_fetch_stock_min_adv parameter code=%s , start=%s, end=%s frequence=%s call QA_fetch_stock_min return None"%(code,start,end,frequence))
        return None
    else:
        res_set_index = res.set_index(['datetime', 'code'],drop=if_drop_index)
        if res_set_index is None:
            print("💢 Error QA_fetch_stock_min_adv set index 'datetime, code' return None")
            return None
        else:
            return QA_DataStruct_Stock_min(res_set_index)


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
    return QA_DataStruct_Index_day(QA_fetch_index_day(code, start, end, format='pd').set_index(['date', 'code'], drop=if_drop_index))


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
    return QA_DataStruct_Index_min(QA_fetch_index_min(code,start,end,format='pd',frequence=frequence).set_index(['datetime', 'code'], drop=if_drop_index))

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
    '''
    返回板块
    :param code:
    :param blockname:
    :param collections: 默认数据库 stock_block
    :return:
    '''
    if code is not None and blockname is None:
        # 根据代码 和 板块名称 查找
        data = pd.DataFrame([item for item in collections.find({'code': code})]).drop(['_id'], axis=1)
        return QA_DataStruct_Stock_block(data.set_index('code', drop=False).drop_duplicates())
    elif blockname is not None and code is None:
        # 板块名称 查找
        data = pd.DataFrame([item for item in collections.find({'blockname': re.compile(blockname)})]).drop(['_id'], axis=1)
    else:
        # ？？
        data = pd.DataFrame([item for item in collections.find()]).drop(['_id'], axis=1)
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
