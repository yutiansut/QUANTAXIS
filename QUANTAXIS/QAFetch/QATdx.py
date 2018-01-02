# coding:utf-8
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
import datetime

import numpy as np
import pandas as pd
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API

from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_date_str2int,
                              QA_util_date_valid, QA_util_get_real_date,
                              QA_util_get_real_datelist, QA_util_get_trade_gap,
                              QA_util_log_info, QA_util_time_stamp,
                              QA_util_web_ping, future_ip_list, stock_ip_list,
                              trade_date_sse)

# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#


def ping(ip, type_='stock'):
    api = TdxHq_API()
    apix = TdxExHq_API()
    __time1 = datetime.datetime.now()
    try:
        if type_ in ['stock']:
            with api.connect(ip, 7709, time_out=0.7):
                if len(api.get_security_list(0, 1)) > 800:
                    return datetime.datetime.now() - __time1
                else:
                    print('Bad STOCKIP REPSONSE %s' % ip)
                    return datetime.timedelta(9, 9, 0)
        elif type_ in ['future']:
            with apix.connect(ip, 7727, time_out=0.7):
                if apix.get_instrument_count() > 40000:
                    return datetime.datetime.now() - __time1
                else:
                    print('Bad FUTUREIP REPSONSE %s' % ip)
                    return datetime.timedelta(9, 9, 0)
    except:
        print('Bad REPSONSE %s' % ip)
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    QA_util_log_info('Selecting the Best Server IP of TDX')

    data_stock = [ping(x, 'stock') for x in stock_ip_list]
    data_future = [ping(x, 'future') for x in future_ip_list]

    best_stock_ip = stock_ip_list[data_stock.index(min(data_stock))]
    best_future_ip = future_ip_list[data_future.index(min(data_future))]

    QA_util_log_info('=== The BEST SERVER ===\n stock_ip {} future_ip {}'.format(
        best_stock_ip, best_future_ip))
    return {'stock': best_stock_ip, 'future': best_future_ip}


best_ip = select_best_ip()

# return 1 if sh, 0 if sz


def _select_market_code(code):
    code = str(code)
    if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
        return 1
    return 0


def _select_type(level):
    if level in ['day', 'd', 'D', 'DAY', 'Day']:
        level = 9
    elif level in ['w', 'W', 'Week', 'week']:
        level = 5
    elif level in ['month', 'M', 'm', 'Month']:
        level = 6
    elif level in ['Q', 'Quarter', 'q']:
        level = 10
    elif level in ['y', 'Y', 'year', 'Year']:
        level = 11
    elif str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'

    return level


def QA_fetch_get_security_bars(code, _type, lens, ip=best_ip['stock'], port=7709):
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_security_bars(_select_type(_type), _select_market_code(
            code), code, (i - 1) * 800, 800)) for i in range(1, int(lens / 800) + 2)], axis=0)
        data = data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=str(code))\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(x)))\
            .assign(time_stamp=data['datetime'].apply(lambda x: QA_util_time_stamp(x)))\
            .assign(type=_type).set_index('datetime', drop=False, inplace=False).tail(lens)
        if data is not None:
            return data
        else:
            return None


def QA_fetch_get_stock_day(code, start_date, end_date, if_fq='00', level='day', ip=best_ip['stock'], port=7709):
    api = TdxHq_API()
    with api.connect(ip, port):

        if level in ['day', 'd', 'D', 'DAY', 'Day']:
            level = 9
        elif level in ['w', 'W', 'Week', 'week']:
            level = 5
        elif level in ['month', 'M', 'm', 'Month']:
            level = 6
        elif level in ['Q', 'Quarter', 'q']:
            level = 10
        elif level in ['y', 'Y', 'year', 'Year']:
            level = 11
        start_date = str(start_date)[0:10]
        today_ = datetime.date.today()
        lens = QA_util_get_trade_gap(start_date, today_)

        data = pd.concat([api.to_df(api.get_security_bars(level, _select_market_code(
            code), code, (int(lens / 800) - i) * 800, 800)) for i in range(int(lens / 800) + 1)], axis=0)

        data = data[data['open'] != 0]

        if if_fq in ['00', 'bfq']:
            data = data.assign(date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10]))).set_index('date', drop=False, inplace=False)

            return data.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)[start_date:end_date].assign(date=data['date'].apply(lambda x: str(x)[0:10]))

        elif if_fq in ['01', 'qfq']:

            xdxr_data = QA_fetch_get_stock_xdxr(code)
            bfq_data = data.assign(date=pd.to_datetime(data['datetime'].apply(lambda x: str(x[0:10])))).assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10]))).set_index('date', drop=False, inplace=False)
            bfq_data = bfq_data.drop(
                ['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)
            #
            if xdxr_data is not None:
                info = xdxr_data[xdxr_data['category'] == 1]
                bfq_data['if_trade'] = True
                data = pd.concat([bfq_data, info[['category']]
                                  [bfq_data.index[0]:]], axis=1)

                data['date'] = data.index
                data['if_trade'].fillna(value=False, inplace=True)
                data = data.fillna(method='ffill')
                data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                              'songzhuangu']][bfq_data.index[0]:]], axis=1)
                data = data.fillna(0)

                data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                    * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
                data['adj'] = (data['preclose'].shift(-1) /
                               data['close']).fillna(1)[::-1].cumprod()
                data['open'] = data['open'] * data['adj']
                data['high'] = data['high'] * data['adj']
                data['low'] = data['low'] * data['adj']
                data['close'] = data['close'] * data['adj']
                data['preclose'] = data['preclose'] * data['adj']

                data = data[data['if_trade']]
                return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]
            else:

                bfq_data['preclose'] = bfq_data['close'].shift(1)
                bfq_data['adj'] = 1
                return bfq_data[start_date:end_date]
        elif if_fq in ['03', 'ddqfq']:
            xdxr_data = QA_fetch_get_stock_xdxr(code)

            info = xdxr_data[xdxr_data['category'] == 1]

            bfq_data = data\
                .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10])))\
                .assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10])))\
                .set_index('date', drop=False, inplace=False)\
                .drop(['year', 'month', 'day', 'hour',
                       'minute', 'datetime'], axis=1)

            bfq_data['if_trade'] = True
            data = pd.concat([bfq_data, info[['category']]
                              [bfq_data.index[0]:end_date]], axis=1)

            data['date'] = data.index
            data['if_trade'].fillna(value=False, inplace=True)
            data = data.fillna(method='ffill')
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][bfq_data.index[0]:end_date]], axis=1)
            data = data.fillna(0)

            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1)[::-1].cumprod()
            data['open'] = data['open'] * data['adj']
            data['high'] = data['high'] * data['adj']
            data['low'] = data['low'] * data['adj']
            data['close'] = data['close'] * data['adj']
            data['preclose'] = data['preclose'] * data['adj']

            data = data[data['if_trade']]
            return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]

        elif if_fq in ['02', 'hfq']:
            xdxr_data = QA_fetch_get_stock_xdxr(code)

            info = xdxr_data[xdxr_data['category'] == 1]

            bfq_data = data\
                .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10])))\
                .assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10])))\
                .set_index('date', drop=False, inplace=False)\
                .drop(['year', 'month', 'day', 'hour',
                       'minute', 'datetime'], axis=1)

            bfq_data['if_trade'] = True
            data = pd.concat([bfq_data, info[['category']]
                              [bfq_data.index[0]:]], axis=1)

            data['date'] = data.index
            data['if_trade'].fillna(value=False, inplace=True)
            data = data.fillna(method='ffill')
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][bfq_data.index[0]:]], axis=1)
            data = data.fillna(0)

            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1).cumprod()
            data['open'] = data['open'] / data['adj']
            data['high'] = data['high'] / data['adj']
            data['low'] = data['low'] / data['adj']
            data['close'] = data['close'] / data['adj']
            data['preclose'] = data['preclose'] / data['adj']
            data = data[data['if_trade']]
            return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]

        elif if_fq in ['04', 'ddhfq']:
            xdxr_data = QA_fetch_get_stock_xdxr(code)

            info = xdxr_data[xdxr_data['category'] == 1]

            bfq_data = data\
                .assign(date=pd.to_datetime(data['datetime'].apply(lambda x: x[0:10])))\
                .assign(code=str(code))\
                .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10])))\
                .set_index('date', drop=False, inplace=False)\
                .drop(['year', 'month', 'day', 'hour',
                       'minute', 'datetime'], axis=1)

            bfq_data['if_trade'] = True
            data = pd.concat([bfq_data, info[['category']]
                              [bfq_data.index[0]:end_date]], axis=1)

            data['date'] = data.index
            data['if_trade'].fillna(value=False, inplace=True)
            data = data.fillna(method='ffill')
            data = pd.concat([data, info[['fenhong', 'peigu', 'peigujia',
                                          'songzhuangu']][bfq_data.index[0]:end_date]], axis=1)
            data = data.fillna(0)

            data['preclose'] = (data['close'].shift(1) * 10 - data['fenhong'] + data['peigu']
                                * data['peigujia']) / (10 + data['peigu'] + data['songzhuangu'])
            data['adj'] = (data['preclose'].shift(-1) /
                           data['close']).fillna(1).cumprod()
            data['open'] = data['open'] / data['adj']
            data['high'] = data['high'] / data['adj']
            data['low'] = data['low'] / data['adj']
            data['close'] = data['close'] / data['adj']
            data['preclose'] = data['preclose'] / data['adj']
            data = data[data['if_trade']]
            return data.drop(['fenhong', 'peigu', 'peigujia', 'songzhuangu', 'if_trade', 'category'], axis=1)[data['open'] != 0].assign(date=data['date'].apply(lambda x: str(x)[0:10]))[start_date:end_date]


def QA_fetch_get_stock_min(code, start, end, level='1min', ip=best_ip['stock'], port=7709):
    api = TdxHq_API()
    type_ = ''
    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    if str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
        lens = 48 * lens
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
        lens = 240 * lens
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
        lens = 16 * lens
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
        lens = 8 * lens
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'
        lens = 4 * lens
    if lens > 20800:
        lens = 20800
    with api.connect(ip, port):

        data = pd.concat([api.to_df(api.get_security_bars(level, _select_market_code(
            str(code)), str(code), (int(lens / 800) - i) * 800, 800)) for i in range(int(lens / 800) + 1)], axis=0)
        data = data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=str(code))\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(x)))\
            .assign(time_stamp=data['datetime'].apply(lambda x: QA_util_time_stamp(x)))\
            .assign(type=type_).set_index('datetime', drop=False, inplace=False)[start:end]
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


def QA_fetch_get_stock_latest(code, ip=best_ip['stock'], port=7709):
    code = [code] if isinstance(code, str) else code
    api = TdxHq_API(multithread=True)
    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_security_bars(
            9, _select_market_code(item), item, 0, 1)).assign(code=item) for item in code], axis=0)
        return data\
            .assign(date=pd.to_datetime(data['datetime']
                                        .apply(lambda x: x[0:10])), date_stamp=data['datetime']
                    .apply(lambda x: QA_util_date_stamp(str(x[0:10]))))\
            .set_index('date', drop=False)\
            .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)


def QA_fetch_get_stock_realtime(code=['000001', '000002'], ip=best_ip['stock'], port=7709):
    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if type(code) is str else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(_select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
        data = __data[['datetime', 'active1', 'active2', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
                       's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
                       'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
                       'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]
        return data.set_index('code', drop=False, inplace=False)
    
def QA_fetch_depth_market_data(code=['000001', '000002'], ip=best_ip['stock'], port=7709):
    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if type(code) is str else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(_select_market_code(x), x) for x in code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
        data = __data[['datetime', 'active1', 'active2', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
                       's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
                       'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
                       'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]
        return data.set_index(['datetime','code'], drop=False, inplace=False)

def QA_fetch_get_stock_list(type_='stock', ip=best_ip['stock'], port=7709):

    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat([pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(sse='sz' if j == 0 else 'sh').set_index(
            ['code', 'sse'], drop=False) for i in range(int(api.get_security_count(j) / 1000) + 1)], axis=0) for j in range(2)], axis=0)
        if type_ in ['stock', 'gp']:
            return pd.concat([data[data['sse'] == 'sz'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 10000 <= 30][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 100000 != 2][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 100000 != 1],
                              data[data['sse'] == 'sh'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 100000 == 6]]).assign(code=data['code'].apply(lambda x: str(x))).assign(name=data['name'].apply(lambda x: str(x)[0:4]))
            #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #.assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))
        elif type_ in ['index', 'zs']:

            return pd.concat([data[data['sse'] == 'sz'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 1000 >= 399],
                              data[data['sse'] == 'sh'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 1000 == 0]]) \
                .sort_index()\
                .assign(name=data['name'].apply(lambda x: str(x)[0:4]))\
                .assign(code=data['code'].apply(lambda x: str(x)))
            #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #.assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))
        elif type_ in ['etf', 'ETF']:
            return pd.concat([data[data['sse'] == 'sz'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 10000 == 15],
                              data[data['sse'] == 'sh'][data.assign(code=data['code'].apply(lambda x: int(x)))['code'] // 10000 == 51]]).sort_index().assign(code=data['code'].apply(lambda x: str(x))).assign(name=data['name'].apply(lambda x: str(x)[0:4]))\
                #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #.assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))

        else:
            return data.assign(code=data['code'].apply(lambda x: str(x))).assign(name=data['name'].apply(lambda x: str(x)[0:4]))
            #.assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #    .assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))


def QA_fetch_get_index_day(code, start_date, end_date, level='day', ip=best_ip['stock'], port=7709):
    '指数日线'
    api = TdxHq_API()
    if level in ['day', 'd', 'D', 'DAY', 'Day']:
        level = 9
    elif level in ['w', 'W', 'Week', 'week']:
        level = 5
    elif level in ['month', 'M', 'm', 'Month']:
        level = 6
    elif level in ['Q', 'Quarter', 'q']:
        level = 10
    elif level in ['y', 'Y', 'year', 'Year']:
        level = 11

    with api.connect(ip, port):

        start_date = str(start_date)[0:10]
        today_ = datetime.date.today()
        lens = QA_util_get_trade_gap(start_date, today_)

        if str(code)[0] in ['5', '1']:  # ETF
            data = pd.concat([api.to_df(api.get_security_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (int(lens / 800) - i) * 800, 800)) for i in range(int(lens / 800) + 1)], axis=0)
        else:
            data = pd.concat([api.to_df(api.get_index_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (int(lens / 800) - i) * 800, 800)) for i in range(int(lens / 800) + 1)], axis=0)
        data = data.assign(date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(code=str(code))\
            .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10])))\
            .set_index('date', drop=False, inplace=False)\
            .drop(['year', 'month', 'day', 'hour',
                   'minute', 'datetime'], axis=1)[start_date:end_date]
        return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))


def QA_fetch_get_index_min(code, start, end, level='1min', ip=best_ip['stock'], port=7709):
    '指数分钟线'
    api = TdxHq_API()
    type_ = ''

    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    if str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
        lens = 48 * lens
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
        lens = 240 * lens
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
        lens = 16 * lens
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
        lens = 8 * lens
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'
        lens = 4 * lens

    if lens > 20800:
        lens = 20800
    with api.connect(ip, port):

        if str(code)[0] in ['5', '1']:  # ETF
            data = pd.concat([api.to_df(api.get_security_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (int(lens / 800) - i) * 800, 800)) for i in range(int(lens / 800) + 1)], axis=0)
        else:
            data = pd.concat([api.to_df(api.get_index_bars(
                level, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0, code, (int(lens / 800) - i) * 800, 800)) for i in range(int(lens / 800) + 1)], axis=0)
        data = data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=str(code))\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(x)))\
            .assign(time_stamp=data['datetime'].apply(lambda x: QA_util_time_stamp(x)))\
            .assign(type=type_).set_index('datetime', drop=False, inplace=False)[start:end]
        # data
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


def __QA_fetch_get_stock_transaction(code, day, retry, api):
    batch_size = 2000  # 800 or 2000 ? 2000 maybe also works
    data_arr = []
    max_offset = 21
    cur_offset = 0
    while cur_offset <= max_offset:
        one_chunk = api.get_history_transaction_data(
            _select_market_code(str(code)), str(code), cur_offset * batch_size, batch_size, QA_util_date_str2int(day))
        if one_chunk is None or one_chunk == []:
            break
        data_arr = one_chunk + data_arr
        cur_offset += 1
    data_ = api.to_df(data_arr)

    for _ in range(retry):
        if len(data_) < 2:
            return __QA_fetch_get_stock_transaction(code, day, 0, api)
        else:
            return data_.assign(date=day).assign(datetime=pd.to_datetime(data_['time'].apply(lambda x: str(day) + ' ' + x)))\
                        .assign(code=str(code)).assign(order=range(len(data_.index))).set_index('datetime', drop=False, inplace=False)


def QA_fetch_get_stock_transaction(code, start, end, retry=2, ip=best_ip['stock'], port=7709):
    '历史逐笔成交'
    api = TdxHq_API()

    real_start, real_end = QA_util_get_real_datelist(start, end)
    if real_start is None:
        return None
    real_id_range = []
    with api.connect(ip, port):
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

        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)[0:19]))

def QA_fetch_get_stock_transaction_realtime(code, ip=best_ip['stock'], port=7709):
    '实时逐笔成交 包含集合竞价'
    api = TdxHq_API()

    with api.connect(ip, port):
        data = pd.DataFrame()
        data = pd.concat([api.to_df(api.get_transaction_data(
            _select_market_code(str(code)), code, (2 - i) * 2000, 2000)) for i in range(3)], axis=0)
        if 'value' in data.columns:
            data = data.drop(['value'], axis=1)

        day = datetime.date.today()
        return data.dropna().assign(date=day).assign(datetime=pd.to_datetime(data['time'].apply(lambda x: str(day) + ' ' + str(x))))\
                            .assign(code=str(code)).assign(order=range(len(data.index))).set_index('datetime', drop=False, inplace=False)


def QA_fetch_get_stock_xdxr(code, ip=best_ip['stock'], port=7709):
    '除权除息'
    api = TdxHq_API()
    market_code = _select_market_code(code)
    with api.connect(ip, port):
        category = {
            '1': '除权除息', '2': '送配股上市', '3': '非流通股上市', '4': '未知股本变动', '5': '股本变化',
            '6': '增发新股', '7': '股份回购', '8': '增发新股上市', '9': '转配股上市', '10': '可转债上市',
            '11': '扩缩股', '12': '非流通股缩股', '13':  '送认购权证', '14': '送认沽权证'}
        data = api.to_df(api.get_xdxr_info(market_code, code))
        if len(data) >= 1:
            data = data\
                .assign(date=pd.to_datetime(data[['year', 'month', 'day']]))\
                .drop(['year', 'month', 'day'], axis=1)\
                .assign(category_meaning=data['category'].apply(lambda x: category[str(x)]))\
                .assign(code=str(code))\
                .rename(index=str, columns={'panhouliutong': 'liquidity_after',
                                            'panqianliutong': 'liquidity_before', 'houzongguben': 'shares_after',
                                            'qianzongguben': 'shares_before'})\
                .set_index('date', drop=False, inplace=False)
            return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))
        else:
            return None


def QA_fetch_get_stock_info(code, ip=best_ip['stock'], port=7709):
    '除权除息'
    api = TdxHq_API()
    market_code = _select_market_code(code)
    with api.connect(ip, port):
        return api.to_df(api.get_finance_info(market_code, code))



def QA_fetch_get_stock_block(ip=best_ip['stock'], port=7709):
    '板块数据'
    api = TdxHq_API()
    with api.connect(ip, port):

        data = pd.concat([api.to_df(api.get_and_parse_block_info("block_gn.dat")).assign(type='gn'),
                          api.to_df(api.get_and_parse_block_info(
                              "block.dat")).assign(type='yb'),
                          api.to_df(api.get_and_parse_block_info(
                              "block_zs.dat")).assign(type='zs'),
                          api.to_df(api.get_and_parse_block_info("block_fg.dat")).assign(type='fg')])

        if len(data) > 10:
            return data.assign(source='tdx').drop(['block_type', 'code_index'], axis=1).set_index('code', drop=False, inplace=False).drop_duplicates()
        else:
            QA_util_log_info('Wrong with fetch block ')


"""
期货数据接口

1: 获取市场代码
可以获取该api服务器可以使用的市场列表，类别等信息
api.get_markets()
返回结果 api.to_df(api.get_markets()) 一般某个服务器返回的类型比较固定，该结果可以缓存到本地或者内存中。
2017-07-31 21:22:06,067 - PYTDX - INFO - 获取市场代码
    market  category    name short_name
0        1         1     临时股         TP
1        4        12  郑州商品期权         OZ
2        5        12  大连商品期权         OD
3        6        12  上海商品期权         OS
4        8        12  上海个股期权         QQ
5       27         5    香港指数         FH
6       28         3    郑州商品         QZ
7       29         3    大连商品         QD
8       30         3    上海期货         QS
9       31         2    香港主板         KH
10      32         2    香港权证         KR
11      33         8   开放式基金         FU
12      34         9   货币型基金         FB
13      35         8  招商理财产品         LC
14      36         9  招商货币产品         LB
15      37        11    国际指数         FW
16      38        10  国内宏观指标         HG
17      40        11   中国概念股         CH
18      41        11  美股知名公司         MG
19      43         1   B股转H股         HB
20      44         1    股份转让         SB
21      47         3    股指期货         CZ
22      48         2   香港创业板         KG
23      49         2  香港信托基金         KT
24      54         6   国债预发行         GY
25      60         3  主力期货合约         MA
26      62         5    中证指数         ZZ
27      71         2     港股通         GH
2: 查询代码列表
参数， 起始位置， 获取数量
api.get_instrument_info(0, 100)
Demo: get_list_demo
3: 查询市场中商品数量
api.get_instrument_count()
4: 查询五档行情
参数 市场ID，证券代码
市场ID可以通过 get_markets 获得
api.get_instrument_quote(47, "IF1709")
5: 查询分时行情
参数 市场ID，证券代码
市场ID可以通过 get_markets 获得
api.get_minute_time_data(47, "IF1709")
6: 查询历史分时行情
参数 市场ID，证券代码，日期
市场ID可以通过 get_markets 获得
日期格式 YYYYMMDD 如 20170811
api.get_history_minute_time_data(31, "00020", 20170811)
7: 查询k线数据
参数： K线周期， 市场ID， 证券代码，起始位置， 数量
K线周期参考 TDXParams
市场ID可以通过 get_markets 获得
api.get_instrument_bars(TDXParams.KLINE_TYPE_DAILY, 8, "10000843", 0, 100)
8: 查询分笔成交
参数：市场ID，证券代码
市场ID可以通过 get_markets 获得
api.get_transaction_data(31, "00020")
注意，这个接口最多返回1800条记录, 如果有超过1800条记录的请求，我们有一个start 参数作为便宜量，可以取出超过1800条记录
如期货的数据：这个接口可以取出1800条之前的记录，数量也是1800条
api.get_history_transaction_data(47, "IFL0", 20170810, start=1800)
9: 查询历史分笔成交
参数：市场ID，证券代码, 日期
市场ID可以通过 get_markets 获得
日期格式 YYYYMMDD 如 20170810
api.get_history_transaction_data(31, "00020", 20170810)

"""
"""
期货及扩展行情

首先会初始化/存储一个代码对应表 extension_market_info

"""


def QA_fetch_get_future_list(ip=best_ip['future'], port=7727):
    '期货代码list'
    apix = TdxExHq_API()
    with apix.connect(ip, port):
        num = apix.get_instrument_count()
        return pd.concat([apix.to_df(
            apix.get_instrument_info((int(num / 500) - i) * 500, 500))
            for i in range(int(num / 500) + 1)], axis=0).set_index('code', drop=False)
global extension_market_info
extension_market_info = None
def QA_fetch_get_future_day(code, start_date, end_date, level='day', ip=best_ip['future'], port=7727):
    '期货数据 日线'

    apix = TdxExHq_API()
    start_date = str(start_date)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    global extension_market_info
    extension_market_info=QA_fetch_get_future_list() if extension_market_info is None else extension_market_info

    with apix.connect(ip, port):
        code_market = extension_market_info.query('code=="{}"'.format(code))
        
        data = pd.concat([apix.to_df(apix.get_instrument_bars(_select_type(
            level), int(code_market.market), str(code),(int(lens / 700) - i) * 700, 700))for i in range(int(lens / 700) + 1)], axis=0)
        data = data.assign(date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(code=str(code))\
            .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(str(x)[0:10]))).set_index('date', drop=False, inplace=False)

        return data.drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)[start_date:end_date].assign(date=data['date'].apply(lambda x: str(x)[0:10]))


def QA_fetch_get_future_min(code, start, end, level='1min',ip=best_ip['future'], port=7727):
    '期货数据 分钟线'
    apix = TdxExHq_API()
    type_ = ''
    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    global extension_market_info
    extension_market_info=QA_fetch_get_future_list() if extension_market_info is None else extension_market_info
    
    if str(level) in ['5', '5m', '5min', 'five']:
        level, type_ = 0, '5min'
        lens = 48 * lens
    elif str(level) in ['1', '1m', '1min', 'one']:
        level, type_ = 8, '1min'
        lens = 240 * lens
    elif str(level) in ['15', '15m', '15min', 'fifteen']:
        level, type_ = 1, '15min'
        lens = 16 * lens
    elif str(level) in ['30', '30m', '30min', 'half']:
        level, type_ = 2, '30min'
        lens = 8 * lens
    elif str(level) in ['60', '60m', '60min', '1h']:
        level, type_ = 3, '60min'
        lens = 4 * lens
    if lens > 20800:
        lens = 20800
    with apix.connect(ip, port):
        code_market = extension_market_info.query('code=="{}"'.format(code))
        data = pd.concat([apix.to_df(apix.get_instrument_bars(level, int(code_market.market), str(code), (int(lens / 700) - i) * 700, 700)) for i in range(int(lens / 700) + 1)], axis=0)

        data = data\
            .assign(datetime=pd.to_datetime(data['datetime']), code=str(code))\
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1, inplace=False)\
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]))\
            .assign(date_stamp=data['datetime'].apply(lambda x: QA_util_date_stamp(x)))\
            .assign(time_stamp=data['datetime'].apply(lambda x: QA_util_time_stamp(x)))\
            .assign(type=type_).set_index('datetime', drop=False, inplace=False)[start:end]
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


def QA_fetch_get_future_transaction(ip=best_ip['future'], port=7727):
    '期货历史成交分笔'
    apix = TdxExHq_API()
    with apix.connect(ip, port):
        pass


def QA_fetch_get_future_transaction_realtime(ip=best_ip['future'], port=7727):
    '期货历史成交分笔'
    apix = TdxExHq_API()
    with apix.connect(ip, port):
        pass


def QA_fetch_get_future_realtime(code, ip=best_ip['future'], port=7727):
    '期货实时价格'
    pass


if __name__ == '__main__':
    # print(QA_fetch_get_stock_day('000001','2017-07-03','2017-07-10'))
    # print(QA_fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
    print(QA_fetch_get_stock_realtime('000001'))
    #print(QA_fetch_get_index_day('000001', '2017-01-01', '2017-07-01'))
    # print(QA_fetch_get_stock_transaction('000001', '2017-07-03', '2017-07-10'))

    print(QA_fetch_get_stock_info('600116'))
