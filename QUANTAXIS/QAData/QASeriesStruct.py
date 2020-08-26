# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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
from copy import deepcopy

import numpy as np
import pandas as pd


class QA_DataStruct_Series():
    def __init__(self, series):
        self.series = series.sort_index()

        if isinstance(series.index, pd.core.indexes.multi.MultiIndex):
            self.if_multiindex=True
            self.index = series.index.remove_unused_levels()
        else:
            self.if_multiindex=False
            self.index = series.index

    def __repr__(self):
        return '< QA_DATASTRUCT_SEIRES >'

    def __call__(self):
        return self.series

    @property
    def code(self):
        if self.if_multiindex:
            return self.index.levels[1].tolist()
        else:
            return None

    @property
    def datetime(self):
        if self.if_multiindex:
            return self.index.levels[0].tolist()
        elif (self.index,pd.core.indexes.datetimes.DatetimeIndex):
            return self.index
        else:
            return None

    @property
    def date(self):
        if self.if_multiindex:
            return np.unique(self.index.levels[0].date).tolist()
        elif (self.index,pd.core.indexes.datetimes.DatetimeIndex):
            return np.unique(self.index.date).tolist()
        else:
            return None

    def new(self, series):
        temp = deepcopy(self)
        temp.__init__(series)
        return temp

    def select_code(self, code):
        return self.new(self.series.loc[(slice(None), code)])

    def select_time(self, start, end=None):
        if end is None:
            return self.new(self.series.loc[(pd.Timestamp(start), slice(None))])
        else:
            return self.new(self.series.loc[(slice(pd.Timestamp(start), pd.Timestamp(end)), slice(None))])
