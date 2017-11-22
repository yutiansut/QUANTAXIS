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
import math
import datetime
import time
import numpy as np
import pandas as pd
from QUANTAXIS.QAUtil.QADate_trade import (QA_util_get_real_datelist, QA_util_date_gap,
                                           QA_util_get_trade_range,
                                           QA_util_if_trade, trade_date_sse)


def QA_util_make_min_index(day, type_='1min'):
    if QA_util_if_trade(day) is True:
        return pd.date_range(str(day) + ' 09:30:00', str(day) + ' 11:30:00', freq=type_, closed='right').append(
            pd.date_range(str(day) + ' 13:00:00', str(day) + ' 15:00:00', freq=type_, closed='right'))
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_hour_index(day, type_='1h'):
    if QA_util_if_trade(day) is True:
        return pd.date_range(str(day) + ' 09:30:00', str(day) + ' 11:30:00', freq=type_, closed='right').append(
            pd.date_range(str(day) + ' 13:00:00', str(day) + ' 15:00:00', freq=type_, closed='right'))
    else:
        return pd.DataFrame(['No trade'])


def QA_util_time_gap(time, gap, methods, type_):

    '分钟线回测的时候的gap'
    min_len = int(240 / int(str(type_).split('min')[0]))
    day_gap = math.ceil(gap / min_len)

    if methods in ['>', 'gt']:
        data = pd.concat([pd.DataFrame(QA_util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())):trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date())) + day_gap+1]]).reset_index()
        return np.asarray(data[data[0] > time].head(gap)[0].apply(lambda x: str(x))).tolist()[-1]
    elif methods in ['>=', 'gte']:
        data = pd.concat([pd.DataFrame(QA_util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())):trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date())) + day_gap+1]]).reset_index()

        return np.asarray(data[data[0] >= time].head(gap)[0].apply(lambda x: str(x))).tolist()[-1]
    elif methods in ['<', 'lt']:
        data = pd.concat([pd.DataFrame(QA_util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())) - day_gap:trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date()))+1]]).reset_index()

        return np.asarray(data[data[0] < time].tail(gap)[0].apply(lambda x: str(x))).tolist()[0]
    elif methods in ['<=', 'lte']:
        data = pd.concat([pd.DataFrame(QA_util_make_min_index(day, type_)) for day in trade_date_sse[trade_date_sse.index(str(datetime.datetime.strptime(
            time, '%Y-%m-%d %H:%M:%S').date())) - day_gap:trade_date_sse.index(str(datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date()))+1]]).reset_index()

        return np.asarray(data[data[0] <= time].tail(gap)[0].apply(lambda x: str(x))).tolist()[0]
    elif methods in ['==', '=', 'eq']:
        return time


if __name__ == '__main__':
    pass
