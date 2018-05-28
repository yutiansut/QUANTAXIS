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

import datetime
import os
import statistics
import webbrowser
from copy import copy
from functools import lru_cache

from abc import abstractmethod

import numpy as np
import pandas as pd
from pyecharts import Kline

from QUANTAXIS.QAUtil import (QA_util_log_info,
                              QA_util_random_with_topic,
                              QA_util_to_json_from_pandas)

from QUANTAXIS.QAUtil.QADate import QA_util_to_datetime

#todo 🛠基类名字 _quotation_base 小写是因为 不直接初始化， 建议改成抽象类
class _quotation_base():
    '''
    一个自适应股票/期货/指数的基础类 , 抽象类， 不能直接初始化，必须通过下面的类继承实现
    🥑index_day  字符串 初始化  👤👥QA_DataStruct_Index_day继承
    🥑index_min  字符串 初始化  👤👥QA_DataStruct_Index_min继承
    🥑stock_day  字符串 初始化  👤👥QA_DataStruct_Stock_day继承
    🥑stock_min  字符串 初始化  👤👥QA_DataStruct_Stock_min继承
    🥑future_min 字符串 初始化  👤👥QA_DataStruct_Future_min继承
    🥑future_day 字符串 初始化  👤👥QA_DataStruct_Future_day继承
    '''

    # 🛠todo  DataFrame 改成 df 变量名字
    def __init__(self, DataFrame, dtype='undefined', if_fq='bfq', marketdata_type='None'):
        '''
        :param df: DataFrame 类型
        :param dtype: 数据
        :param if_fq: 是否复权
        :param marketdata_type:
        '''

        #🛠todo 判断DataFame 对象字段的合法性，是否正确
        self.data = DataFrame.sort_index(level=1)

        #🛠todo 该变量没有用到， 是不是 self.data_type = marketdata_type ??
        self.data_type = dtype

        #数据类型 可能的取值

        self.type = dtype
        self.data_id = QA_util_random_with_topic('DATA', lens=3)

        #默认是不复权
        self.if_fq = if_fq

        # dtype 参数 指定类 mongo 中 collection 的名字   ，
        # 🛠todo 检查 dtype 字符串是否合法， 放到抽象类中，用子类指定数据库， 后期可以支持mongodb分片集群
        # 🛠todo 子类中没有用到mongodb的数据是通过， QA_data_stock_to_fq  实现数据复权的
        # 🛠todo ❌
        # 等价执行 例如：type='stock_min' 则执行 DATABASE.stock_min
        #self.mongo_coll = eval('DATABASE.{}'.format(self.type))
        self.choose_db()

    #不能直接实例化这个类
    @abstractmethod
    def choose_db(self):
        pass

    def __repr__(self):
        return '< QA_Base_DataStruct with %d securities >' % len(self.code)

    def __call__(self):
        '''
        Emulating callable objects
        object.__call__(self[, args…])
        Called when the instance is “called” as a function;
        if this method is defined, x(arg1, arg2, ...) is a shorthand for x.__call__(arg1, arg2, ...).
        比如
        obj =  _quotation_base() 调用 __init__
        df = obj()  调用 __call__
        等同 df = obj.__call__()
        :return:  DataFrame类型
        '''
        return self.data

    __str__ = __repr__

    def __len__(self):
        '''
        :return: dataframe 的index 的数量
        '''
        return len(self.index)

    # def __getitem__(self,index):
    #     try:
    #         return self.data.__getitem__(index)
    #     except:
    #         raise ValueError('NONE EXIST INDEX')
        
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

        # try:
        #     self.new(data=self.data.__getattr__(attr), dtype=self.type, if_fq=self.if_fq)
        # except:
        raise AttributeError('QA CLASS Currently has no attribute {}'.format(attr))

    def ix(self, key):
        return self.new(data=self.data.ix(key), dtype=self.type, if_fq=self.if_fq)

    def iloc(self, key):
        return self.new(data=self.data.iloc(key), dtype=self.type, if_fq=self.if_fq)

    def loc(self, key):
        return self.new(data=self.data.loc(key), dtype=self.type, if_fq=self.if_fq)

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
        return self.price.groupby('code').apply(lambda x: x.max())

    @property
    @lru_cache()
    def min(self):
        return self.price.groupby('code').apply(lambda x: x.min())

    @property
    @lru_cache()
    def mean(self):
        return self.price.groupby('code').apply(lambda x: x.mean())
    # 一阶差分序列

    @property
    @lru_cache()
    def price_diff(self):
        '返回DataStruct.price的一阶差分'
        return self.price.groupby('code').apply(lambda x: x.diff(1))
    # 样本方差(无偏估计) population variance
    @property
    @lru_cache()
    def pvariance(self):
        '返回DataStruct.price的方差 variance'
        return self.price.groupby('code').apply(lambda x: statistics.pvariance(x))

    # 方差
    @property
    @lru_cache()
    def variance(self):
        '返回DataStruct.price的方差 variance'
        return self.price.groupby('code').apply(lambda x: statistics.variance(x))
    # 标准差

    @property
    @lru_cache()
    def bar_pct_change(self):
        '返回bar的涨跌幅'
        return (self.close - self.open) / self.open

    @property
    @lru_cache()
    def bar_amplitude(self):
        "返回bar振幅"
        return (self.high-self.low)/self.low

    @property
    @lru_cache()
    def stdev(self):
        '返回DataStruct.price的样本标准差 Sample standard deviation'
        return self.price.groupby('code').apply(lambda x: statistics.stdev(x))
    # 总体标准差

    @property
    @lru_cache()
    def pstdev(self):
        '返回DataStruct.price的总体标准差 Population standard deviation'
        return self.price.groupby('code').apply(lambda x: statistics.pstdev(x))

    # 调和平均数
    @property
    @lru_cache()
    def mean_harmonic(self):
        '返回DataStruct.price的调和平均数'
        return self.price.groupby('code').apply(lambda x: statistics.harmonic_mean(x))

    # 众数
    @property
    @lru_cache()
    def mode(self):
        '返回DataStruct.price的众数'
        try:
            return self.price.groupby('code').apply(lambda x: statistics.mode(x))
        except:
            return None

    # 振幅
    @property
    @lru_cache()
    def amplitude(self):
        '返回DataStruct.price的百分比变化'
        return self.price.groupby('code').apply(lambda x: x.max()-x.min())
    # 偏度 Skewness

    @property
    @lru_cache()
    def skew(self):
        '返回DataStruct.price的偏度'
        return self.price.groupby('code').apply(lambda x: x.skew())
    # 峰度Kurtosis

    @property
    @lru_cache()
    def kurt(self):
        '返回DataStruct.price的峰度'
        return self.price.groupby('code').apply(lambda x: x.kurt())
    # 百分数变化

    @property
    @lru_cache()
    def pct_change(self):
        '返回DataStruct.price的百分比变化'
        return self.price.groupby('code').apply(lambda x: x.pct_change())

    # 平均绝对偏差
    @property
    @lru_cache()
    def mad(self):
        '平均绝对偏差'
        return self.price.groupby('code').apply(lambda x: x.mad())

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
            yield self.new(self.data.xs(item, level=1).set_index(self.index.names, drop=False), dtype=self.type, if_fq=self.if_fq)

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


    @property
    @lru_cache()
    def split_dicts(self):
        """
        拆分成dict code:datastruct模式,方便快速选择.
        加入缓存
        """
        return dict(zip(list(self.code), self.splits()))

    def get_data(self, time, code):
        'give the time,code tuple and turn the dict'
        try:
            return self.dicts[(QA_util_to_datetime(time), str(code))]
        except Exception as e:
            raise e

    def plot(self, code=None):
        """plot the market_data"""
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
    def get(self,name):

        if name in self.data.__dir__(): 
            return eval('self.{}'.format(name))
        else:
            raise ValueError('QADATASTRUCT CANNOT GET THIS PROPERTY')

    def query(self, context):
        """
        查询data
        """
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
        """
        打印数据包的内容
        """
        return QA_util_log_info(self.data)

    def to_list(self):
        """
        转换DataStruct为list
        """
        return np.asarray(self.data).tolist()

    def to_pd(self):
        """
        转换DataStruct为dataframe
        """
        return self.data

    def to_numpy(self):
        """
        转换DataStruct为numpy.ndarray
        """
        return np.asarray(self.data)

    def to_json(self):
        """
        转换DataStruct为json
        """
        return QA_util_to_json_from_pandas(self.data)

    def to_dict(self, orient='dict'):
        """
        转换DataStruct为dict格式
        """
        return self.data.to_dict(orient)

    def to_hdf(self, place, name):
        'IO --> hdf5'
        self.data.to_hdf(place, name)
        return place, name

    def is_same(self, DataStruct):
        """
        判断是否相同
        """
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

    # def add_func(self, func, *arg, **kwargs):
    #     return pd.concat(list(map(lambda x: func(
    #         self.query('code=="{}"'.format(x)), *arg, **kwargs), self.code)))
    def add_func(self, func, *arg, **kwargs):
        return pd.concat(list(map(lambda x: func(
            self.query('code=="{}"'.format(x)), *arg, **kwargs), self.code))).sort_index()

    def pivot(self, column_):
        """增加对于多列的支持"""
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

    def selects(self, code, start, end=None):
        if self.type[-3:] in ['day']:
            if end is not None:

                return self.new(self.query('code=="{}"'.format(code)).query('date>="{}" and date<="{}"'.format(start, end)).set_index(['date', 'code'], drop=False), self.type, self.if_fq)
            else:
                return self.new(self.query('code=="{}"'.format(code)).query('date>="{}"'.format(start)).set_index(['date', 'code'], drop=False), self.type, self.if_fq)
        elif self.type[-3:] in ['min']:
            if end is not None:
                return self.new(self.query('code=="{}"'.format(code)).data[self.data['datetime'] >= start][self.data['datetime'] <= end].set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)
            else:
                return self.new(self.query('code=="{}"'.format(code)).data[self.data['datetime'] >= start].set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)

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

    def get_bar(self, code, time, if_trade=True):
        if self.type[-3:] in ['day']:
            return self.new(self.query('code=="{}" & date=="{}"'.format(code, str(time)[0:10])).set_index(['date', 'code'], drop=False), self.type, self.if_fq)

        elif self.type[-3:] in ['min']:
            return self.new(self.query('code=="{}"'.format(code))[self.data['datetime'] == str(time)].set_index(['datetime', 'code'], drop=False), self.type, self.if_fq)

    def find_bar(self, code, time):
        if len(time) == 10:
            return self.dicts[(datetime.datetime.strptime(time, '%Y-%m-%d'), code)]
        elif len(time) == 19:
            return self.dicts[(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S'), code)]
