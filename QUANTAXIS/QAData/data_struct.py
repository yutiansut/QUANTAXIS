# coding :utf-8

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import pandas as pd
import numpy as np

from QUANTAXIS.QAUtil import QA_Setting, QA_util_log_info
from QUANTAXIS.QAFetch import QAQuery


class QA_DataStruct_Stock_day():
    def __init__(self, DataFrame):
        self.type = 'stock_day'
        self.if_fq='bfq'
        self.mongo_coll = QA_Setting.client.quantaxis.stock_day
        self.open = DataFrame['open']
        self.high = DataFrame['high']
        self.low = DataFrame['low']
        self.close = DataFrame['close']
        self.vol = DataFrame['volume']
        self.date = DataFrame['date']
        self.date_index = DataFrame.index
        self.data = DataFrame

    def to_qfq(self):
        data=QA_DataStruct_Stock_day(QAQuery.QA_fetch_stock_to_fq(self.data))
        data.if_fq='qfq'
        return data
    def to_hfq(self):
        data=QA_DataStruct_Stock_day(QAQuery.QA_fetch_stock_to_fq(self.data, 'hfq'))
        data.if_fq='hfq'
        return data

    def show(self):
        return QA_util_log_info(self.data)

    def add_func(self, func, *arg, **kwargs):
        return func(self.data, *arg, **kwargs)

    def to_list(self):
        return np.asarray(self.data).tolist()


class QA_DataStruct_Stock_transaction():
    pass


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
