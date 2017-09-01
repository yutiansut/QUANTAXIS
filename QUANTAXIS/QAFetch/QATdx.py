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
import tushare as ts
from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_date_str2int,
                              QA_util_date_valid, QA_util_get_real_date,
                              QA_util_get_real_datelist, QA_util_log_info,
                              QA_util_time_stamp, QA_util_web_ping,
                              trade_date_sse)

# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#


def ping(ip):
    api = TdxHq_API()
    __time1 = datetime.datetime.now()
    try:
        with api.connect(ip, 7709):
            api.get_security_bars(9, 0, '000001', 0, 1)
        return datetime.datetime.now() - __time1
    except:
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    QA_util_log_info('Selecting the Best Server IP of TDX')
    listx = ['180.153.18.170', '180.153.18.171', '202.108.253.130', '202.108.253.131',
             '60.191.117.167', '115.238.56.198', '218.75.126.9', '115.238.90.165',
             '124.160.88.183', '60.12.136.250', '218.108.98.244', '218.108.47.69',
             '14.17.75.71', '180.153.39.51']
    data = [ping(x) for x in listx]
    QA_util_log_info('===The BEST SERVER is :  %s ===' %
                     (listx[data.index(min(data))]))
    return listx[data.index(min(data))]


best_ip = select_best_ip()


def __select_market_code(code):

    return 1 if str(code)[0] == '6' else 0


def QA_fetch_get_stock_day(code, start_date, end_date, if_fq='00', ip=best_ip, port=7709):
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
            data.set_index('date', drop=False, inplace=True)
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
            data.set_index('date', drop=False, inplace=True)
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
            data.set_index('date', drop=False, inplace=True)
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


def QA_fetch_get_stock_latest(code, ip=best_ip, port=7709):
    code = [code] if isinstance(code, str) else code
    api = TdxHq_API(multithread=True)
    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_security_bars(
            9, __select_market_code(item), item, 0, 1)).assign(code=item) for item in code], axis=0)
        return data\
            .assign(date=pd.to_datetime(data['datetime']
                                        .apply(lambda x: x[0:10])), date_stamp=data['datetime']
                    .apply(lambda x: QA_util_date_stamp(str(x[0:10]))))\
            .set_index('date', drop=False)\
            .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)


def QA_fetch_get_stock_realtime(code=['000001', '000002'], ip=best_ip, port=7709):
    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if type(code) is str else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(__select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
        data = __data[['datetime', 'code', 'open', 'high', 'low', 'price']]
        return data.set_index('code', drop=False, inplace=False)


def QA_fetch_get_stock_list(ip=best_ip, port=7709):
    api = TdxHq_API()
    with api.connect(ip, port):
        return pd.concat([pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(sse='sh' if j == 0 else 'sz') for i in range(int(api.get_security_count(j) / 1000) + 1)], axis=0) for j in range(2)], axis=0)


def QA_fetch_get_index_day(code, start_date, end_date, ip=best_ip, port=7709):
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_index_bars(
            9, 1, code, (9 - i) * 800, 800)) for i in range(10)], axis=0)

        return data.assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10]))).set_index('date', drop=False, inplace=False).drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1, inplace=False)[start_date:end_date]


def QA_fetch_get_index_min(code, start, end, level='1min', ip=best_ip, port=7709):
    api = TdxHq_API()
    #market_code = __select_market_code(code)
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
        data = pd.DataFrame()
        for i in range(26):
            data = data.append(api.to_df(api.get_index_bars(
                level, 1, code, (25 - i) * 800, 800)))
        print(data)
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['code'] = code
        data = data.drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                         inplace=False).set_index('datetime', drop=False, inplace=False)
        data['datetime'] = data['datetime'].apply(lambda x: str(x)[0:19])
        data['date'] = data['datetime'].apply(lambda x: str(x)[0:10])
        data['date_stamp'] = data['date'].apply(
            lambda x: QA_util_date_stamp(x))
        data['time_stamp'] = data['datetime'].apply(
            lambda x: QA_util_time_stamp(x))
        data['type'] = type_
        print(data)
        return data[start:end]


def QA_fetch_get_stock_min(code, start, end, level='1min', ip=best_ip, port=7709):
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

        data = pd.concat([api.to_df(api.get_security_bars(level,
                                                          market_code, code, (25 - i) * 800, 800)) for i in range(26)], axis=0)
        return data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=code)\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .set_index('datetime', drop=False, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=QA_util_date_stamp(data['datetime'].apply(lambda x: str(x)[0:10])))\
            .assign(time_stamp=data['datetime'].apply(lambda x: QA_util_time_stamp(x)))\
            .assign(type=type_)[start:end]


def __QA_fetch_get_stock_transaction(code, day, retry, api):
    data_ = pd.concat([api.to_df(api.get_history_transaction_data(
        __select_market_code(code), code, (20 - i) * 800, 800, QA_util_date_str2int(day))) for i in range(21)], axis=0)

    for _ in range(retry):
        if len(data_) < 2:
            return __QA_fetch_get_stock_transaction(code, day, 0, api)
        else:
            return data_.assign(date=day).assign(datetime=pd.to_datetime(data_['time'].apply(lambda x: str(day) + ' ' + x)))\
                        .assign(code=str(code)).assign(order=range(len(data_.index))).set_index('datetime', drop=False, inplace=False)


def QA_fetch_get_stock_transaction(code, start, end, retry=2, ip=best_ip, port=7709):
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


def QA_fetch_get_stock_xdxr(code, ip=best_ip, port=7709):
    api = TdxHq_API()
    market_code = __select_market_code(code)
    with api.connect():
        category = {
            '1': '除权除息', '2': '送配股上市', '3': '非流通股上市', '4': '未知股本变动', '5': '股本变化',
            '6': '增发新股', '7': '股份回购', '8': '增发新股上市', '9': '转配股上市', '10': '可转债上市',
            '11': '扩缩股', '12': '非流通股缩股', '13':  '送认购权证', '14': '送认沽权证'}
        data = api.to_df(api.get_xdxr_info(market_code, code))
        return data\
            .assign(date=pd.to_datetime(data[['year', 'month', 'day']]))\
            .drop(['year', 'month', 'day'], axis=1)\
            .assign(category_meaning=data['category'].apply(lambda x: category[str(x)]))\
            .assign(code=str(code))\
            .rename(index=str, columns={'panhouliutong': 'liquidity_after',
                                        'panqianliutong': 'liquidity_before', 'houzongguben': 'shares_after',
                                        'qianzongguben': 'shares_before'})\
            .set_index('date', drop=False, inplace=False)


if __name__ == '__main__':
    # print(QA_fetch_get_stock_day('000001','2017-07-03','2017-07-10'))
    #print(QA_fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
    # print(QA_fetch_get_stock_realtime('000001'))
    print(QA_fetch_get_index_day('000001', '2017-01-01', '2017-07-01'))
    #print(QA_fetch_get_stock_transaction('000001', '2017-07-03', '2017-07-10'))
