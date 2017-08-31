# coding :utf-8

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import pandas as pd
import numpy as np

from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info, QA_util_to_json_from_pandas
from QUANTAXIS.QAData.data_fq import QA_data_stock_to_fq
from QUANTAXIS.QAData.data_resample import QA_data_tick_resample
from QUANTAXIS.QAIndicator import LLV, HHV, SMA, EMA
import numpy as np
import six
import talib
import itertools
from functools import reduce
# ATR


class __stock_hq_base():
    def __init__(self, DataFrame):
        self.data = DataFrame
        self.type = ''
        self.if_fq = 'bfq'
        self.mongo_coll = QA_Setting.client.quantaxis
        self.open = DataFrame['open']
        self.high = DataFrame['high']
        self.low = DataFrame['low']
        self.close = DataFrame['close']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.date = self.data.index.levels[self.data.index.names.index('date')]
        self.index = DataFrame.index
        self.code = self.data.index.levels[self.data.index.names.index('code')]

    def len(self):
        return len(self.data)

    def reverse(self):
        return __stock_hq_base(self.data[::-1])

    def show(self):
        return QA_util_log_info(self.data)

    def to_list(self):
        return np.asarray(self.data).tolist()

    def query(self, query_text):
        return self.data.query(query_text)

    def to_pd(self):
        return self.data

    def to_numpy(self):
        return np.asarray(self.data)

    def to_json(self):
        return QA_util_to_json_from_pandas(self.data)

    def sync_status(self, __stock_hq_base):
        '固定的状态要同步 尤其在创建新的datastruct时候'
        (__stock_hq_base.if_fq, __stock_hq_base.type, __stock_hq_base.mongo_coll) = (
            self.if_fq, self.type, self.mongo_coll)
        return __stock_hq_base

    def splits(self):
        return list(map(lambda data: self.sync_status(data), list(map(lambda x: (
            self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))

    def add_func(self, func, *arg, **kwargs):
        return self.sync_status(__stock_hq_base(pd.concat(list(map(lambda x: func(
            self.data[self.data['code'] == x], *arg, **kwargs), self.code)))))


class QA_DataStruct_Index_day(__stock_hq_base):
    '自定义的日线数据结构'

    def __init__(self, DataFrame):
        self.type = 'index_day'
        self.if_fq = 'bfq'
        self.mongo_coll = QA_Setting.client.quantaxis.stock_day
        self.open = DataFrame['open']
        self.high = DataFrame['high']
        self.low = DataFrame['low']

        self.close = DataFrame['close']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.date = DataFrame['date']
        self.code = DataFrame['code']
        self.index = DataFrame.index
        self.data = DataFrame

    def ATR(self, gap=14):
        list_mtr = []
        __id = -gap
        while __id < 0:
            list_mtr.append(max(self.high[__id] - self.low[__id], abs(
                self.close[__id - 1] - self.high[__id]), abs(self.close[__id - 1] - self.low[__id])))
            __id += 1
        res = talib.MA(np.array(list_mtr), gap)
        return list_mtr[-1], res[-1]

    def KDJ(self, N=9, M1=3, M2=3):
        # https://www.joinquant.com/post/142  先计算KD
        __K, __D = talib.STOCHF(np.array(self.high[-(N + M1 + M2 + 1):]), np.array(self.low[-(
            N + M1 + M2 + 1):]), np.array(self.close[-(N + M1 + M2 + 1):]), N, M2, fastd_matype=0)

        K = np.array(
            list(map(lambda x: SMA(__K[:x], M1), range(1, len(__K) + 1))))
        D = np.array(list(map(lambda x: SMA(K[:x], M2), range(1, len(K) + 1))))
        J = K * 3 - D * 2

        return K[-1], D[-1], J[-1]

    def JLHB(self, N=7, M=5):
        pass


class QA_DataStruct_Stock_min(__stock_hq_base):
    def __init__(self, DataFrame):
        self.type = 'stock_min'
        self.if_fq = 'bfq'
        self.mongo_coll = QA_Setting.client.quantaxis.stock_min
        self.open = DataFrame['open']
        self.high = DataFrame['high']
        self.low = DataFrame['low']
        self.close = DataFrame['close']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.datetime = DataFrame['datetime']
        self.data = DataFrame
        self.date = self.data.index.levels[self.data.index.names.index('date')]
        self.index = DataFrame.index
        self.code = self.data.index.levels[self.data.index.names.index('code')]

    def to_qfq(self):
        if self.if_fq is 'bfq':
            data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                self.data[self.data['code'] == x]), self.code))))
            data.if_fq = 'qfq'
            return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self

    def to_hfq(self):
        if self.if_fq is 'bfq':
            data = QA_DataStruct_Stock_min(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                self.data[self.data['code'] == x], '01'), self.code))))
            data.if_fq = 'hfq'
            return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is:%s' % self.if_fq)
            return self

    def splits(self):
        return list(map(lambda data: self.sync_status(data), list(map(lambda x: QA_DataStruct_Stock_min(self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))

    def ATR(self, gap=14):
        list_mtr = []
        __id = -gap
        while __id < 0:
            list_mtr.append(max(self.high[__id] - self.low[__id], abs(
                self.close[__id - 1] - self.high[__id]), abs(self.close[__id - 1] - self.low[__id])))
            __id += 1
        res = talib.MA(np.array(list_mtr), gap)
        return list_mtr[-1], res[-1]

    def KDJ(self, N=9, M1=3, M2=3):
        # https://www.joinquant.com/post/142  先计算KD
        __K, __D = talib.STOCHF(np.array(self.high[-(N + M1 + M2 + 1):]), np.array(self.low[-(
            N + M1 + M2 + 1):]), np.array(self.close[-(N + M1 + M2 + 1):]), N, M2, fastd_matype=0)

        K = np.array(
            list(map(lambda x: SMA(__K[:x], M1), range(1, len(__K) + 1))))
        D = np.array(list(map(lambda x: SMA(K[:x], M2), range(1, len(K) + 1))))
        J = K * 3 - D * 2

        return K[-1], D[-1], J[-1]

    def JLHB(self, N=7, M=5):
        pass


class QA_DataStruct_Stock_day(__stock_hq_base):
    def __init__(self, DataFrame):
        self.data = DataFrame
        self.type = 'stock_day'
        self.if_fq = 'bfq'
        self.mongo_coll = QA_Setting.client.quantaxis.stock_day
        self.open = DataFrame['open']
        self.high = DataFrame['high']
        self.low = DataFrame['low']
        self.close = DataFrame['close']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.date = self.data.index.levels[self.data.index.names.index('date')]
        self.index = DataFrame.index
        self.code = self.data.index.levels[self.data.index.names.index('code')]

    def to_qfq(self):
        if self.if_fq is 'bfq':
            data = QA_DataStruct_Stock_day(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                self.data[self.data['code'] == x]), self.code))))
            data.if_fq = 'qfq'
            return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    def to_hfq(self):
        if self.if_fq is 'bfq':
            data = QA_DataStruct_Stock_day(pd.concat(list(map(lambda x: QA_data_stock_to_fq(
                self.data[self.data['code'] == x], '01'), self.code))))
            data.if_fq = 'hfq'
            return data
        else:
            QA_util_log_info(
                'none support type for qfq Current type is: %s' % self.if_fq)
            return self

    def splits(self):
        return list(map(lambda data: self.sync_status(data), list(map(lambda x: QA_DataStruct_Stock_day(
            self.data[self.data['code'] == x].set_index(['date', 'code'], drop=False)), self.code))))


class QA_DataStruct_StockList_min(__stock_hq_base):
    def __init__(self, DataFrame):
        self.type = 'stock_min'
        self.if_fq = 'bfq'
        self.mongo_coll = QA_Setting.client.quantaxis.stock_min
        self.open = DataFrame['open']
        self.high = DataFrame['high']
        self.low = DataFrame['low']
        self.close = DataFrame['close']
        if 'volume' in DataFrame.columns:
            self.vol = DataFrame['volume']
        else:
            self.vol = DataFrame['vol']
        self.datetime = DataFrame['datetime']
        self.date = DataFrame['date']
        self.code = DataFrame.index.levels[0]
        self.index = DataFrame.index
        self.data = DataFrame

    def to_qfq(self):
        data = QA_DataStruct_StockList_min(QA_data_stocklist_to_fq(self.data))
        data.if_fq = 'qfq'
        return data

    def to_hfq(self):
        data = QA_DataStruct_StockList_min(
            QA_data_stocklist_to_fq(self.data, 'hfq'))
        data.if_fq = 'hfq'
        return data


class QA_DataStruct_Stock_transaction():
    def __init__(self, DataFrame):
        self.type = 'stock_transaction'
        self.if_fq = 'None'
        self.mongo_coll = QA_Setting.client.quantaxis.stock_transaction
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

    def resample(self, type_='1min'):
        return QA_DataStruct_Stock_min(QA_data_tick_resample(self.data, type_))


class QA_DataStruct_Market_reply():
    pass


class QA_DataStruct_Market_bid():
    pass


class QA_DataStruct_Market_bid_queue():
    pass


class QA_DataStruct_ARP_account():
    pass


class QA_DataStruct_Quantaxis_error():
    pass
