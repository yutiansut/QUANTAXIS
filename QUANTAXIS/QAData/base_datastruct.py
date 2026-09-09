# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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
import json
import os
import statistics
import webbrowser
from abc import abstractmethod
from copy import copy, deepcopy
from functools import lru_cache

import numpy as np
import pandas as pd
from dateutil import parser

try:
    from pyecharts import Bar, Grid, Kline
except:
    from pyecharts.charts import Kline, Bar, Grid

from QUANTAXIS.QAUtil import (QA_util_log_info, QA_util_random_with_topic,
                              QA_util_to_json_from_pandas)
from QUANTAXIS.QAUtil.QADate import QA_util_to_datetime

# todo 🛠基类名字 _quotation_base 小写是因为 不直接初始化， 建议改成抽象类


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
    def __init__(
        self,
        DataFrame,
        dtype='undefined',
        if_fq='bfq',
        marketdata_type='None',
        frequence=None
    ):
        '''
        :param df: DataFrame 类型
        :param dtype: 数据
        :param if_fq: 是否复权
        :param marketdata_type:
        '''
        if 'volume' not in DataFrame.columns and 'vol' in DataFrame.columns:
            DataFrame = DataFrame.assign(volume=DataFrame.vol)
        if 'volume' not in DataFrame.columns and 'trade' in DataFrame.columns:
            DataFrame = DataFrame.assign(volume=DataFrame.trade)
        # print(DataFrame)
        # 🛠todo 判断DataFame 对象字段的合法性，是否正确
        self.data = DataFrame.drop_duplicates().sort_index()
        self.data.index = self.data.index.remove_unused_levels()
        # 🛠todo 该变量没有用到， 是不是 self.type = marketdata_type ??

        # 数据类型 可能的取值

        self.type = dtype
        self.data_id = QA_util_random_with_topic('DATA', lens=3)
        self.frequence = frequence
        # 默认是不复权
        self.if_fq = if_fq
        # dtype 参数 指定类 mongo 中 collection 的名字   ，
        # 🛠todo 检查 dtype 字符串是否合法， 放到抽象类中，用子类指定数据库， 后期可以支持mongodb分片集群
        # 🛠todo 子类中没有用到mongodb的数据是通过， QA_data_stock_to_fq  实现数据复权的
        # 等价执行 例如：type='stock_min' 则执行 DATABASE.stock_min
        #self.mongo_coll = eval('DATABASE.{}'.format(self.type))
        self.choose_db()

    # 不能直接实例化这个类
    @abstractmethod
    def choose_db(self):
        pass

    def __repr__(self):
        return '< QA_Base_DataStruct with %d securities >' % len(self.code)

    def __call__(self):
        '''
        如果需要暴露 DataFrame 内部数据对象，就用() 来转换出 data （DataFrame）
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
        返回记录的数目
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
        📌关于 yield 的问题
        A yield statement is semantically equivalent to a yield expression.
        yield 的作用就是把一个函数变成一个 generator，
        带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator
        for iterObj in ThisObj
        📌关于__iter__ 的问题
        可以不被 __next__ 使用
        Return an iterator object
        iter the row one by one
        :return:  class 'generator'
        """
        for i in range(len(self.index)):
            yield self.data.iloc[i]

    # 🛠todo == 操作比较数据
    # def __eq__(self, other):
    #    return self.data == other.data

    # 初始化的时候会重新排序
    def __reversed__(self):
        """
        If the __reversed__() method is not provided,
        the reversed() built-in will fall back to using the sequence protocol (__len__() and __getitem__()).
        Objects that support the sequence protocol should only provide __reversed__()
        if they can provide an implementation that is more efficient than the one provided by reversed().
        如果__reversed__() 方法没有提供，
        则调用内建的reversed()方法会退回到使用序列协议（ __len__条目数量 和 获取条目__getitem__ ）方法。
        对象如果支持实现序列协议应该只提供__reversed__方法，如果比上述reversed提供的方式更加有效率 （自己实现一个反向迭代)

        self.new(self.data[::-1])
        :return:
        """
        raise NotImplementedError(
            'QA_DataStruct_* CURRENT CURRENTLY NOT SUPPORT reversed ACTION'
        )

    def __add__(self, DataStruct):
        '''
        ➕合并数据，重复的数据drop
        :param DataStruct: _quotation_base 继承的子类  QA_DataStruct_XXXX
        :return: _quotation_base 继承的子类  QA_DataStruct_XXXX
        '''
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        # 🛠todo 继承的子类  QA_DataStruct_XXXX 类型的 判断必须是同一种类型才可以操作
        return self.new(
            data=pd.concat([self.data, DataStruct.data]).drop_duplicates(),
            dtype=self.type,
            if_fq=self.if_fq
        )

    __radd__ = __add__

    def __sub__(self, DataStruct):
        '''
        ⛔️不是提取公共数据， 去掉 DataStruct 中指定的数据
        :param DataStruct:  _quotation_base 继承的子类  QA_DataStruct_XXXX
        :return: _quotation_base 继承的子类  QA_DataStruct_XXXX
        '''
        assert isinstance(DataStruct, _quotation_base)
        assert self.is_same(DataStruct)
        # 🛠todo 继承的子类  QA_DataStruct_XXXX 类型的 判断必须是同一种类型才可以操作
        try:
            return self.new(
                data=self.data.drop(DataStruct.index),
                dtype=self.type,
                if_fq=self.if_fq
            )
        except Exception as e:
            print(e)

    __rsub__ = __sub__

    def __getitem__(self, key):
        '''
        # 🛠todo 进一步研究 DataFrame __getitem__ 的意义。
        DataFrame调用__getitem__调用(key)
        :param key:
        :return:
        '''
        data_to_init = self.data.__getitem__(key)
        if isinstance(data_to_init, pd.DataFrame) == True:
            # 重新构建一个 QA_DataStruct_XXXX，
            return self.new(
                data=data_to_init,
                dtype=self.type,
                if_fq=self.if_fq
            )
        elif isinstance(data_to_init, pd.Series) == True:
            # 返回 QA_DataStruct_XXXX DataFrame 中的一个 序列Series
            return data_to_init

    def __getattr__(self, attr):
        '''
        # 🛠todo 为何不支持 __getattr__ ？？
        :param attr:
        :return:
        '''
        # try:
        #     self.new(data=self.data.__getattr__(attr), dtype=self.type, if_fq=self.if_fq)
        # except:
        raise AttributeError(
            'QA_DataStruct_* Class Currently has no attribute {}'.format(attr)
        )

    '''
    ########################################################################################################
    获取序列
    '''

    def ix(self, key):
        return self.new(
            data=self.data.ix(key),
            dtype=self.type,
            if_fq=self.if_fq
        )

    def iloc(self, key):
        return self.new(
            data=self.data.iloc(key),
            dtype=self.type,
            if_fq=self.if_fq
        )

    def loc(self, key):
        return self.new(
            data=self.data.loc(key),
            dtype=self.type,
            if_fq=self.if_fq
        )

    '''
    ########################################################################################################
    获取序列
    使用 LRU (least recently used) cache 
    '''

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
    def closepanel(self):
        if 'min' in self.type:
            return self.close.reset_index().pivot(index='datetime', columns='code', values='close')
        elif 'day' in self.type:
            return self.close.reset_index().pivot(index='date', columns='code', values='close')

    @property
    @lru_cache()
    def openpanel(self):
        if 'min' in self.type:
            return self.open.reset_index().pivot(index='datetime', columns='code', values='open')
        elif 'day' in self.type:
            return self.open.reset_index().pivot(index='date', columns='code', values='open')

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

    #OPEN = open
    #Open = open
    @property
    @lru_cache()
    def OPEN(self):
        return self.open

    @property
    @lru_cache()
    def Open(self):
        return self.open

    # 开盘 收盘 最高 最低 的 平均价
    @property
    @lru_cache()
    def price(self):

        res = (self.open + self.high + self.low + self.close) / 4
        res.name = 'price'
        return res

    # ？？
    @property
    @lru_cache()
    def trade(self):
        """
        期货中
        """
        if 'trade' in self.data.columns:
            return self.data.trade
        else:
            return None

    # ？？

    @property
    @lru_cache()
    def position(self):
        if 'position' in self.data.columns:
            return self.data.position
        else:
            return None

    # 交易日期
    @property
    @lru_cache()
    def date(self):
        index = self.data.index.remove_unused_levels()
        try:
            return index.levels[0
                                ] if 'date' in self.data.index.names else sorted(
                list(set(self.datetime.date))
            )
        except:
            return None

    @property
    @lru_cache()
    def datetime(self):
        '分钟线结构返回datetime 日线结构返回date'
        index = self.data.index.remove_unused_levels()
        return pd.to_datetime(
            index.levels[0], utc=False)

    @property
    @lru_cache()
    def money(self):
        res = self.data.amount
        res.name = 'money'
        return res

    @property
    @lru_cache()
    def avg(self):
        try:
            res = self.amount / self.volume
            res.name = 'avg'
            return res
        except:
            return None

    @property
    @lru_cache()
    def ndarray(self):
        return self.reset_index().values

    '''
    ########################################################################################################
    计算统计相关的
    '''

    @property
    @lru_cache()
    def max(self):
        res = self.price.groupby(level=1).apply(lambda x: x.max())
        res.name = 'max'
        return res

    @property
    @lru_cache()
    def min(self):
        res = self.price.groupby(level=1).apply(lambda x: x.min())
        res.name = 'min'
        return res

    @property
    @lru_cache()
    def mean(self):
        res = self.price.groupby(level=1).apply(lambda x: x.mean())
        res.name = 'mean'
        return res

    # 一阶差分序列

    @property
    @lru_cache()
    def price_diff(self):
        '返回DataStruct.price的一阶差分'
        res = self.price.groupby(level=1).apply(lambda x: x.diff(1))
        res.name = 'price_diff'
        return res

    # 样本方差(无偏估计) population variance

    @property
    @lru_cache()
    def pvariance(self):
        '返回DataStruct.price的方差 variance'
        res = self.price.groupby(level=1
                                 ).apply(lambda x: statistics.pvariance(x))
        res.name = 'pvariance'
        return res

    # 方差
    @property
    @lru_cache()
    def variance(self):
        '返回DataStruct.price的方差 variance'
        res = self.price.groupby(level=1
                                 ).apply(lambda x: statistics.variance(x))
        res.name = 'variance'
        return res

    # 标准差

    @property
    @lru_cache()
    def bar_pct_change(self):
        '返回bar的涨跌幅'
        res = (self.close - self.open) / self.open
        res.name = 'bar_pct_change'
        return res

    @property
    @lru_cache()
    def bar_amplitude(self):
        "返回bar振幅"
        res = (self.high - self.low) / self.low
        res.name = 'bar_amplitude'
        return res

    @property
    @lru_cache()
    def stdev(self):
        '返回DataStruct.price的样本标准差 Sample standard deviation'
        res = self.price.groupby(level=1).apply(lambda x: statistics.stdev(x))
        res.name = 'stdev'
        return res

    # 总体标准差

    @property
    @lru_cache()
    def pstdev(self):
        '返回DataStruct.price的总体标准差 Population standard deviation'
        res = self.price.groupby(level=1).apply(lambda x: statistics.pstdev(x))
        res.name = 'pstdev'
        return res

    # 调和平均数
    @property
    @lru_cache()
    def mean_harmonic(self):
        '返回DataStruct.price的调和平均数'
        res = self.price.groupby(level=1
                                 ).apply(lambda x: statistics.harmonic_mean(x))
        res.name = 'mean_harmonic'
        return res

    # 众数
    @property
    @lru_cache()
    def mode(self):
        '返回DataStruct.price的众数'
        try:
            res = self.price.groupby(level=1
                                     ).apply(lambda x: statistics.mode(x))
            res.name = 'mode'
            return res
        except:
            return None

    # 振幅
    @property
    @lru_cache()
    def amplitude(self):
        '返回DataStruct.price的百分比变化'
        res = self.price.groupby(
            level=1
        ).apply(lambda x: (x.max() - x.min()) / x.min())
        res.name = 'amplitude'
        return res

    # 偏度 Skewness

    @property
    @lru_cache()
    def skew(self):
        '返回DataStruct.price的偏度'
        res = self.price.groupby(level=1).apply(lambda x: x.skew())
        res.name = 'skew'
        return res

    # 峰度Kurtosis

    @property
    @lru_cache()
    def kurt(self):
        '返回DataStruct.price的峰度'
        res = self.price.groupby(level=1).apply(lambda x: x.kurt())
        res.name = 'kurt'
        return res

    # 百分数变化

    @property
    @lru_cache()
    def pct_change(self):
        '返回DataStruct.price的百分比变化'
        res = self.price.groupby(level=1).apply(lambda x: x.pct_change())
        res.name = 'pct_change'
        return res

    @lru_cache()
    def close_pct_change(self):
        '返回DataStruct.close的百分比变化'
        res = self.close.groupby(level=1).apply(lambda x: x.pct_change())
        res.name = 'close_pct_change'
        return res

    # 平均绝对偏差
    @property
    @lru_cache()
    def mad(self):
        '平均绝对偏差'
        res = self.price.groupby(level=1).apply(lambda x: x.mad())
        res.name = 'mad'
        return res

    # 归一化(此处的归一化不能使用 MinMax方法, 会引入未来数据)
    @property
    @lru_cache()
    def normalized(self):
        '归一化'
        res = self.groupby('code').apply(lambda x: x / x.iloc[0])
        return res

    @property
    def panel_gen(self):
        '返回一个基于bar的面板迭代器'
        for item in self.index.levels[0]:
            yield self.new(
                self.data.xs(item,
                             level=0,
                             drop_level=False),
                dtype=self.type,
                if_fq=self.if_fq
            )

    @property
    def bar_gen(self):
        '返回一个基于bar的面板迭代器 返回的是dataframe'
        # for item in self.index.levels[0]:
        #     yield self.data.xs(item, level=0, drop_level=False)
        return self.data.iterrows()

    @property
    def security_gen(self):
        '返回一个基于代码的迭代器'
        for item in self.index.levels[1]:
            yield self.new(
                self.data.xs(item,
                             level=1,
                             drop_level=False),
                dtype=self.type,
                if_fq=self.if_fq
            )

    @property
    @lru_cache()
    def index(self):
        '返回结构体的索引'
        return self.data.index.remove_unused_levels()

    @property
    @lru_cache()
    def code(self):
        '返回结构体中的代码'
        return self.index.levels[1].map(lambda x: x[0:6])

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

    def get_dict(self, time, code):
        '''
        'give the time,code tuple and turn the dict'
        :param time:
        :param code:
        :return:  字典dict 类型
        '''
        try:
            return self.dicts[(
                QA_util_to_datetime(time),
                str(code)
            )]
        except Exception as e:
            raise e

    def reset_index(self):
        return self.data.reset_index()

    def rolling(self, N):
        return self.groupby('code').rolling(N)

    def kline_echarts(self, code=None):

        def kline_formater(param):
            return param.name + ':' + vars(param)

        """plot the market_data"""
        if code is None:
            path_name = '.' + os.sep + 'QA_' + self.type + \
                '_codepackage_' + self.if_fq + '.html'
            kline = Kline(
                'CodePackage_' + self.if_fq + '_' + self.type,
                width=1360,
                height=700,
                page_title='QUANTAXIS'
            )

            bar = Bar()
            data_splits = self.splits()

            for ds in data_splits:
                data = []
                axis = []
                if ds.type[-3:] == 'day':
                    datetime = np.array(ds.date.map(str))
                else:
                    datetime = np.array(ds.datetime.map(str))
                ohlc = np.array(
                    ds.data.loc[:,
                                ['open',
                                 'close',
                                 'low',
                                 'high']]
                )

                kline.add(
                    ds.code[0],
                    datetime,
                    ohlc,
                    mark_point=["max",
                                "min"],
                    is_datazoom_show=True,
                    datazoom_orient='horizontal'
                )
            return kline

        else:
            data = []
            axis = []
            ds = self.select_code(code)
            data = []
            #axis = []
            if self.type[-3:] == 'day':
                datetime = np.array(ds.date.map(str))
            else:
                datetime = np.array(ds.datetime.map(str))

            ohlc = np.array(ds.data.loc[:, ['open', 'close', 'low', 'high']])
            vol = np.array(ds.volume)
            kline = Kline(
                '{}__{}__{}'.format(code,
                                    self.if_fq,
                                    self.type),
                width=1360,
                height=700,
                page_title='QUANTAXIS'
            )
            bar = Bar()
            kline.add(self.code, datetime, ohlc,
                      mark_point=["max", "min"],
                      # is_label_show=True,
                      is_datazoom_show=True,
                      is_xaxis_show=False,
                      # is_toolbox_show=True,
                      tooltip_formatter='{b}:{c}',  # kline_formater,
                      # is_more_utils=True,
                      datazoom_orient='horizontal')

            bar.add(
                self.code,
                datetime,
                vol,
                is_datazoom_show=True,
                datazoom_xaxis_index=[0,
                                      1]
            )

            grid = Grid(width=1360, height=700, page_title='QUANTAXIS')
            grid.add(bar, grid_top="80%")
            grid.add(kline, grid_bottom="30%")
            return grid

    def plot(self, code=None):
        path_name = '.{}QA_{}_{}_{}.html'.format(
            os.sep,
            self.type,
            code,
            self.if_fq
        )
        self.kline_echarts(code).render(path_name)
        webbrowser.open(path_name)
        QA_util_log_info(
            'The Pic has been saved to your path: {}'.format(path_name)
        )

    def get(self, name):

        if name in self.data.__dir__():
            return eval('self.{}'.format(name))
        else:
            raise ValueError('QADATASTRUCT CANNOT GET THIS PROPERTY')

    def query(self, context):
        """
        查询data
        """
        try:
            return self.data.query(context)

        except pd.core.computation.ops.UndefinedVariableError:
            print('QA CANNOT QUERY THIS {}'.format(context))
            pass

    def groupby(
        self,
        by=None,
        axis=0,
        level=None,
        as_index=True,
        sort=False,
        group_keys=False,
        squeeze=False,
        **kwargs
    ):
        """仿dataframe的groupby写法,但控制了by的code和datetime

        Keyword Arguments:
            by {[type]} -- [description] (default: {None})
            axis {int} -- [description] (default: {0})
            level {[type]} -- [description] (default: {None})
            as_index {bool} -- [description] (default: {True})
            sort {bool} -- [description] (default: {True})
            group_keys {bool} -- [description] (default: {True})
            squeeze {bool} -- [description] (default: {False})
            observed {bool} -- [description] (default: {False})

        Returns:
            [type] -- [description]
        """

        if by == self.index.names[1]:
            by = None
            level = 1
        elif by == self.index.names[0]:
            by = None
            level = 0
        # 适配 pandas 1.0+，避免出现 FutureWarning:
        # Paramter 'squeeze' is deprecated 提示
        if (squeeze):
            return self.data.groupby(
                by=by,
                axis=axis,
                level=level,
                as_index=as_index,
                sort=sort,
                group_keys=group_keys,
                squeeze=squeeze
            ).squeeze()
        else:
            return self.data.groupby(
                by=by,
                axis=axis,
                level=level,
                as_index=as_index,
                sort=sort,
                group_keys=group_keys,
            )

    def new(self, data=None, dtype=None, if_fq=None):
        """
        创建一个新的DataStruct
        data 默认是self.data
        🛠todo 没有这个？？ inplace 是否是对于原类的修改 ？？
        """
        data = self.data if data is None else data

        dtype = self.type if dtype is None else dtype
        if_fq = self.if_fq if if_fq is None else if_fq

        temp = copy(self)
        temp.__init__(data, dtype, if_fq)
        return temp

    def reverse(self):
        return self.new(self.data[::-1])

    def reindex(self, ind):
        """reindex

        Arguments:
            ind {[type]} -- [description]

        Raises:
            RuntimeError -- [description]
            RuntimeError -- [description]

        Returns:
            [type] -- [description]
        """

        if isinstance(ind, pd.MultiIndex):
            try:
                return self.new(self.data.reindex(ind))
            except:
                raise RuntimeError('QADATASTRUCT ERROR: CANNOT REINDEX')
        else:
            raise RuntimeError(
                'QADATASTRUCT ERROR: ONLY ACCEPT MULTI-INDEX FORMAT'
            )

    def reindex_time(self, ind):
        if isinstance(ind, pd.DatetimeIndex):
            try:
                return self.new(self.data.loc[(ind, slice(None)), :])
            except:
                raise RuntimeError('QADATASTRUCT ERROR: CANNOT REINDEX')

        else:
            raise RuntimeError(
                'QADATASTRUCT ERROR: ONLY ACCEPT DATETIME-INDEX FORMAT'
            )

    def locclose(self, codelist, start, end):
        if 'min' in self.type:
            start = parser.parse(start)
            end = parser.parse(end)
        elif 'day' in self.type:
            start = parser.parse(start).date()
            end = parser.parse(end).date()

        return self.closepanel.loc[slice(start, end), codelist]

    def iterrows(self):
        return self.data.iterrows()

    def iteritems(self):
        return self.data.items()

    def itertuples(self):
        return self.data.itertuples()

    def abs(self):
        return self.new(self.data.abs())

    def agg(self, func, axis=0, *args, **kwargs):
        return self.new(self.data.agg(func, axis=0, *args, **kwargs))

    def aggregate(self, func, axis=0, *args, **kwargs):
        return self.new(self.data.aggregate(func, axis=0, *args, **kwargs))

    def tail(self, lens=5):
        """返回最后Lens个值的DataStruct

        Arguments:
            lens {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.new(self.data.tail(lens))

    def head(self, lens=5):
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
        return self.data.reset_index().values.tolist()

    def to_pd(self):
        """
        转换DataStruct为dataframe
        """
        return self.data

    def to_numpy(self):
        """
        转换DataStruct为numpy.ndarray
        """
        return self.data.reset_index().values

    def to_json(self):
        """
        转换DataStruct为json
        """

        data = self.data
        if self.type[-3:] != 'min':
            data = self.data.assign(datetime=self.datetime)
        return QA_util_to_json_from_pandas(data.reset_index())

    def to_string(self):
        return json.dumps(self.to_json())

    def to_bytes(self):
        return bytes(self.to_string(), encoding='utf-8')

    def to_csv(self, *args, **kwargs):
        """datastruct 存本地csv
        """

        self.data.to_csv(*args, **kwargs)

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
        """
        将一个DataStruct按code分解为N个DataStruct
        """
        return list(map(lambda x: self.select_code(x), self.code))

    # def add_func(self, func, *arg, **kwargs):
    #     return pd.concat(list(map(lambda x: func(
    #         self.data.loc[(slice(None), x), :], *arg, **kwargs), self.code))).sort_index()

    def apply(self, func, *arg, **kwargs):
        """func(DataStruct)

        Arguments:
            func {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return func(self, *arg, **kwargs)

    def add_func(self, func, *arg, **kwargs):
        """QADATASTRUCT的指标/函数apply入口

        Arguments:
            func {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.groupby(level=1, sort=False).apply(func, *arg, **kwargs)

    def add_funcx(self, func, *arg, **kwargs):
        """QADATASTRUCT的指标/函数apply入口

        add_funcx 和add_func 的区别是:

        add_funcx 会先 reset_index 变成单索引(pd.DatetimeIndex)
        """

        return self.groupby(
            level=1,
            sort=False
        ).apply(lambda x: func(x.reset_index(1),
                               *arg,
                               **kwargs))

    # def add_func_adv(self, func, *arg, **kwargs):
    #     """QADATASTRUCT的指标/函数apply入口

    #     Arguments:
    #         func {[type]} -- [description]

    #     Returns:
    #         [type] -- [description]
    #     """
    #     return self.data.groupby(by=None, axis=0, level=1, as_index=True, sort=False, group_keys=False, squeeze=False).apply(func, *arg, **kwargs)

    def get_data(self, columns, type='ndarray', with_index=False):
        """获取不同格式的数据

        Arguments:
            columns {[type]} -- [description]

        Keyword Arguments:
            type {str} -- [description] (default: {'ndarray'})
            with_index {bool} -- [description] (default: {False})

        Returns:
            [type] -- [description]
        """

        res = self.select_columns(columns)
        if type == 'ndarray':
            if with_index:
                return res.reset_index().values
            else:
                return res.values
        elif type == 'list':
            if with_index:
                return res.reset_index().values.tolist()
            else:
                return res.values.tolist()
        elif type == 'dataframe':
            if with_index:
                return res.reset_index()
            else:
                return res

    def pivot(self, column_):
        """增加对于多列的支持"""
        if isinstance(column_, str):
            try:
                return self.data.reset_index().pivot(
                    index='datetime',
                    columns='code',
                    values=column_
                )
            except:
                return self.data.reset_index().pivot(
                    index='date',
                    columns='code',
                    values=column_
                )
        elif isinstance(column_, list):
            try:
                return self.data.reset_index().pivot_table(
                    index='datetime',
                    columns='code',
                    values=column_
                )
            except:
                return self.data.reset_index().pivot_table(
                    index='date',
                    columns='code',
                    values=column_
                )

    def selects(self, code, start, end=None):
        """
        选择code,start,end

        如果end不填写,默认获取到结尾

        @2018/06/03 pandas 的索引问题导致
        https://github.com/pandas-dev/pandas/issues/21299

        因此先用set_index去重做一次index
        影响的有selects,select_time,select_month,get_bar

        @2018/06/04
        当选择的时间越界/股票不存在,raise ValueError

        @2018/06/04 pandas索引问题已经解决
        全部恢复
        """

        if 'min' in self.type:
            start = parser.parse(start)
            end = parser.parse(end) if end else end
        elif 'day' in self.type:
            start = parser.parse(start).date()
            end = parser.parse(end).date() if end else end

        def _selects(code, start, end):
            if end is not None:
                return self.data.loc[(slice(start, end), code), :]
            else:
                return self.data.loc[(slice(start, None), code), :]

        try:
            return self.new(_selects(code, start, end), self.type, self.if_fq)
        except:
            raise ValueError(
                'QA CANNOT GET THIS CODE {}/START {}/END{} '.format(
                    code,
                    start,
                    end
                )
            )

    def select_time(self, start, end=None):
        """
        选择起始时间
        如果end不填写,默认获取到结尾

        @2018/06/03 pandas 的索引问题导致
        https://github.com/pandas-dev/pandas/issues/21299

        因此先用set_index去重做一次index
        影响的有selects,select_time,select_month,get_bar

        @2018/06/04
        当选择的时间越界/股票不存在,raise ValueError

        @2018/06/04 pandas索引问题已经解决
        全部恢复
        """

        if 'min' in self.type:
            start = parser.parse(start)
            end = parser.parse(end) if end else end
        elif 'day' in self.type:
            start = parser.parse(start).date()
            end = parser.parse(end).date() if end else end

        def _select_time(start, end):
            if end is not None:
                return self.data.loc[(slice(start, end), slice(None)), :]
            else:
                return self.data.loc[(slice(start, None), slice(None)), :]

        try:
            return self.new(_select_time(start, end), self.type, self.if_fq)
        except:
            raise ValueError(
                'QA CANNOT GET THIS START {}/END{} '.format(start,
                                                            end)
            )

    def select_day(self, day):
        """选取日期(一般用于分钟线)

        Arguments:
            day {[type]} -- [description]

        Raises:
            ValueError -- [description]

        Returns:
            [type] -- [description]
        """

        def _select_day(day):
            return self.data.loc[(day, slice(None)), :]

        try:
            return self.new(_select_day(day), self.type, self.if_fq)
        except:
            raise ValueError('QA CANNOT GET THIS Day {} '.format(day))

    def select_month(self, month):
        """
        选择月份

        @2018/06/03 pandas 的索引问题导致
        https://github.com/pandas-dev/pandas/issues/21299

        因此先用set_index去重做一次index
        影响的有selects,select_time,select_month,get_bar

        @2018/06/04
        当选择的时间越界/股票不存在,raise ValueError

        @2018/06/04 pandas索引问题已经解决
        全部恢复
        """

        def _select_month(month):
            return self.data.loc[month, slice(None)]

        try:
            return self.new(_select_month(month), self.type, self.if_fq)
        except:
            raise ValueError('QA CANNOT GET THIS Month {} '.format(month))

    def select_code(self, code):
        """
        选择股票

        @2018/06/03 pandas 的索引问题导致
        https://github.com/pandas-dev/pandas/issues/21299

        因此先用set_index去重做一次index
        影响的有selects,select_time,select_month,get_bar

        @2018/06/04
        当选择的时间越界/股票不存在,raise ValueError

        @2018/06/04 pandas索引问题已经解决
        全部恢复
        """

        def _select_code(code):
            return self.data.loc[(slice(None), code), :]

        try:
            return self.new(_select_code(code), self.type, self.if_fq)
        except:
            raise ValueError('QA CANNOT FIND THIS CODE {}'.format(code))

    def select_columns(self, columns):
        if isinstance(columns, list):
            columns = columns
        elif isinstance(columns, str):
            columns = [columns]
        else:
            print('wrong columns')

        try:
            return self.data.loc[:, columns]
        except:
            pass

    def select_single_time(self, hour=9, minute=0, second=0):
        """
        选择一个特定的时间点
        """
        return self.data.loc[self.datetime.map(
            lambda x: x.minute == minute and x.hour == hour and x.second ==
            second
        ),
            slice(None)]

    def get_bar(self, code, time):
        """
        获取一个bar的数据
        返回一个series
        如果不存在,raise ValueError
        """
        try:
            return self.data.loc[(pd.Timestamp(time), code)]
        except:
            raise ValueError(
                'DATASTRUCT CURRENTLY CANNOT FIND THIS BAR WITH {} {}'.format(
                    code,
                    time
                )
            )

    def select_time_with_gap(self, time, gap, method):

        if method in ['gt', '>']:

            def gt(data):
                return data.loc[(slice(pd.Timestamp(time), None), slice(None)), :].groupby(level=1, axis=0, as_index=False, sort=False, group_keys=False).apply(lambda x: x.iloc[1:gap+1])

            return self.new(gt(self.data), self.type, self.if_fq)

        elif method in ['gte', '>=']:

            def gte(data):
                return data.loc[(slice(pd.Timestamp(time), None), slice(None)), :].groupby(level=1, axis=0, as_index=False, sort=False, group_keys=False).apply(lambda x: x.iloc[0:gap])

            return self.new(gte(self.data), self.type, self.if_fq)
        elif method in ['lt', '<']:

            def lt(data):
                return data.loc[(slice(None, pd.Timestamp(time)), slice(None)), :].groupby(level=1, axis=0, as_index=False, sort=False, group_keys=False).apply(lambda x: x.iloc[-gap-1:-1])

            return self.new(lt(self.data), self.type, self.if_fq)
        elif method in ['lte', '<=']:

            def lte(data):
                return data.loc[(slice(None, pd.Timestamp(time)), slice(None)), :].groupby(level=1, axis=0, as_index=False, sort=False, group_keys=False).apply(lambda x: x.tail(gap))

            return self.new(lte(self.data), self.type, self.if_fq)
        elif method in ['eq', '==', '=', 'equal', 'e']:

            def eq(data):
                return data.loc[(pd.Timestamp(time), slice(None)), :]

            return self.new(eq(self.data), self.type, self.if_fq)
        else:
            raise ValueError(
                'QA CURRENTLY DONOT HAVE THIS METHODS {}'.format(method)
            )

    def find_bar(self, code, time):
        if len(time) == 10:
            return self.dicts[
                (datetime.datetime.strptime(time,
                                            '%Y-%m-%d'),
                 code)]
        elif len(time) == 19:
            return self.dicts[
                (datetime.datetime.strptime(time,
                                            '%Y-%m-%d %H:%M:%S'),
                 code)]

    def fast_moving(self, pct):
        """bar快速上涨的股票(输入pct 百分比)

        Arguments:
            pct {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.bar_pct_change[self.bar_pct_change > pct].sort_index()
