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

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import datetime
import itertools
import os
import platform
import statistics
import sys
import time
import webbrowser
from copy import copy
from functools import lru_cache, partial, reduce

import numpy as np
import pandas as pd
from pyecharts import Kline

from QUANTAXIS.QAData.data_fq import QA_data_stock_to_fq
from QUANTAXIS.QAData.data_resample import QA_data_tick_resample
from QUANTAXIS.QAData.proto import stock_day_pb2  # protobuf import
from QUANTAXIS.QAData.proto import stock_min_pb2
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_realtime
from QUANTAXIS.QAIndicator import EMA, HHV, LLV, SMA
from QUANTAXIS.QAUtil import (DATABASE, QA_util_log_info,
                              QA_util_random_with_topic,
                              QA_util_to_json_from_pandas,
                              QA_util_to_pandas_from_json, trade_date_sse)
from QUANTAXIS.QAUtil.QADate import QA_util_to_datetime
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE


class _quotation_base():
    '一个自适应股票/期货/指数的基础类'

    def __init__(self, DataFrame, dtype='undefined', if_fq='bfq', marketdata_type='None'):
        self.data = DataFrame.sort_index()
        self.data_type = dtype
        self.type = dtype
        self.data_id = QA_util_random_with_topic('DATA', lens=3)
        self.if_fq = if_fq
        self.mongo_coll = eval(
            'DATABASE.{}'.format(self.type))

    def __repr__(self):
        return '< QA_Base_DataStruct with %s securities >' % len(self.code)

    def __call__(self):
        return self.data

    __str__ = __repr__

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        """
        iter the row one by one
        """
        for i in range(len(self.index)):
            yield self.data.iloc[i]

    def __reversed__(self):
        return self.reverse()

    def __add__(self, DataStruct):
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        return self.new(data=self.data.append(DataStruct.data).drop_duplicates().set_index(self.index.names, drop=False), dtype=self.type, if_fq=self.if_fq)

    __radd__ = __add__

    def __sub__(self, DataStruct):
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        return self.new(data=self.data.drop(DataStruct.index).set_index(self.index.names, drop=False), dtype=self.type, if_fq=self.if_fq)

    __rsub__ = __sub__

    def __getitem__(self, key):
        return self.new(data=self.data.__getitem__(key), dtype=self.type, if_fq=self.if_fq)

    def __getattr__(self, attr):
        raise AttributeError(
            'QA CLASS Currently has no attribute {}'.format(attr))

    def ix(self, key):
        return self.new(data=self.data.ix(key), dtype=self.type, if_fq=self.if_fq)

    @property
    @lru_cache()
    def open(self):
        'return open price series'
        return self.data.open

    @property
    @lru_cache()
    def high(self):
        'return high price series'
        return self.data.high

    @property
    @lru_cache()
    def low(self):
        'return low price series'
        return self.data.low

    @property
    @lru_cache()
    def close(self):
        'return close price series'
        return self.data.close

    @property
    @lru_cache()
    def volume(self):
        if 'volume' in self.data.columns:
            return self.data.volume
        elif 'vol' in self.data.columns:
            return self.data.vol
        elif 'trade' in self.data.columns:
            return self.data.trade
        else:
            return None

    vol = volume

    @property
    @lru_cache()
    def amount(self):
        if 'amount' in self.data.columns:
            return self.data.amount
        else:
            return self.vol * self.price * 100

    """为了方便调用  增加一些容易写错的情况
    """

    HIGH = high
    High = high
    LOW = low
    Low = low
    CLOSE = close
    Close = close
    VOLUME = vol
    Volume = vol
    VOL = vol
    Vol = vol

    @property
    @lru_cache()
    def OPEN(self):
        return self.open

    @property
    @lru_cache()
    def Open(self):
        return self.open

    @property
    @lru_cache()
    def price(self):
        return (self.open + self.high + self.low + self.close) / 4

    @property
    @lru_cache()
    def trade(self):
        if 'trade' in self.data.columns:
            return self.data.trade
        else:
            return None

    @property
    @lru_cache()
    def position(self):
        if 'position' in self.data.columns:
            return self.data.position
        else:
            return None

    @property
    @lru_cache()
    def date(self):
        try:
            return self.data.index.levels[0] if 'date' in self.data.index.names else self.data['date']
        except:
            return None

    @property
    @lru_cache()
    def datetime(self):
        '分钟线结构返回datetime 日线结构返回date'
        return self.data.index.levels[0]

    @property
    @lru_cache()
    def max(self):
        return self.price.max()

    @property
    @lru_cache()
    def min(self):
        return self.price.min()

    @property
    @lru_cache()
    def mean(self):
        return self.price.mean()
    # 一阶差分序列

    @property
    @lru_cache()
    def price_diff(self):
        '返回DataStruct.price的一阶差分'
        return self.price.diff(1)

    # 样本方差(无偏估计) population variance
    @property
    @lru_cache()
    def pvariance(self):
        '返回DataStruct.price的方差 variance'
        return statistics.pvariance(self.price)

    # 方差
    @property
    @lru_cache()
    def variance(self):
        '返回DataStruct.price的方差 variance'
        return statistics.variance(self.price)
    # 标准差

    @property
    @lru_cache()
    def bar_pct_change(self):
        '返回bar的涨跌幅'
        return (self.close - self.open) / self.open

    @property
    @lru_cache()
    def stdev(self):
        '返回DataStruct.price的样本标准差 Sample standard deviation'
        return statistics.stdev(self.price)
    # 总体标准差

    @property
    @lru_cache()
    def pstdev(self):
        '返回DataStruct.price的总体标准差 Population standard deviation'
        return statistics.pstdev(self.price)

    # 调和平均数
    @property
    @lru_cache()
    def mean_harmonic(self):
        '返回DataStruct.price的调和平均数'
        return statistics.harmonic_mean(self.price)

    # 众数
    @property
    @lru_cache()
    def mode(self):
        '返回DataStruct.price的众数'
        try:
            return statistics.mode(self.price)
        except:
            return None

    # 振幅
    @property
    @lru_cache()
    def amplitude(self):
        '返回DataStruct.price的百分比变化'
        return self.max - self.min
    # 偏度 Skewness

    @property
    @lru_cache()
    def skew(self):
        '返回DataStruct.price的偏度'
        return self.price.skew()
    # 峰度Kurtosis

    @property
    @lru_cache()
    def kurt(self):
        '返回DataStruct.price的峰度'
        return self.price.kurt()
    # 百分数变化

    @property
    @lru_cache()
    def pct_change(self):
        '返回DataStruct.price的百分比变化'
        return self.price.pct_change()

    # 平均绝对偏差
    @property
    @lru_cache()
    def mad(self):
        '平均绝对偏差'
        return self.price.mad()

    @property
    @lru_cache()
    def panel_gen(self):
        '返回一个基于bar的面板迭代器'
        for item in self.index.levels[0]:
            yield self.new(self.data.xs(item, level=0).set_index(self.index.names, drop=False), dtype=self.type, if_fq=self.if_fq)

    @property
    @lru_cache()
    def security_gen(self):
        '返回一个基于代码的迭代器'
        for item in self.index.levels[1]:
            yield self.data.xs(item, level=1)

    @property
    @lru_cache()
    def index(self):
        '返回结构体的索引'
        return self.data.index

    @property
    @lru_cache()
    def code(self):
        '返回结构体中的代码'
        return self.data.index.levels[1]

    @property
    @lru_cache()
    def dicts(self):
        '返回dict形式数据'
        return self.to_dict('index')

    @property
    @lru_cache()
    def len(self):
        '返回结构的长度'
        return len(self.data)

    def get_data(self, time, code):
        'give the time,code tuple and turn the dict'
        try:
            return self.dicts[(QA_util_to_datetime(time), str(code))]
        except Exception as e:
            raise e

    def plot(self, code=None):
        'plot the market_data'
        if code is None:
            path_name = '.' + os.sep + 'QA_' + self.type + \
                '_codepackage_' + self.if_fq + '.html'
            kline = Kline('CodePackage_' + self.if_fq + '_' + self.type,
                          width=1360, height=700, page_title='QUANTAXIS')

            data_splits = self.splits()

            for i_ in range(len(data_splits)):
                data = []
                axis = []
                for dates, row in data_splits[i_].data.iterrows():
                    open, high, low, close = row[1:5]
                    datas = [open, close, low, high]
                    axis.append(dates[0])
                    data.append(datas)

                kline.add(self.code[i_], axis, data, mark_point=[
                          "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
            kline.render(path_name)
            webbrowser.open(path_name)
            QA_util_log_info(
                'The Pic has been saved to your path: %s' % path_name)
        else:
            data = []
            axis = []
            for dates, row in self.select_code(code).data.iterrows():
                open, high, low, close = row[1:5]
                datas = [open, close, low, high]
                axis.append(dates[0])
                data.append(datas)

            path_name = '.{}QA_{}_{}_{}.html'.format(
                os.sep, self.type, code, self.if_fq)
            kline = Kline('{}__{}__{}'.format(code, self.if_fq, self.type),
                          width=1360, height=700, page_title='QUANTAXIS')
            kline.add(code, axis, data, mark_point=[
                      "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
            kline.render(path_name)
            webbrowser.open(path_name)
            QA_util_log_info(
                'The Pic has been saved to your path: {}'.format(path_name))

    def query(self, context):
        return self.data.query(context)

    def new(self, data=None, dtype=None, if_fq=None):
        """
        创建一个新的DataStruct
        data 默认是self.data
        inplace 是否是对于原类的修改

        """
        data = self.data if data is None else data
        dtype = self.type if dtype is None else dtype
        if_fq = self.if_fq if if_fq is None else if_fq
        temp = copy(self)
        temp.__init__(data, dtype, if_fq)
        return temp

    def reverse(self):
        return self.new(self.data[::-1])

    def tail(self, lens):
        """返回最后Lens个值的DataStruct

        Arguments:
            lens {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.new(self.data.tail(lens))

    def head(self, lens):
        """返回最前lens个值的DataStruct

        Arguments:
            lens {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.new(self.data.head(lens))

    def show(self):
        return QA_util_log_info(self.data)

    def to_list(self):
        return np.asarray(self.data).tolist()

    def to_pd(self):
        return self.data

    def to_numpy(self):
        return np.asarray(self.data)

    def to_json(self):
        return QA_util_to_json_from_pandas(self.data)

    def to_dict(self, orient='dict'):
        return self.data.to_dict(orient)

    def to_hdf(self, place, name):
        'IO --> hdf5'
        self.data.to_hdf(place, name)
        return place, name

    def is_same(self, DataStruct):
        if self.type == DataStruct.type and self.if_fq == DataStruct.if_fq:
            return True
        else:
            return False

    def splits(self):
        if self.type[-3:] in ['day']:
            return list(map(lambda x: self.new(
                self.query('code=="{}"'.format(x)).set_index(['date', 'code'], drop=False)), self.code))
        elif self.type[-3:] in ['min']:
            return list(map(lambda x: self.new(
                self.query('code=="{}"'.format(x)).set_index(['datetime', 'code'], drop=False), self.type, self.if_fq), self.code))

    def add_func(self, func, *arg, **kwargs):
        return list(map(lambda x: func(
            self.query('code=="{}"'.format(x)), *arg, **kwargs), self.code))

    def pivot(self, column_):
        '增加对于多列的支持'
        if isinstance(column_, str):
            try:
                return self.data.pivot(index='datetime', columns='code', values=column_)
            except:
                return self.data.pivot(index='date', columns='code', values=column_)
        elif isinstance(column_, list):
            try:
                return self.data.pivot_table(index='datetime', columns='code', values=column_)
            except:
                return self.data.pivot_table(index='date', columns='code', values=column_)

    def select_time(self, start, end=None):
        if self.type[-3:] in ['day']:
            if end is not None:

                return self.new(self.query('date>="{}" and date<="{}"'.format(start, end)).set_index(['date', 'code'], drop=False), self.type, self.if_fq)
            else:
                return self.new(self.query('date>="{}"'.format(start)).set_index(['date', 'code'], drop=False), self.type, self.if_fq)
        elif self.type[-3:] in ['min']:
            if end is not None:
                return self.new(self.data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)
            else:
                return self.new(self.data[self.data['datetime'] >= start].set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)

    def select_month(self, month):
        return self.new(self.data.loc[month, slice(None)], self.type, self.if_fq)

    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>']:

            def __gt(_data):
                if self.type[-3:] in ['day']:

                    return _data.query('date>"{}"'.format(time)).head(gap).set_index(['date', 'code'], drop=False)
                elif self.type[-3:] in ['min']:

                    return _data.data[_data.data['datetime'] > time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.new(pd.concat(list(map(lambda x: __gt(x), self.splits()))), self.type, self.if_fq)

        elif method in ['gte', '>=']:
            def __gte(_data):
                if self.type[-3:] in ['day']:
                    return _data.query('date>="{}"'.format(time)).head(gap).set_index(['date', 'code'], drop=False)
                elif self.type[-3:] in ['min']:
                    return _data.data[_data.data['datetime'] >= time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.new(pd.concat(list(map(lambda x: __gte(x), self.splits()))), self.type, self.if_fq)
        elif method in ['lt', '<']:
            def __lt(_data):
                if self.type[-3:] in ['day']:
                    return _data.query('date<"{}"'.format(time)).tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type[-3:] in ['min']:
                    return _data.data[_data.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)

            return self.new(pd.concat(list(map(lambda x: __lt(x), self.splits()))), self.type, self.if_fq)
        elif method in ['lte', '<=']:
            def __lte(_data):
                if self.type[-3:] in ['day']:
                    return _data.query('date<="{}"'.format(time)).tail(gap).set_index(['date', 'code'], drop=False)
                elif self.type[-3:] in ['min']:
                    return _data.data[_data.data['datetime'] <= time].tail(gap).set_index(['datetime', 'code'], drop=False)
            return self.new(pd.concat(list(map(lambda x: __lte(x), self.splits()))), self.type, self.if_fq)
        elif method in ['e', '==', '=', 'equal']:
            def __eq(_data):
                if self.type[-3:] in ['day']:
                    return _data.query('date=="{}"'.format(time)).head(gap).set_index(['date', 'code'], drop=False)
                elif self.type[-3:] in ['min']:
                    return _data.data[_data.data['datetime'] == time].head(gap).set_index(['datetime', 'code'], drop=False)
            return self.new(pd.concat(list(map(lambda x: __eq(x), self.splits()))), self.type, self.if_fq)

    def select_code(self, code):
        if self.type[-3:] in ['day']:

            return self.new(self.data.query('code=="{}"'.format(code)).set_index(['date', 'code'], drop=False), self.type, self.if_fq)

        elif self.type[-3:] in ['min']:
            return self.new(self.data.query('code=="{}"'.format(code)).set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)

    def get_bar(self, code, time, if_trade):
        if self.type[-3:] in ['day']:
            return self.new(self.query('code=="{}" & date=="{}"'.format(code, str(time)[0:10])).set_index(['date', 'code'], drop=False), self.type, self.if_fq)

        elif self.type[-3:] in ['min']:
            return self.new(self.query('code=="{}"'.format(code))[self.data['datetime'] == str(time)].set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)

    def find_bar(self, code, time):
        if len(time) == 10:
            return self.dicts[(datetime.datetime.strptime(time, '%Y-%m-%d'), code)]
        elif len(time) == 19:
            return self.dicts[(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), code)]


class QA_DataStruct_Stock_day(_quotation_base):
    """
    this is a datastruct for stock_day
    """

    def __init__(self, DataFrame, dtype='stock_day', if_fq='bfq'):
        super().__init__(DataFrame, dtype, if_fq)
        if 'high_limit' not in self.data.columns:
            self.data['high_limit'] = round(
                (self.data.close.shift(1) + 0.0002) * 1.1, 2)
        if 'low_limit' not in self.data.columns:
            self.data['low_limit'] = round(
                (self.data.close.shift(1) + 0.0002) * 0.9, 2)

    def __repr__(self):
        return '< QA_DataStruct_Stock_day with {} securities >'.format(len(self.code))
    __str__ = __repr__

    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'qfq'
                return self
            elif len(self.code) < 20:
                return self.new(pd.concat(list(map(
                    lambda x: QA_data_stock_to_fq(self.data[self.data['code'] == x]), self.code))), self.type, 'qfq')
            else:
                return self.new(
                    self.data.groupby('code').apply(QA_data_stock_to_fq), self.type, 'qfq')
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    def to_hfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'hfq'
                return self
            else:
                return self.new(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                    self.data[self.data['code'] == x], 'hfq'), self.code))), self.type, 'hfq')
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    @property
    def high_limit(self):
        '涨停价'
        return self.data.high_limit

    @property
    def low_limit(self):
        '跌停价'
        return self.data.low_limit


class QA_DataStruct_Stock_min(_quotation_base):
    def __init__(self, DataFrame, dtype='stock_min', if_fq='bfq'):
        super().__init__(DataFrame, dtype, if_fq)
        try:
            self.data = DataFrame.ix[:, [
                'code', 'open', 'high', 'low', 'close', 'volume', 'preclose', 'datetime', 'date']]
        except:
            self.data = DataFrame.ix[:, [
                'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'date']]
        if 'high_limit' not in self.data.columns:
            self.data['high_limit'] = round(
                (self.data.close.shift(1) + 0.0002) * 1.1, 2)
        if 'low_limit' not in self.data.columns:
            self.data['low_limit'] = round(
                (self.data.close.shift(1) + 0.0002) * 0.9, 2)
        self.type = dtype
        self.if_fq = if_fq
        self.mongo_coll = DATABASE.stock_min

    def __repr__(self):
        return '< QA_DataStruct_Stock_Min with {} securities >'.format(len(self.code))
    __str__ = __repr__

    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'qfq'
                return self
            elif len(self.code) < 20:
                data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                    self.data[self.data['code'] == x]), self.code))).set_index(['datetime', 'code'], drop=False))
                data.if_fq = 'qfq'
                return data
            else:
                data = QA_DataStruct_Stock_min(
                    self.data.groupby('code').apply(QA_data_stock_to_fq))
                return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self

    def to_hfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'hfq'
                return self
            else:
                data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                    self.data[self.data['code'] == x], 'hfq'), self.code))).set_index(['datetime', 'code'], drop=False))
                data.if_fq = 'hfq'
                return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self

    @property
    def high_limit(self):
        '涨停价'
        return self.data.high_limit

    @property
    def low_limit(self):
        '跌停价'
        return self.data.low_limit


class QA_DataStruct_Future_day(_quotation_base):
    def __init__(self, DataFrame, dtype='future_day', if_fq=''):
        self.type = 'future_day'
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'trade', 'position', 'datetime', 'date']]
        self.mongo_coll = DATABASE.future_day

    def __repr__(self):
        return '< QA_DataStruct_Future_day with {} securities >'.format(len(self.code))
    __str__ = __repr__


class QA_DataStruct_Future_min(_quotation_base):
    """
    struct for future
    """
    def __init__(self, DataFrame, dtype='future_min', if_fq=''):
        self.type = 'future_day'
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'trade', 'position', 'datetime', 'date']]
        self.mongo_coll = DATABASE.future_min

    def __repr__(self):
        return '< QA_DataStruct_Future_min with {} securities >'.format(len(self.code))
    __str__ = __repr__


class QA_DataStruct_Index_day(_quotation_base):
    '自定义的日线数据结构'

    def __init__(self, DataFrame, dtype='index_day', if_fq=''):
        self.data = DataFrame
        self.type = dtype
        self.if_fq = if_fq
        self.mongo_coll = eval(
            'DATABASE.{}'.format(self.type))
    """
    def __add__(self,DataStruct):
        'add func with merge list and reindex'
        assert isinstance(DataStruct,QA_DataStruct_Index_day)
        if self.if_fq==DataStruct.if_fq:
            self.sync_status(pd.concat())
    """

    def __repr__(self):
        return '< QA_DataStruct_Index_day with {} securities >'.format(len(self.code))
    __str__ = __repr__


class QA_DataStruct_Index_min(_quotation_base):
    '自定义的分钟线数据结构'

    def __init__(self, DataFrame, dtype='index_min', if_fq=''):
        self.type = dtype
        self.if_fq = if_fq
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'date']]
        self.mongo_coll = DATABASE.index_min

    def __repr__(self):
        return '< QA_DataStruct_Index_Min with %s securities >' % len(self.code)

    __str__ = __repr__


class QA_DataStruct_Stock_block():
    def __init__(self, DataFrame):
        self.data = DataFrame

    def __repr__(self):
        return '< QA_DataStruct_Stock_Block >'

    def __call__(self):
        return self.data

    @property
    def len(self):
        """返回DataStruct的长度

        Returns:
            [type] -- [description]
        """

        return len(self.data)

    @property
    def block_name(self):
        """返回所有的板块名

        Returns:
            [type] -- [description]
        """

        return self.data.groupby('blockname').sum().index.unique().tolist()

    @property
    def code(self):
        """返回唯一的证券代码

        Returns:
            [type] -- [description]
        """

        return self.data.code.unique().tolist()

    def show(self):
        """展示DataStruct

        Returns:
            dataframe -- [description]
        """

        return self.data

    def get_code(self, code):
        """getcode 获取某一只股票的板块

        Arguments:
            code {str} -- 股票代码

        Returns:
            DataStruct -- [description]
        """

        return QA_DataStruct_Stock_block(self.data[self.data['code'] == code])

    def get_block(self, _block_name):
        """getblock 获取板块

        Arguments:
            _block_name {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return QA_DataStruct_Stock_block(self.data[self.data['blockname'] == _block_name])

    def getdtype(self, dtype):
        """getdtype

        Arguments:
            dtype {str} -- gn-概念/dy-地域/fg-风格/zs-指数

        Returns:
            [type] -- [description]
        """

        return QA_DataStruct_Stock_block(self.data[self.data['type'] == dtype])

    def get_price(self, _block_name=None):
        """get_price

        Keyword Arguments:
            _block_name {[type]} -- [description] (default: {None})

        Returns:
            [type] -- [description]
        """

        if _block_name is not None:
            try:
                code = self.data[self.data['blockname']
                                 == _block_name].code.unique().tolist()
                # try to get a datastruct package of lastest price
                return QA_fetch_get_stock_realtime(code)

            except:
                return "Wrong Block Name! Please Check"
        else:
            code = self.data.code.unique().tolist()
            return QA_fetch_get_stock_realtime(code)


class QA_DataStruct_Stock_transaction():
    def __init__(self, DataFrame):
        """Stock Transaction

        Arguments:
            DataFrame {pd.Dataframe} -- [input is one/multi day transaction]
        """

        self.type = 'stock_transaction'

        self.data = DataFrame
        if 'amount' not in DataFrame.columns:
            if 'vol' in DataFrame.columns:
                self.data['amount'] = self.data.vol * self.data.price * 100
            elif 'volume' in DataFrame.columns:
                self.data['amount'] = self.data.volume * self.data.price * 100
        self.mongo_coll = DATABASE.stock_transaction

    @property
    @lru_cache()
    def buyorsell(self):
        """return the buy or sell towards 0--buy 1--sell 2--none

        Decorators:
            lru_cache

        Returns:
            [pd.Series] -- [description]
        """

        return self.data.buyorsell

    @property
    @lru_cache()
    def price(self):
        """return the deal price of tick transaction

        Decorators:
            lru_cache

        Returns:
            [type] -- [description]
        """

        return self.data.price

    @property
    @lru_cache()
    def vol(self):
        """return the deal volume of tick

        Decorators:
            lru_cache

        Returns:
            pd.Series -- volume of transaction
        """

        try:
            return self.data.volume
        except:
            return self.data.vol

    volume = vol

    @property
    @lru_cache()
    def date(self):
        """return the date of transaction

        Decorators:
            lru_cache

        Returns:
            pd.Series -- date of transaction
        """

        return self.data.date

    @property
    @lru_cache()
    def time(self):
        """return the exact time of transaction(to minute level)

        Decorators:
            lru_cache

        Returns:
            pd.Series -- till minute level 
        """

        return self.data.time

    @property
    @lru_cache()
    def datetime(self):
        """return the datetime of transaction

        Decorators:
            lru_cache

        Returns:
            pd.Series -- [description]
        """

        return self.data.datetime

    @property
    @lru_cache()
    def order(self):
        """return the order num of transaction/ for everyday change

        Decorators:
            lru_cache

        Returns:
            pd.series -- [description]
        """

        return self.data.order

    @property
    @lru_cache()
    def index(self):
        """return the transaction index

        Decorators:
            lru_cache

        Returns:
            [type] -- [description]
        """

        return self.data.index

    @property
    @lru_cache()
    def amount(self):
        """return current tick trading amount

        Decorators:
            lru_cache

        Returns:
            [type] -- [description]
        """

        return self.data.amount
    """
    最新:IF(ISNULL(NEW),PRE,NEW);
    IF (ISNULL(RANGE_AVG_PRICE) OR RANGE_AVG_PRICE <= 0)
    {
        IF (MARKETTYPE == 232 OR MARKETTYPE == 56 OR MARKETTYPE==64 OR MARKETTYPE==128 OR MARKETTYPE==168 OR MARKETTYPE==184 OR MARKETTYPE == 200 OR MARKETTYPE == 80 OR (VOL > 1 AND VOL<100))
        {
            b=SUBSAMEDAY(&VOL) ;
            m=SUM(b*最新,0);
            均价:IF(m>0,m/VOL,PRE);
        }
        ELSE IF(CODETYPE!=0 AND MONEY>0)
        {
            IF(ISNULL(MONEY) OR ISNULL(VOL) OR VOL==0 OR MONEY==0)
                均价:PRE;
            ELSE IF(VOL==VOL[1] OR MONEY==MONEY[1])
                均价:均价[1];
            ELSE
                均价:MONEY/VOL;
        }
        ELSE IF (MARKETTYPE == 176)
        {
            b=SUBSAMEDAY(&MONEY);
            m=SUM(b*最新,0);
            IF(m>0)
                均价:m/MONEY;
        }
    }
    ELSE
    {
        均价:RANGE_AVG_PRICE;
    }
    DRAWGBK(MARKETTYPE==32 AND FORMATTIME(1)<10 AND TRADETIME>242),RGB(0,0,128);
    RETURN;


    hx_star;
    hx_star_p;
    """

    def __repr__(self):
        return '< QA_DataStruct_Stock_Transaction >'

    def __call__(self):
        return self.data

    def resample(self, type_='1min'):
        """resample methods

        Returns:
            [type] -- [description]
        """

        return QA_DataStruct_Stock_min(QA_data_tick_resample(self.data, type_))

    def get_big_orders(self, bigamount=1000000):
        """return big order

        Keyword Arguments:
            bigamount {[type]} -- [description] (default: {1000000})

        Returns:
            [type] -- [description]
        """

        return self.data.query('amount>={}'.format(bigamount))

    def get_medium_order(self, lower=200000, higher=1000000):
        """return medium 

        Keyword Arguments:
            lower {[type]} -- [description] (default: {200000})
            higher {[type]} -- [description] (default: {1000000})

        Returns:
            [type] -- [description]
        """

        return self.data.query('amount>={}'.format(lower)).query('amount<={}'.format(higher))

    def get_small_order(self, smallamount=200000):
        """return small level order

        Keyword Arguments:
            smallamount {[type]} -- [description] (default: {200000})

        Returns:
            [type] -- [description]
        """

        return self.data.query('amount<={}'.format(smallamount))

    def get_time(self, start, end=None):
        if end is None:
            return self.data.loc[start]
        else:
            return self.data.loc[start:end]



class _realtime_base():
    """
    realtime 基类

    主要字段有:
    code/name
    time
    open/high/low

    买卖报价队列:(不同的可能不一样 只提供list)
    ask_list[ask1_price/ask1_volume|ask2_price/ask2_volume|ask3_price/ask3_volume....]
    bid_list[bid1_price/bid1_volume|bid2_price/bid2_volume|bid3_price/bid3_volume....]
    """

    def __init__(self, market_data):
        """转化成dict模式

        Arguments:
            market_data {[type]} -- [description]
        """

        if isinstance(market_data, dict):
            self.market_data = market_data
        elif isinstance(market_data, pd.DataFrame):
            self.market_data = QA_util_to_json_from_pandas(market_data)

    @property
    def open(self):
        return self.market_data.get('open', None)

    @property
    def price(self):
        return self.market_data.get('price', None)

    @property
    def datetime(self):
        return self.market_data.get('datetime', None)

    @property
    def high(self):
        return self.market_data.get('high', None)

    @property
    def low(self):
        return self.market_data.get('low', None)

    @property
    def code(self):
        return self.market_data.get('code', None)

    @property
    def last_close(self):
        return self.market_data.get('last_close', None)

    @property
    def cur_vol(self):
        return self.market_data.get('cur_vol', None)

    @property
    def bid1(self):
        return self.market_data.get('bid1', None)

    @property
    def bid_vol1(self):
        return self.market_data.get('bid_vol1', None)

    @property
    def bid2(self):
        return self.market_data.get('bid2', None)

    @property
    def bid_vol2(self):
        return self.market_data.get('bid_vol2', None)

    @property
    def bid3(self):
        return self.market_data.get('bid3', None)

    @property
    def bid_vol3(self):
        return self.market_data.get('bid_vol3', None)

    @property
    def bid4(self):
        return self.market_data.get('bid4', None)

    @property
    def bid_vol4(self):
        return self.market_data.get('bid_vol4', None)

    @property
    def bid5(self):
        return self.market_data.get('bid5', None)

    @property
    def bid_vol5(self):
        return self.market_data.get('bid_vol5', None)

    @property
    def ask1(self):
        return self.market_data.get('ask1', None)

    @property
    def ask_vol1(self):
        return self.market_data.get('ask_vol1', None)

    @property
    def ask2(self):
        return self.market_data.get('ask2', None)

    @property
    def ask_vol2(self):
        return self.market_data.get('ask_vol2', None)

    @property
    def ask3(self):
        return self.market_data.get('ask3', None)

    @property
    def ask_vol3(self):
        return self.market_data.get('ask_vol3', None)

    @property
    def ask4(self):
        return self.market_data.get('ask4', None)

    @property
    def ask_vol4(self):
        return self.market_data.get('ask_vol4', None)

    @property
    def ask5(self):
        return self.market_data.get('ask5', None)

    @property
    def ask_vol5(self):
        return self.market_data.get('ask_vol5', None)


class QA_DataStruct_Stock_realtime(_realtime_base):
    def __init__(self, market_data):
        if isinstance(market_data, dict):
            self.market_data = market_data
        elif isinstance(market_data, pd.DataFrame):
            self.market_data = QA_util_to_json_from_pandas(market_data)

    def __repr__(self):
        return '< QA_REALTIME_STRUCT {}{} >'.format(self.code, self.datetime)

    # @property
    # def ask_list(self):
    #     return self.market_data.ix[:, ['ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
    #                                    'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
    #                                    'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]

    # @property
    # def bid_list(self):
    #     return self.market_data.ix[:, ['bid1', 'bid_vol1', 'bid2', 'bid_vol2',  'bid3', 'bid_vol3', 'bid4', 'bid_vol4', 'bid5', 'bid_vol5']]

    @property
    def _data(self):
        """
        return a dataframe-type result
        """
        return pd.DataFrame(self.market_data)

    @property
    def ab_board(self):
        """ask_bid board
        bid3 bid_vol3
        bid2 bid_vol2
        bid1 bid_vol1
        ===============
        price /cur_vol
        ===============
        ask1 ask_vol1
        ask2 ask_vol2
        ask3 ask_vol3
        """
        return 'BID5 {}  {} \nBID4 {}  {} \nBID3 {}  {} \nBID2 {}  {} \nBID1 {}  {} \n============\nCURRENT {}  {} \n============\
        \nASK1 {}  {} \nASK2 {}  {} \nASK3 {}  {} \nASK4 {}  {} \nASK5 {}  {} \nTIME {}  CODE {} '.format(
            self.bid5, self.bid_vol5, self.bid4, self.bid_vol4, self.bid3, self.bid_vol3, self.bid2, self.bid_vol2, self.bid1, self.bid_vol1,
            self.price, self.cur_vol,
            self.ask1, self.ask_vol1, self.ask2, self.ask_vol2, self.ask3, self.ask_vol3, self.ask4, self.ask_vol4, self.ask5, self.ask_vol5,
            self.datetime, self.code
        )

    def serialize(self):
        """to_protobuf
        """
        pass


class QA_DataStruct_Stock_realtime_series():
    def __init__(self, sr_series):

        if isinstance(sr_series[0], QA_DataStruct_Stock_realtime):
            self.sr_series = sr_series
        elif isinstance(sr_series[0], dict):
            self.sr_series = [
                QA_DataStruct_Stock_realtime(sr) for sr in sr_series]
        self.table = pd.concat([sr._data for sr in self.sr_series])


class QA_DataStruct_Security_list():
    def __init__(self, DataFrame):
        self.data = DataFrame.loc[:, ['sse', 'code', 'name']].set_index(
            'code', drop=False)

    @property
    def code(self):
        return self.data.code

    @property
    def name(self):
        return self.data.name

    def get_stock(self, ST_option):
        return self.data

    def get_index(self):
        return self.data

    def get_etf(self):
        return self.data
