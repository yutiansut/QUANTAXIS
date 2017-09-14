# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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

import json

import numpy as np
import pandas as pd

from .QADate_trade import QA_util_if_trade, trade_date_sse, QA_util_get_real_datelist, QA_util_get_trade_range


def QA_util_make_min_index(day, type_='1min'):
    if QA_util_if_trade(day) is True:
        return pd.date_range(str(day) + ' 09:30:00', str(day) + ' 11:30:00', freq=type_, closed='right').append(
                                pd.date_range(str(day) + ' 13:00:00', str(day) + ' 15:00:00', freq=type_, closed='right'))
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_hour_index(day, type_='1h'):
    if QA_util_if_trade(day) is True:
        return pd.date_range(str(day) + '09:30:00', str(day) + ' 11:30:00', freq=type_, closed='right').append(
                                pd.date_range(str(day) + ' 13:00:00', str(day) + ' 15:00:00', freq=type_, closed='right'))
    else:
        return pd.DataFrame(['No trade'])


if __name__ == '__main__':
    pass
