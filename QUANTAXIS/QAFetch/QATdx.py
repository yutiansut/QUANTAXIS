# coding:utf-8
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
import datetime

import numpy as np
import pandas as pd
from pytdx.hq import TdxHq_API
from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_date_str2int,
                              QA_util_date_valid, QA_util_get_real_date,
                              QA_util_get_real_datelist, QA_util_log_info,
                              QA_util_time_stamp, QA_util_web_ping,
                              trade_date_sse)

# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#

api = TdxHq_API()


def __select_market_code(code):

    return 1 if str(code)[0] == '6' else 0


def QA_fetch_get_stock_day(code, start_date, end_date, ip='119.147.212.81', port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    start_date = QA_util_get_real_date(start_date, trade_date_sse, 1)
    end_date = QA_util_get_real_date(end_date, trade_date_sse, -1)
    with api.connect(ip, port):
        data = []
        for i in range(10):
            data += api.get_security_bars(9,
                                          market_code, code, (9 - i) * 800, 800)
        data = api.to_df(data)
        data['date'] = data['datetime'].apply(lambda x: x[0:10])
        data['date_stamp'] = data['date'].apply(
            lambda x: QA_util_date_stamp(x))
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date', drop=False)
        data['date'] = data['date'].apply(lambda x: str(x)[0:10])
        data = data.drop(['year', 'month', 'day', 'hour',
                          'minute', 'datetime'], axis=1)
        return data[start_date:end_date]


def QAt_stock_list(code, date, ip='119.147.212.81', port=7709):
    with api.co_fetch_gennect(ip, port):
        stocks = api.get_security_list(1, 255)
        return stocks


def QA_fetch_get_stock_realtime(code, ip='119.147.212.81', port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    with api.connect(ip, port):
        __data = api.to_df(api.get_security_quotes([(market_code, code)]))
        data = __data[['code', 'open', 'high', 'low', 'price']]
        data = data.rename(columns={'price': 'close'}, inplace=True)
        return data


def QA_fetch_get_index_day(code, start_date, end_date, ip='119.147.212.81', port=7709):
    api = TdxHq_API()
    start_date = QA_util_get_real_date(start_date, trade_date_sse, 1)
    end_date = QA_util_get_real_date(end_date, trade_date_sse, -1)
    with api.connect(ip, port):
        data = []
        for i in range(10):
            data += api.get_index_bars(9, 1, code, (9 - i) * 800, 800)
        data = api.to_df(data)
        data['date'] = data['datetime'].apply(lambda x: x[0:10])
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date', drop=False)
        data = data.drop(['year', 'month', 'day', 'hour',
                          'minute', 'datetime'], axis=1)

        return data[start_date:end_date]


def QA_fetch_get_stock_min(code, start, end, level, ip='221.231.141.60', port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    if str(level) in ['5', '5m', '5min', 'five']:
        level = 0
    elif str(level) in ['1', '1m', '1min', 'one']:
        level = 8
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level = 1
    elif str(level) in ['30', '30m', '30min', 'half']:
        level = 2
    elif str(level) in ['60', '60m', '60min', '1h']:
        level = 3
    with api.connect(ip, port):
        data = []
        for i in range(26):
            data += api.get_security_bars(level,
                                          market_code, code, (25 - i) * 800, 800)
        data = api.to_df(data)
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['code'] = code
        data = data.set_index('datetime', drop=False)
        data = data.drop(['year', 'month', 'day', 'hour',
                          'minute'], axis=1)
        data['datetime'] = data['datetime'].apply(lambda x: str(x)[0:19])
        data['date'] = data['datetime'].apply(lambda x: str(x)[0:10])
        data['date_stamp'] = data['date'].apply(
            lambda x: QA_util_date_stamp(x))
        data['time_stamp'] = data['datetime'].apply(
            lambda x: QA_util_time_stamp(x))
    return data[start:end]


def __QA_fetch_get_stock_transaction(code, day, retry, api):
    market_code = __select_market_code(code)
    data_ = []
    for i in range(21):
        data_ += api.get_history_transaction_data(
            market_code, code, (20 - i) * 800, 800, QA_util_date_str2int(day))
    data_ = api.to_df(data_)
    data_['date'] = day
    data_['datetime'] = data_['time'].apply(lambda x: str(day) + ' ' + x)
    data_['datetime'] = pd.to_datetime(data_['datetime'])
    data_['code'] = str(code)
    data_['order'] = range(len(data_.index))
    data_ = data_.set_index('datetime', drop=True)

    for _ in range(retry):
        if len(data_) < 2:
            return __QA_fetch_get_stock_transaction(code, day, 0, api)
        else:
            return data_


def QA_fetch_get_stock_transaction(code, start, end, retry=2, ip='221.231.141.60', port=7709):
    api = TdxHq_API()

    real_start, real_end = QA_util_get_real_datelist(start, end)
    real_id_range = []
    with api.connect():
        data = pd.DataFrame()
        for index_ in range(trade_date_sse.index(real_start), trade_date_sse.index(real_end) + 1):

            try:
                data_ = __QA_fetch_get_stock_transaction(
                    code, trade_date_sse[index_], retry, api)
                if len(data_) < 1:
                    return None
            except:
                QA_util_log_info('Wrong in Getting %s history transaction data in day %s' % (
                    code, trade_date_sse[index_]))
            else:
                QA_util_log_info('Successfully Getting %s history transaction data in day %s' % (
                    code, trade_date_sse[index_]))
                data = data.append(data_)

        return data


def QA_fetch_get_stock_info():
    pass


def QA_fetch_get_stock_xdxr(code, ip='221.231.141.60', port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    with api.connect():
        return api.to_df(api.get_xdxr_info(market_code, code))


if __name__ == '__main__':
    # print(QA_fetch_get_stock_day('000001','2017-07-03','2017-07-10'))
    #print(QA_fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
    # print(QA_fetch_get_stock_realtime('000001'))
    print(QA_fetch_get_index_day('000001', '2017-01-01', '2017-07-01'))
    #print(QA_fetch_get_stock_transaction('000001', '2017-07-03', '2017-07-10'))
