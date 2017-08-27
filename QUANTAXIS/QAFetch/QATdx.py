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


def ping(ip):
    __time1 = datetime.datetime.now()
    api = TdxHq_API()
    try:
        with api.connect(ip, 7709):
            api.get_security_bars(9, 0, '000001', 0, 1)
        return float(datetime.datetime.now() - x1)
    except:
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    listx = ['180.153.18.170', '180.153.18.171', '202.108.253.130', '202.108.253.131', '60.191.117.167', '115.238.56.198', '218.75.126.9', '115.238.90.165',
             '124.160.88.183', '60.12.136.250', '218.108.98.244', '218.108.47.69', '14.17.75.71', '180.153.39.51']
    data = [ping(x) for x in listx]
    return listx[data.index(min(data))]


def __select_market_code(code):

    return 1 if str(code)[0] == '6' else 0


def QA_fetch_get_stock_day(code, start_date, end_date, if_fq='00', ip=select_best_ip(), port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    if if_fq in ['00', 'bfq']:
        with api.connect(ip, port):
            data = []
            for i in range(10):
                data += api.get_security_bars(9,
                                              market_code, code, (9 - i) * 800, 800)
            data = api.to_df(data)
            data['date'] = data['datetime'].apply(lambda x: x[0:10])
            data['code'] = code
            data['date_stamp'] = data['date'].apply(
                lambda x: QA_util_date_stamp(x))
            data['date'] = pd.to_datetime(data['date'])
            data = data.set_index('date', drop=False)
            data['date'] = data['date'].apply(lambda x: str(x)[0:10])
            data = data.drop(['year', 'month', 'day', 'hour',
                              'minute', 'datetime'], axis=1)
            return data[data['open'] != 0][start_date:end_date]
    elif if_fq in ['01', 'qfq']:
        xdxr_data = QA_fetch_get_stock_xdxr(code)
        info = xdxr_data[xdxr_data['category'] == 1]

        with api.connect(ip, port):
            data = []
            for i in range(10):
                data += api.get_security_bars(9,
                                              market_code, code, (9 - i) * 800, 800)
            data = api.to_df(data)
            data['code'] = code
            data['date'] = data['datetime'].apply(lambda x: x[0:10])
            data['date_stamp'] = data['date'].apply(
                lambda x: QA_util_date_stamp(x))
            data['date'] = pd.to_datetime(data['date'])
            data = data.set_index('date', drop=False)
            data['date'] = data['date'].apply(lambda x: str(x)[0:10])
            data = data.drop(['year', 'month', 'day', 'hour',
                              'minute', 'datetime'], axis=1)
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][data.index[0]:]], axis=1).fillna(0)
            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1)[::-1].cumprod()
            data['open'] = data['open'] * data['adj']
            data['high'] = data['high'] * data['adj']
            data['low'] = data['low'] * data['adj']
            data['close'] = data['close'] * data['adj']
            data['preclose'] = data['preclose'] * data['adj']
            return data[data['open'] != 0][start_date:end_date]
    elif if_fq in ['02', 'hfq']:
        xdxr_data = QA_fetch_get_stock_xdxr(code)
        info = xdxr_data[xdxr_data['category'] == 1]

        with api.connect(ip, port):
            data = []
            for i in range(10):
                data += api.get_security_bars(9,
                                              market_code, code, (9 - i) * 800, 800)
            data = api.to_df(data)
            data['date'] = data['datetime'].apply(lambda x: x[0:10])
            data['code'] = code
            data['date_stamp'] = data['date'].apply(
                lambda x: QA_util_date_stamp(x))
            data['date'] = pd.to_datetime(data['date'])
            data = data.set_index('date', drop=False)
            data['date'] = data['date'].apply(lambda x: str(x)[0:10])
            data = data.drop(['year', 'month', 'day', 'hour',
                              'minute', 'datetime'], axis=1)

            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][data.index[0]:]], axis=1).fillna(0)
            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1).cumprod()
            data['open'] = data['open'] / data['adj']
            data['high'] = data['high'] / data['adj']
            data['low'] = data['low'] / data['adj']
            data['close'] = data['close'] / data['adj']
            data['preclose'] = data['preclose'] / data['adj']
            return data[data['open'] != 0][start_date:end_date]


def QA_fetch_get_stock_latest(code, ip=select_best_ip(), port=7709):
    code = [code] if isinstance(code, str) else code
    api = TdxHq_API(multithread=True)
    with api.connect(ip, port):
        data = pd.DataFrame()
        for item in code:
            market_code = __select_market_code(item)
            __data = api.to_df(api.get_security_bars(
                9, market_code, item, 0, 1))
            __data['code'] = item
            print(item)
            data = data.append(__data)
        data['date'] = data['datetime'].apply(lambda x: x[0:10])
        data['date_stamp'] = data['date'].apply(
            lambda x: QA_util_date_stamp(x))
        data['date'] = pd.to_datetime(data['date'])
        data = data.set_index('date', drop=False)
        data['date'] = data['date'].apply(lambda x: str(x)[0:10])
        data = data.drop(['year', 'month', 'day', 'hour',
                          'minute', 'datetime'], axis=1)
        return data


def QA_fetch_get_stock_list(code, date, ip=select_best_ip(), port=7709):
    with api.connect(ip, port):
        stocks = api.get_security_list(1, 255)
        return stocks


def QA_fetch_get_stock_realtime(code=['000001', '000002'], ip=select_best_ip(), port=7709):
    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if type(code) is str else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(__select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
        data = __data[['datetime', 'code', 'open', 'high', 'low', 'price']]
        data = data.set_index('code', drop=False)

        return data


def QA_fetch_get_index_day(code, start_date, end_date, ip=select_best_ip(), port=7709):
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


def QA_fetch_get_stock_min(code, start, end, level, ip=select_best_ip(), port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    type_ = ''
    if str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'
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
        data['type'] = type_
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


def QA_fetch_get_stock_transaction(code, start, end, retry=2, ip=select_best_ip(), port=7709):
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


def QA_fetch_get_stock_xdxr(code, ip=select_best_ip(), port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    with api.connect():
        """
        1 除权除息 002175 2008-05-29
        2 送配股上市  000656 2015-04-29
        3 非流通股上市 000656 2010-02-10
        4 未知股本变动 600642 1993-07-19
        5 股本变化 000656 2017-06-30
        6 增发新股 600887 2002-08-20
        7 股份回购  600619 2000-09-08
        8 增发新股上市 600186 2001-02-14
        9 转配股上市 600811 2017-07-25
        10 可转债上市 600418 2006-07-07
        11 扩缩股  600381 2014-06-27
        12 非流通股缩股 600339 2006-04-10
        13 送认购权证 600008 2006-04-19
        14 送认沽权证 000932 2006-03-01
        """
        category = {
            '1': '除权除息', '2': '送配股上市', '3': '非流通股上市', '4': '未知股本变动', '5': '股本变化',
            '6': '增发新股', '7': '股份回购', '8': '增发新股上市', '9': '转配股上市', '10': '可转债上市',
            '11': '扩缩股', '12': '非流通股缩股', '13':  '送认购权证', '14': '送认沽权证'}
        data = api.to_df(api.get_xdxr_info(market_code, code))
        data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
        data = data.drop(['year', 'month', 'day'], axis=1)
        data['category_meaning'] = data['category'].apply(
            lambda x: category[str(x)])
        data['code'] = code
        data = data.set_index('date', drop=False)
        return data


if __name__ == '__main__':
    # print(QA_fetch_get_stock_day('000001','2017-07-03','2017-07-10'))
    #print(QA_fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
    # print(QA_fetch_get_stock_realtime('000001'))
    print(QA_fetch_get_index_day('000001', '2017-01-01', '2017-07-01'))
    #print(QA_fetch_get_stock_transaction('000001', '2017-07-03', '2017-07-10'))
