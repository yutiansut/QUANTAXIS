# coding:utf-8
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


"""DataStruct的方法
"""
import pandas as pd

from QUANTAXIS.QAData.QADataStruct import (QA_DataStruct_Index_day,
                                           QA_DataStruct_Index_min,
                                           QA_DataStruct_Stock_day,
                                           QA_DataStruct_Stock_min)


def concat(lists):
    """类似于pd.concat 用于合并一个list里面的多个DataStruct,会自动去重



    Arguments:
        lists {[type]} -- [DataStruct1,DataStruct2,....,DataStructN]

    Returns:
        [type] -- new DataStruct
    """

    return lists[0].new(pd.concat([lists.data for lists in lists]).drop_duplicates())


def from_tushare(dataframe, dtype='day'):
    """dataframe from tushare

    Arguments:
        dataframe {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    if dtype in ['day']:
        return QA_DataStruct_Stock_day(dataframe.assign(date=pd.to_datetime(dataframe.date)).set_index(['date', 'code'], drop=False), dtype='stock_day')
    elif dtype in ['min']:
        return QA_DataStruct_Stock_min(dataframe.assign(datetime=pd.to_datetime(dataframe.datetime)).set_index(['datetime', 'code'], drop=False), dtype='stock_min')


def QDS_StockDayWarpper(func):
    """
    日线QDS装饰器
    """
    def warpper(*args, **kwargs):
        data = func(*args, **kwargs)


        if isinstance(data.index, pd.MultiIndex):

            return QA_DataStruct_Stock_day(data)
        else:
            return QA_DataStruct_Stock_day(data.assign(date=pd.to_datetime(data.date)).set_index(['date', 'code'], drop=False), dtype='stock_day')
    return warpper


def QDS_StockMinWarpper(func, *args, **kwargs):
    """
    分钟线QDS装饰器
    """

    def warpper(*args, **kwargs):
        data = func(*args, **kwargs)
        if isinstance(data.index, pd.MultiIndex):

            return QA_DataStruct_Stock_min(data)
        else:
            return QA_DataStruct_Stock_min(data.assign(datetime=pd.to_datetime(data.datetime)).set_index(['datetime', 'code'], drop=False), dtype='stock_min')
    return warpper

def QDS_IndexDayWarpper(func, *args, **kwargs):
    """
    指数日线QDS装饰器
    """

    def warpper(*args, **kwargs):
        data = func(*args, **kwargs)
        if isinstance(data.index, pd.MultiIndex):

            return QA_DataStruct_Index_day(data)
        else:
            return QA_DataStruct_Index_day(data.assign(date=pd.to_datetime(data.date)).set_index(['datetime', 'code'], drop=False), dtype='index_min')
    return warpper


def QDS_IndexMinWarpper(func, *args, **kwargs):
    """
    分钟线QDS装饰器
    """

    def warpper(*args, **kwargs):
        data = func(*args, **kwargs)
        if isinstance(data.index, pd.MultiIndex):

            return QA_DataStruct_Index_min(data)
        else:
            return QA_DataStruct_Index_min(data.assign(datetime=pd.to_datetime(data.datetime)).set_index(['datetime', 'code'], drop=False), dtype='index_min')
    return warpper


if __name__ =='__main__':
    """演示QDS装饰器
    
    Returns:
        [type] -- [description]
    """

    # import QUANTAXIS as QA

    # @QA.QDS_StockDayWarpper
    # def fetch(code,start,end):
    #     return QA.QA_fetch_get_stock_day('tdx',code,start,end,'bfq')

    # print(fetch('000001','2018-01-01','2018-06-26'))
    """演示tushare获取数据的转化
    """

    import tushare as ts
    print(from_tushare(ts.get_k_data('000001','2018-01-01','2018-06-26')))

    """[summary]
    """
