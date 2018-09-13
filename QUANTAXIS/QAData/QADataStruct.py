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

from QUANTAXIS.QAData.base_datastruct import _quotation_base
from QUANTAXIS.QAData.data_fq import QA_data_stock_to_fq
from QUANTAXIS.QAData.data_resample import QA_data_tick_resample, QA_data_day_resample, QA_data_min_resample
from QUANTAXIS.QAData.proto import stock_day_pb2  # protobuf import
from QUANTAXIS.QAData.proto import stock_min_pb2
from QUANTAXIS.QAIndicator import EMA, HHV, LLV, SMA
from QUANTAXIS.QAUtil import (DATABASE, QA_util_log_info,
                              QA_util_random_with_topic,
                              QA_util_to_json_from_pandas,
                              QA_util_to_pandas_from_json, trade_date_sse)
from QUANTAXIS.QAUtil.QADate import QA_util_to_datetime
from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE


class QA_DataStruct_Stock_day(_quotation_base):
    '''

        股票日线数据
    '''

    def __init__(self, init_data_by_df, dtype='stock_day', if_fq='bfq'):
        '''
        # 🛠 todo dtype=stock_day 和 QA_DataStruct_Stock_day 类的名字是对应的 不变的不需要指定 ，容易出错，建议改成常量 ❌
        :param init_data_by_df:  DataFrame 类型的数据，包含了数据，用来初始化这个类
        :param dtype:  stock_day 🛠 todo 改成常量
        :param if_fq:  是否复权
        '''
        super().__init__(init_data_by_df, dtype, if_fq)

        if isinstance(init_data_by_df, pd.DataFrame) == False:
            print("QAError init_data_by_df is not kind of DataFrame type !")

    # 抽象类继承

    def choose_db(self):
        self.mongo_coll = DATABASE.stock_day

    def __repr__(self):
        return '< QA_DataStruct_Stock_day with {} securities >'.format(len(self.code))
    __str__ = __repr__

    # 前复权
    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'qfq'
                return self
            # elif len(self.code) < 20:
            #     return self.new(pd.concat(list(map(
            #         lambda x: QA_data_stock_to_fq(self.data[self.data['code'] == x]), self.code))), self.type, 'qfq')
            else:
                return self.new(
                    self.groupby(level=1).apply(QA_data_stock_to_fq, 'qfq'), self.type, 'qfq')
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    # 后复权
    def to_hfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'hfq'
                return self
            else:
                return self.new(
                    self.groupby(level=1).apply(QA_data_stock_to_fq, 'hfq'), self.type, 'hfq')
                # return self.new(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                #     self.data[self.data['code'] == x], 'hfq'), self.code))), self.type, 'hfq')
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    @property
    @lru_cache()
    def high_limit(self):
        '涨停价'
        return self.groupby(level=1).close.apply(lambda x: round((x.shift(1) + 0.0002)*1.1, 2)).sort_index()

    @property
    @lru_cache()
    def low_limit(self):
        '跌停价'
        return self.groupby(level=1).close.apply(lambda x: round((x.shift(1) + 0.0002)*0.9, 2)).sort_index()

    @property
    @lru_cache()
    def next_day_low_limit(self):
        "明日跌停价"
        return round((self.data.close + 0.0002) * 0.9, 2)

    @property
    @lru_cache()
    def next_day_high_limit(self):
        "明日涨停价"
        return round((self.data.close + 0.0002) * 1.1, 2)

    @property
    def preclose(self):
        try:
            return self.data.preclose
        except:
            return None

    pre_close=preclose


    @property
    def price_chg(self):
        try:
            return (self.close-self.preclose)/self.preclose
        except:
            return None

    @property
    @lru_cache()
    def week(self):
        return self.resample('w')

    @property
    @lru_cache()
    def month(self):
        return self.resample('M')


    @property
    @lru_cache()
    def quarter(self):
        return self.resample('Q')


    # @property
    # @lru_cache()
    # def semiannual(self):
    #     return self.resample('SA')


    @property
    @lru_cache()
    def year(self):
        return self.resample('Y')

    def resample(self, level):
        try:
            return self.add_func(QA_data_day_resample, level).sort_index()
        except Exception as e:
            print('QA ERROR : FAIL TO RESAMPLE {}'.format(e))
            return None


class QA_DataStruct_Stock_min(_quotation_base):
    def __init__(self, DataFrame, dtype='stock_min', if_fq='bfq'):
        super().__init__(DataFrame, dtype, if_fq)

        try:
            if 'preclose' in DataFrame.columns:
                self.data = DataFrame.loc[:, [
                    'open', 'high', 'low', 'close', 'volume', 'amount', 'preclose']]
            else:
                self.data = DataFrame.loc[:, [
                    'open', 'high', 'low', 'close', 'volume', 'amount']]
        except Exception as e:
            raise e

        if 'high_limit' not in self.data.columns:
            self.data['high_limit'] = round(
                (self.data.close.shift(1) + 0.0002) * 1.1, 2)
        if 'low_limit' not in self.data.columns:
            self.data['low_limit'] = round(
                (self.data.close.shift(1) + 0.0002) * 0.9, 2)
        self.type = dtype
        self.if_fq = if_fq

        self.data=self.data.sort_index()

    # 抽象类继承
    def choose_db(self):
        self.mongo_coll = DATABASE.stock_min

    def __repr__(self):
        return '< QA_DataStruct_Stock_Min with {} securities >'.format(len(self.code))
    __str__ = __repr__

    def to_qfq(self):
        if self.if_fq is 'bfq':
            if len(self.code) < 1:
                self.if_fq = 'qfq'
                return self
            # elif len(self.code) < 20:
            #     data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
            #         self.data[self.data['code'] == x]), self.code))).set_index(['datetime', 'code'], drop=False))
            #     data.if_fq = 'qfq'
            #     return data
            else:
                return self.new(
                    self.groupby(level=1).apply(QA_data_stock_to_fq, 'qfq'), self.type, 'qfq')

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
                return self.new(
                    self.groupby(level=1).apply(QA_data_stock_to_fq, 'hfq'), self.type, 'hfq')
                # data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                #     self.data[self.data['code'] == x], 'hfq'), self.code))).set_index(['datetime', 'code'], drop=False))
                # data.if_fq = 'hfq'
                # return data
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

    def resample(self, level):
        try:
            return self.add_func(QA_data_min_resample, level).sort_index()
        except Exception as e:
            print('QA ERROR : FAIL TO RESAMPLE {}'.format(e))
            return None

    @property
    @lru_cache()
    def min5(self):
        return self.resample('5min')

    @property
    @lru_cache()
    def min15(self):
        return self.resample('15min')

    @property
    @lru_cache()
    def min30(self):
        return self.resample('30min')

    @property
    @lru_cache()
    def min60(self):
        return self.resample('60min')


class QA_DataStruct_Future_day(_quotation_base):
    def __init__(self, DataFrame, dtype='future_day', if_fq=''):
        self.type = 'future_day'
        self.data = DataFrame.loc[:, [
            'open', 'high', 'low', 'close', 'trade', 'position', 'price']]
        self.if_fq = if_fq

    # 抽象类继承
    def choose_db(self):
        self.mongo_coll = DATABASE.future_day

    def __repr__(self):
        return '< QA_DataStruct_Future_day with {} securities >'.format(len(self.code))
    __str__ = __repr__


class QA_DataStruct_Future_min(_quotation_base):
    """
    struct for future
    """

    def __init__(self, DataFrame, dtype='future_min', if_fq=''):
        # 🛠todo  期货分钟数据线的维护， 暂时用日线代替分钟线
        self.type = 'future_day'
        self.data = DataFrame.loc[:, [
            'open', 'high', 'low', 'close', 'trade', 'position', 'price']]
        self.if_fq = if_fq

    # 抽象类继承
    def choose_db(self):
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
        # self.mongo_coll = eval(
        #    'DATABASE.{}'.format(self.type))
    """
    def __add__(self,DataStruct):
        'add func with merge list and reindex'
        assert isinstance(DataStruct,QA_DataStruct_Index_day)
        if self.if_fq==DataStruct.if_fq:
            self.sync_status(pd.concat())
    """

    # 抽象类继承
    def choose_db(self):
        self.mongo_coll = DATABASE.index_day

    def __repr__(self):
        return '< QA_DataStruct_Index_day with {} securities >'.format(len(self.code))
    __str__ = __repr__


class QA_DataStruct_Index_min(_quotation_base):
    '自定义的分钟线数据结构'

    def __init__(self, DataFrame, dtype='index_min', if_fq=''):
        self.type = dtype
        self.if_fq = if_fq
        self.data = DataFrame.loc[:, [
            'open', 'high', 'low', 'close', 'up_count', 'down_count', 'volume', 'amount']]
        #self.mongo_coll = DATABASE.index_min

    # 抽象类继承
    def choose_db(self):
        self.mongo_coll = DATABASE.index_min

    def __repr__(self):
        return '< QA_DataStruct_Index_Min with %s securities >' % len(self.code)

    __str__ = __repr__


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
            self.data = market_data
        elif isinstance(market_data, pd.DataFrame):
            self.data = QA_util_to_json_from_pandas(market_data)

    @property
    def open(self):
        return self.data.get('open', None)

    @property
    def price(self):
        return self.data.get('price', None)

    @property
    def datetime(self):
        return self.data.get('datetime', None)

    @property
    def high(self):
        return self.data.get('high', None)

    @property
    def low(self):
        return self.data.get('low', None)

    @property
    def code(self):
        return self.data.get('code', None)

    @property
    def last_close(self):
        return self.data.get('last_close', None)

    @property
    def cur_vol(self):
        return self.data.get('cur_vol', None)

    @property
    def bid1(self):
        return self.data.get('bid1', None)

    @property
    def bid_vol1(self):
        return self.data.get('bid_vol1', None)

    @property
    def bid2(self):
        return self.data.get('bid2', None)

    @property
    def bid_vol2(self):
        return self.data.get('bid_vol2', None)

    @property
    def bid3(self):
        return self.data.get('bid3', None)

    @property
    def bid_vol3(self):
        return self.data.get('bid_vol3', None)

    @property
    def bid4(self):
        return self.data.get('bid4', None)

    @property
    def bid_vol4(self):
        return self.data.get('bid_vol4', None)

    @property
    def bid5(self):
        return self.data.get('bid5', None)

    @property
    def bid_vol5(self):
        return self.data.get('bid_vol5', None)

    @property
    def ask1(self):
        return self.data.get('ask1', None)

    @property
    def ask_vol1(self):
        return self.data.get('ask_vol1', None)

    @property
    def ask2(self):
        return self.data.get('ask2', None)

    @property
    def ask_vol2(self):
        return self.data.get('ask_vol2', None)

    @property
    def ask3(self):
        return self.data.get('ask3', None)

    @property
    def ask_vol3(self):
        return self.data.get('ask_vol3', None)

    @property
    def ask4(self):
        return self.data.get('ask4', None)

    @property
    def ask_vol4(self):
        return self.data.get('ask_vol4', None)

    @property
    def ask5(self):
        return self.data.get('ask5', None)

    @property
    def ask_vol5(self):
        return self.data.get('ask_vol5', None)


class QA_DataStruct_Stock_realtime(_realtime_base):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '< QA_REALTIME_STRUCT code {} start {} end {} >'.format(self.code.unique(), self.datetime.iloc[1], self.datetime.iloc[-1])

    # @property
    # def ask_list(self):
    #     return self.data.loc[:, ['ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
    #                                    'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
    #                                    'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]

    # @property
    # def bid_list(self):
    #     return self.data.loc[:, ['bid1', 'bid_vol1', 'bid2', 'bid_vol2',  'bid3', 'bid_vol3', 'bid4', 'bid_vol4', 'bid5', 'bid_vol5']]

    @property
    def _data(self):
        """
        return a dataframe-type result
        """
        return pd.DataFrame(self.data)

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

    def resample(self, level):
        return QA_data_tick_resample(self.data, level)


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
