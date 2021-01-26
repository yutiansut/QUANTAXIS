# coding :utf-8
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

"""
指标结构

"""
import pandas as pd


class QA_DataStruct_Indicators():
    """
    指标的结构
    """

    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return '< QA_DATASTRUCT_INDICATOR FROM {} TO {} WITH {} CODES >'.format(self.data.index.levels[0][0], self.data.index.levels[0][-1], len(self.data.index.levels[1]))

    @property
    def index(self):
        return self.data.index

    def get_indicator(self, time, code, indicator_name=None):
        """
        获取某一时间的某一只股票的指标
        """
        try:
            return self.data.loc[(pd.Timestamp(time), code), indicator_name]
        except:
            raise ValueError('CANNOT FOUND THIS DATE&CODE')

    def get_code(self, code):
        """
        获取某一只股票的指标序列
        """
        try:
            return self.data.loc[(slice(None), code), :]
        except:
            return ValueError('CANNOT FOUND THIS CODE')

    def get_timerange(self, start, end, code=None):
        """
        获取某一段时间的某一只股票的指标
        """
        try:
            if code is None:
                #  code为空时 返回start ～end之间的所有数据
                return self.data.loc[(slice(pd.Timestamp(start), pd.Timestamp(end))), :]
            else:
                return self.data.loc[(slice(pd.Timestamp(start), pd.Timestamp(end)), code), :]
        except:
            return ValueError('CANNOT FOUND THIS TIME RANGE')

    def groupby(self, by=None, axis=0, level=None, as_index=True, sort=False, group_keys=True, squeeze=False, **kwargs):
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
        return self.data.groupby(by=by, axis=axis, level=level, as_index=as_index, sort=sort, group_keys=group_keys, squeeze=squeeze)

    def add_func(self, func, *args, **kwargs):
        return self.groupby(level=1, as_index=False, group_keys=False).apply(func, raw=True, *args, **kwargs)
