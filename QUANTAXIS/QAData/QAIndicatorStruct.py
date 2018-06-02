# coding :utf-8
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
        return '< QA_DATASTRUCT_INDICATOR FROM {} TO {} WITH {} CODES >'.format(self.data.index.levels[0][0],self.data.index.levels[0][-1],len(self.data.index.levels[1]))

    def get_indicator(self, time, code, indicator_name=None):
        """
        获取某一时间的某一只股票的指标
        """
        try:
            return self.data.loc[(pd.Timestamp(time), code),slice(indicator_name)]
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
            return self.data.loc[(slice(pd.Timestamp(start), pd.Timestamp(end)), slice(code)), :]
        except:
            return ValueError('CANNOT FOUND THIS TIME RANGE')
