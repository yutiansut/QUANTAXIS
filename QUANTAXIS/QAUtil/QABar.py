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


def QA_util_make_bar(type, start, end=None):
    '综合性入口'
    if end is None:
        # 1day

        if str(type) in ['1min', '1m']:
            return QA_util_make_1min_bar(start)
        elif str(type) in ['5min', '5m']:
            return QA_util_make_5min_bar(start)
        elif str(type) in ['15min', '15m']:
            return QA_util_make_15min_bar(start)
        elif str(type) in ['30min', '30m']:
            return QA_util_make_30min_bar(start)
        elif str(type) in ['1h', '60min', '60m']:
            return QA_util_make_30min_bar(start)
    else:
        start, end = QA_util_get_real_datelist(start, end)
        range_ = QA_util_get_trade_range(start, end)
        #print(range_)
        data = pd.DataFrame()
        for item in range_:
            if str(type) in ['1min', '1m']:
                data=data.append(QA_util_make_1min_bar(item))
            elif str(type) in ['5min', '5m']:
                data=data.append(QA_util_make_5min_bar(item))
            elif str(type) in ['15min', '15m']:
                data=data.append(QA_util_make_15min_bar(item))
            elif str(type) in ['30min', '30m']:
                data=data.append(QA_util_make_30min_bar(item))
            elif str(type) in ['1h', '60min', '60m']:
                data=data.append(QA_util_make_30min_bar(item))
        return data

        # date range


def QA_util_make_1min_bar(day):
    if QA_util_if_trade(day) is True:
        return pd.DataFrame(data=None,
                            index=pd.date_range(str(day) + ' 09:31:00', str(day) + ' 11:30:00', freq='1min').append(
                                pd.date_range(str(day) + ' 13:01:00', str(day) + ' 15:00:00', freq='1min')),
                            columns=['open', 'high', 'low', 'close', 'volume'])
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_5min_bar(day):
    if QA_util_if_trade(day) is True:
        return pd.DataFrame(data=None,
                            index=pd.date_range(str(day) + ' 09:35:00', str(day) + ' 11:30:00', freq='5min').append(
                                pd.date_range(str(day) + ' 13:05:00', str(day) + ' 15:00:00', freq='5min')),
                            columns=['open', 'high', 'low', 'close', 'volume'])
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_15min_bar(day):
    if QA_util_if_trade(day) is True:
        return pd.DataFrame(data=None,
                            index=pd.date_range(str(day) + ' 09:45:00', str(day) + ' 11:30:00', freq='15min').append(
                                pd.date_range(str(day) + ' 13:15:00', str(day) + ' 15:00:00', freq='15min')),
                            columns=['open', 'high', 'low', 'close', 'volume'])
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_30min_bar(day):
    if QA_util_if_trade(day) is True:
        return pd.DataFrame(data=None,
                            index=pd.date_range(str(day) + ' 10:00:00', str(day) + ' 11:30:00', freq='30min').append(
                                pd.date_range(str(day) + ' 13:30:00', str(day) + ' 15:00:00', freq='30min')),
                            columns=['open', 'high', 'low', 'close', 'volume'])
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_1h_bar(day):
    if QA_util_if_trade(day) is True:
        return pd.DataFrame(data=None,
                            index=pd.date_range(str(day) + ' 10:30:00', str(day) + ' 11:30:00', freq='1h').append(
                                pd.date_range(str(day) + ' 14:00:00', str(day) + ' 15:00:00', freq='1h')),
                            columns=['open', 'high', 'low', 'close', 'volume'])
    else:
        return pd.DataFrame(['No trade'])


if __name__ == '__main__':
    print(QA_util_make_1h_bar('2016-07-01'))
