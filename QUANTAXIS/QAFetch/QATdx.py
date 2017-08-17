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
import numpy as np
import pandas as pd
from pytdx.hq import TdxHq_API
from QUANTAXIS.QAUtil import (QA_util_date_valid, QA_util_log_info, QA_util_get_real_date,
                              QA_util_web_ping, trade_date_sse, QA_util_get_real_datelist)
import datetime
# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#

api = TdxHq_API()


def __select_market_code(code):

    market_code = 0

    if str(code)[0] == '6':
        # 0 - 深圳， 1 - 上海
        return 1
    else:
        return 0


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
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date')
        data = data.drop(['year', 'month', 'day', 'hour',
                          'minute', 'datetime'], axis=1)

        return data[start_date:end_date]


def QA_fetch_get_stock_list(code, date, ip='119.147.212.81', port=7709):
    with api.connect(ip, port):
        stocks = api.get_security_list(1, 255)
        return stocks


def QA_fetch_get_stock_realtime(code, date, ip='119.147.212.81', port=7709):
    with api.connect(ip, port):
        stocks = api.get_security_quotes([(0, "000001")])
        return stocks


def QA_fetch_get_index_day(code, date, ip='119.147.212.81', port=7709):
    with api.connect(ip, port):
        stocks = api.get_index_bars(9, 1, '000001', 1, 2)
    return stocks


def QA_fetch_get_stock_min(code, start, end, level, ip='119.147.212.81', port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)

    with api.connect(ip, port):
        data = []
        for i in range(25):
            data += api.get_security_bars(8, market_code,
                                          code, (25 - i) * 800, 800)
        data = api.to_df(data)

        data['datetime'] = pd.to_datetime(data['datetime'])
        data = data.set_index('datetime')

    return data[start:end]


def QA_fetch_get_stock_min(code, start, end, level, ip='119.147.212.81', port=7709):
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
        data = data.set_index('datetime')

    return data[start:end]


def QA_fetch_get_stock_transaction(code, start, end, ip='119.147.212.81', port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)

    real_start, real_end = QA_util_get_real_datelist(start, end)
    real_id_range = []
    with api.connect(ip, port):
        data = pd.DataFrame()

        for index_ in range(trade_date_sse.index(real_start), trade_date_sse.index(real_end) + 1):
            data_ = []
            print(trade_date_sse[index_])
            for i in range(25):
                data_ += api.to_df(api.get_history_transaction_data(market_code,
                                                                    code, (25 - i) * 800, 800, trade_date_sse[index_]))
            data_ = api.to_df(data_)
            data_['date'] = trade_date_sse[index_]

            #data_['datetime'] = pd.to_datetime(data_['datetime'])
            data_ = data_.set_index('date')
            data.append(data_)
    return data


if __name__ == '__main__':
    # print(QA_fetch_get_stock_day('000001','2017-07-03','2017-07-10'))
    #print(QA_fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
