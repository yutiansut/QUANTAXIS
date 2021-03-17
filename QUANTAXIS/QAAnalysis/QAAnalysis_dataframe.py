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


import statistics
from functools import lru_cache


#import scipy
#import statsmodels
#from scipy import integrate, optimize, stats

#from QUANTAXIS.QAData.QADataStruct import QA_DataStruct_Index_day,QA_DataStruct_Index_min,QA_DataStruct_Stock_day,QA_DataStruct_Stock_min


class QAAnalysis_stock():
    """
    行情分析器

    计算所有的指标

    """

    def __init__(self, dataStruct, *args, **kwargs):
        try:
            # 如果是QA_Data_系列
            self.data = dataStruct.data
            self._data = dataStruct
        except AttributeError:
            # 如果是dataframe
            self.data = dataStruct

        # self.data=DataSturct.data

    def __repr__(self):
        return '< QAAnalysis_Stock >'

    def __call__(self):
        return self.data

    # 使用property进行懒运算

    @property
    def open(self):
        return self.data['open']

    @property
    def high(self):
        return self.data['high']

    @property
    def low(self):
        return self.data['low']

    @property
    def close(self):
        return self.data['close']

    @property
    def vol(self):
        if 'volume' in self.data.columns:
            return self.data['volume']
        else:
            return self.data['vol']

    @property
    def volume(self):
        if 'volume' in self.data.columns:
            return self.data['volume']
        else:
            return self.data['vol']

    @property
    def date(self):

        return self.data.index.levels[self.data.index.names.index(
            'date')] if 'date' in self.data.index.names else self.data['date']

    @property
    def datetime(self):

        return self.data.index.levels[self.data.index.names.index(
            'datetime')] if 'datetime' in self.data.index.names else self.data.index.levels[self.data.index.names.index(
                'date')]

    @property
    def index(self):
        return self.data.index

    # 均价
    @property
    def price(self):
        return 0.25 * (self.open + self.close + self.high + self.low)

    @property
    def max(self):
        return self.price.max()

    @property
    def min(self):
        return self.price.min()

    @property
    def mean(self):
        return self.price.mean()
    # 一阶差分序列

    @property
    def price_diff(self):
        return self.price.diff(1)

    # 样本方差(无偏估计) population variance
    @property
    def pvariance(self):
        return statistics.pvariance(self.price)

    # 方差
    @property
    def variance(self):

        return statistics.variance(self.price)
    # 标准差

    @property
    def day_pct_change(self):
        return (self.open - self.close) / self.open

    @property
    def stdev(self):

        return statistics.stdev(self.price)
    # 样本标准差

    @property
    def pstdev(self):
        return statistics.pstdev(self.price)

    # 调和平均数
    @property
    def mean_harmonic(self):
        return statistics.harmonic_mean(self.price)

    # 众数
    @property
    def mode(self):
        return statistics.mode(self.price)

    # 波动率

    # 振幅
    @property
    def amplitude(self):
        return self.max - self.min
    # 偏度 Skewness

    @property
    def skewnewss(self):
        return self.price.skew()
    # 峰度Kurtosis

    @property
    def kurtosis(self):
        return self.price.kurt()
    # 百分数变化

    @property
    def pct_change(self):
        return self.price.pct_change()

    # 平均绝对偏差
    @property
    def mad(self):
        return self.price.mad()

    # 函数 指标计算
    @lru_cache()
    def add_func(self, func, *arg, **kwargs):
        return func(self.data, *arg, **kwargs)


def shadow_calc(data):
    """
    explanation:
        计算上下影线		

    params:
        * data ->:
            meaning: 行情切片
            type: DataStruct.slice
            optional: [null]

    return:
        (up_shadow: 上影线, down_shdow: 下影线, entity: 实体部分, date:时间, code: 代码)

    demonstrate:
        Not described

    output:
        Not described
    """

    up_shadow = abs(data.high - (max(data.open, data.close)))
    down_shadow = abs(data.low - (min(data.open, data.close)))
    entity = abs(data.open - data.close)
    towards = True if data.open < data.close else False
    print('=' * 15)
    print('up_shadow : {}'.format(up_shadow))
    print('down_shadow : {}'.format(down_shadow))
    print('entity: {}'.format(entity))
    print('towards : {}'.format(towards))
    return up_shadow, down_shadow, entity, data.date, data.code


class shadow():
    def __init__(self, data):
        self.data = data

    def shadow_panel(self):
        return
