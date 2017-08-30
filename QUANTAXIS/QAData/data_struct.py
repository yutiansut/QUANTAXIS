# coding :utf-8

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import pandas as pd
import numpy as np

from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info, QA_util_to_json_from_pandas
from QUANTAXIS.QAFetch import QAQuery
from .data_resample import QA_data_tick_resample


class __stock_hq_base():
    def __init__(self, DataFrame):
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
        self.date = DataFrame['date']
        self.code = DataFrame['code']
        self.index = DataFrame.index
        self.data = DataFrame

    def reverse(self):
        return __stock_hq_base(self.data[::-1])

    def show(self):
        return QA_util_log_info(self.data)

    def add_func(self, func, *arg, **kwargs):
        return func(self.data, *arg, **kwargs)

    def to_list(self):
        return np.asarray(self.data).tolist()

    def to_pd(self):
        return self.data

    def to_numpy(self):
        return np.asarray(self.data)

    def to_json(self):
        return QA_util_to_json_from_pandas(self.data)


class QA_DataStruct_Stock_day(__stock_hq_base):
    '自定义的日线数据结构'

    def __init__(self, DataFrame):
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
        self.date = DataFrame['date']
        self.index = DataFrame.index
        self.code = DataFrame['code']
        self.data = DataFrame

    def to_qfq(self):
        data = QA_DataStruct_Stock_day(QAQuery.QA_fetch_stock_to_fq(self.data))
        data.if_fq = 'qfq'
        return data

    def to_hfq(self):
        data = QA_DataStruct_Stock_day(
            QAQuery.QA_fetch_stock_to_fq(self.data, 'hfq'))
        data.if_fq = 'hfq'
        return data


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
        self.date = DataFrame['date']
        self.code = DataFrame['code']
        self.index = DataFrame.index
        self.data = DataFrame

    def to_qfq(self):
        data = QA_DataStruct_Stock_min(QAQuery.QA_fetch_stock_to_fq(self.data))
        data.if_fq = 'qfq'
        return data

    def to_hfq(self):
        data = QA_DataStruct_Stock_min(
            QAQuery.QA_fetch_stock_to_fq(self.data, 'hfq'))
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


class QA_DataStruct_Stock_xdxr():
    pass


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
