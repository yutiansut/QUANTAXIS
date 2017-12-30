# coding:utf-8
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

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import datetime
import itertools
import os
import platform
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
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_log_info,
                              QA_util_random_with_topic,
                              QA_util_to_json_from_pandas,
                              QA_util_to_pandas_from_json, trade_date_sse)
from QUANTAXIS.QAUtil.QAParameter import MARKET_TYPE, MARKETDATA_TYPE
from QUANTAXIS.QAUtil.QADate import QA_util_to_datetime


class _quotation_base():
    '一个自适应股票/期货/指数的基础类'

    def __init__(self, DataFrame, dtype='undefined', if_fq='bfq', marketdata_type='None'):
        self.data = DataFrame
        self.data_type = dtype
        self.type = dtype
        self.data_id = QA_util_random_with_topic('DATA', lens=3)
        self.if_fq = if_fq
        self.mongo_coll = eval(
            'QA_Setting().client.quantaxis.{}'.format(self.type))

    def __repr__(self):
        return '< QA_Base_DataStruct with %s securities >' % len(self.code)

    def __call__(self):
        return self.data

    def __str__(self):
        return self.data

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

    def __iadd__(self, DataStruct):
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        return self.append(DataStruct)

    def __sub__(self, DataStruct):
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        return self.new(data=self.data.drop(DataStruct.index).set_index(self.index.names, drop=False), dtype=self.type, if_fq=self.if_fq)

    __rsub__ = __sub__

    def __isub__(self, DataStruct):
        return self.drop(DataStruct)

    @property
    def open(self):
        return self.data.open

    @property
    def high(self):
        return self.data.high

    @property
    def low(self):
        return self.data.low

    @property
    def close(self):
        return self.data.close

    @property
    def vol(self):
        if 'volume' in self.data.columns:
            return self.data.volume
        elif 'vol' in self.data.columns:
            return self.data.vol
        else:
            return None

    @property
    def volume(self):
        if 'volume' in self.data.columns:
            return self.data.volume
        elif 'vol' in self.data.columns:
            return self.data.vol
        elif 'trade' in self.data.columns:
            return self.data.trade
        else:
            return None

    @property
    def trade(self):
        if 'trade' in self.data.columns:
            return self.data.trade
        else:
            return None

    @property
    def position(self):
        if 'position' in self.data.columns:
            return self.data.position
        else:
            return None

    @property
    def date(self):
        try:
            return self.data.index.levels[1] if 'date' in self.data.index.names else self.data['date']
        except:
            return None

    @property
    def datetime(self):
        '分钟线结构返回datetime 日线结构返回date'
        return self.data.index.levels[1]

    @property
    def panel_gen(self):
        for item in self.index.levels[0]:
            yield self.data.xs(item, level=0)

    @property
    def security_gen(self):
        for item in self.index.levels[1]:
            yield self.data.xs(item, level=1)

    def append(self, DataStruct):
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        self.data = self.data.append(DataStruct.data).drop_duplicates(
        ).set_index(self.index.names, drop=False)
        return self

    def drop(self, DataStruct):
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        self.data = self.data.drop(DataStruct.index).set_index(
            self.index.names, drop=False)
        return self

    @property
    def index(self):
        return self.data.index

    @property
    def code(self):
        return self.data.index.levels[1]

    @property
    def dicts(self):
        return self.to_dict('index')

    def get_data(self, time, code):
        try:
            return self.dicts[(QA_util_to_datetime(time), str(code))]
        except Exception as e:
            raise e

    def plot(self, code=None):
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

    def len(self):
        return len(self.data)

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
    def __init__(self, DataFrame, dtype='stock_day', if_fq='bfq'):
        super().__init__(DataFrame, dtype, if_fq)

    def __repr__(self):
        return '< QA_DataStruct_Stock_day with {} securities >'.format(len(self.code))

    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 20:
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
            return self.new(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                self.data[self.data['code'] == x], '01'), self.code))), self.type, 'hfq')
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self


class QA_DataStruct_Stock_min(_quotation_base):
    def __init__(self, DataFrame, dtype='stock_min', if_fq='bfq'):
        try:
            self.data = DataFrame.ix[:, [
                'code', 'open', 'high', 'low', 'close', 'volume', 'preclose', 'datetime', 'date']]
        except:
            self.data = DataFrame.ix[:, [
                'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'date']]
        self.type = dtype
        self.if_fq = if_fq
        self.mongo_coll = QA_Setting().client.quantaxis.stock_min

    def __repr__(self):
        return '< QA_DataStruct_Stock_Min with {} securities >'.format(len(self.code))

    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 20:
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
            data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                self.data[self.data['code'] == x], '01'), self.code))).set_index(['datetime', 'code'], drop=False))
            data.if_fq = 'hfq'
            return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self


class QA_DataStruct_future_day(_quotation_base):
    def __init__(self, DataFrame, dtype='future_day', if_fq=''):
        self.type = 'future_day'
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'trade', 'position', 'datetime', 'date']]
        self.mongo_coll = QA_Setting().client.quantaxis.future_day


class QA_DataStruct_future_min(_quotation_base):
    def __init__(self, DataFrame, dtype='future_min', if_fq=''):
        self.type = 'future_day'
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'trade', 'position', 'datetime', 'date']]
        self.mongo_coll = QA_Setting().client.quantaxis.future_min


class QA_DataStruct_Index_day(_quotation_base):
    '自定义的日线数据结构'

    def __init__(self, DataFrame, dtype='index_day', if_fq=''):
        self.data = DataFrame
        self.type = dtype
        self.if_fq = if_fq
        self.mongo_coll = eval(
            'QA_Setting().client.quantaxis.{}'.format(self.type))
    """
    def __add__(self,DataStruct):
        'add func with merge list and reindex'
        assert isinstance(DataStruct,QA_DataStruct_Index_day)
        if self.if_fq==DataStruct.if_fq:
            self.sync_status(pd.concat())
    """

    def __repr__(self):
        return '< QA_DataStruct_Index_day with {} securities >'.format(len(self.code))


class QA_DataStruct_Index_min(_quotation_base):
    '自定义的分钟线数据结构'

    def __init__(self, DataFrame, dtype='index_min', if_fq=''):
        self.type = dtype
        self.if_fq = if_fq
        self.data = DataFrame.ix[:, [
            'code', 'open', 'high', 'low', 'close', 'volume', 'datetime', 'date']]
        self.mongo_coll = QA_Setting().client.quantaxis.index_min

    def __repr__(self):
        return '< QA_DataStruct_Index_Min with %s securities >' % len(self.code)


class QA_DataStruct_Stock_block():
    def __init__(self, DataFrame):
        self.data = DataFrame

    def __repr__(self):
        return '< QA_DataStruct_Stock_Block >'

    def __call__(self):
        return self.data

    @property
    def len(self):
        return len(self.data)

    @property
    def block_name(self):
        return self.data.groupby('blockname').sum().index.unique().tolist()

    @property
    def code(self):
        return self.data.code.unique().tolist()

    def show(self):
        return self.data

    def get_code(self, code):
        return QA_DataStruct_Stock_block(self.data[self.data['code'] == code])

    def get_block(self, _block_name):
        return QA_DataStruct_Stock_block(self.data[self.data['blockname'] == _block_name])

    def getdtype(self, dtype):
        return QA_DataStruct_Stock_block(self.data[self.data['type'] == dtype])

    def get_price(self, _block_name=None):
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
        self.type = 'stock_transaction'
        self.if_fq = 'None'
        self.mongo_coll = QA_Setting().client.quantaxis.stock_transaction
        self.buyorsell = DataFrame['buyorsell']
        self.price = DataFrame['price']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.date = DataFrame['date']
        self.time = DataFrame['time']
        self.datetime = DataFrame['datetime']
        self.order = DataFrame['order']
        self.index = DataFrame.index
        self.data = DataFrame

    def __repr__(self):
        return '< QA_DataStruct_Stock_Transaction >'

    def __call__(self):
        return self.data

    def resample(self, type_='1min'):
        return QA_DataStruct_Stock_min(QA_data_tick_resample(self.data, type_))


class QA_DataStruct_Stock_realtime():
    def __init__(self, market_data):
        if isinstance(market_data, dict):
            self.market_data = QA_util_to_pandas_from_json(market_data)

        elif isinstance(market_data, pd.DataFrame):
            self.market_data = market_data

    @property
    def open(self):
        return self.market_data.open

    @property
    def price(self):
        return self.market_data.price

    @property
    def high(self):
        return self.market_data.high

    @property
    def low(self):
        return self.market_data.low

    @property
    def code(self):
        return self.code

    @property
    def last_close(self):
        return self.market_data.last_close

    @property
    def cur_vol(self):
        return self.market_data.cur_vol

    @property
    def s_vol(self):
        return self.market_data.s_vol

    @property
    def b_vol(self):
        return self.market_data.b_vol

    @property
    def vol(self):
        return self.market_data.vol

    @property
    def ask_list(self):
        return self.market_data.ix[:, ['ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
                                       'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
                                       'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]

    @property
    def bid_list(self):
        return self.market_data.ix[:, ['bid1', 'bid_vol1', 'bid2', 'bid_vol2',  'bid3', 'bid_vol3', 'bid4', 'bid_vol4', 'bid5', 'bid_vol5']]

    [['datetime', 'active1', 'active2', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
      's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
                        'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
                        'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]


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


class QA_DataStruct_Market_reply():
    pass


class QA_DataStruct_Market_order():
    pass


class QA_DataStruct_Market_order_queue():
    pass


class QA_DataStruct_ARP_account():
    pass


class QA_DataStruct_Quantaxis_error():
    pass
