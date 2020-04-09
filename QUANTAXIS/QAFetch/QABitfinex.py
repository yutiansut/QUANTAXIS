# coding: utf-8
# Author: 阿财（Rgveda@github）（11652964@qq.com）
# Created date: 2020-02-27
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
# The above copyright notice and this permission notice shall be included in
# all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Bitfinex api
具体api文档参考:https://docs.bitfinex.com/docs
"""
import requests
import json
import datetime
import time
from dateutil.tz import tzutc
import pandas as pd
import numpy as np
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from requests.exceptions import ConnectTimeout, SSLError, ReadTimeout, ConnectionError
from retrying import retry
from urllib.parse import urljoin

from QUANTAXIS.QAUtil.QADate_Adv import (
    QA_util_timestamp_to_str,
    QA_util_datetime_to_Unix_timestamp,
    QA_util_timestamp_to_str,
    QA_util_print_timestamp,
)
from QUANTAXIS.QAUtil import (
    QA_util_log_info,
)

TIMEOUT = 10
ILOVECHINA = "同学！！你知道什么叫做科学上网么？ 如果你不知道的话，那么就加油吧！蓝灯，喵帕斯，VPS，阴阳师，v2ray，随便什么来一个！我翻墙我骄傲！"
Bitfinex_base_url = "https://api-pub.bitfinex.com/"

column_names = [
    'start_time',
    'open',
    'high',
    'low',
    'close',
    'volume',
    'close_time',
    'quote_asset_volume',
    'num_trades',
    'buy_base_asset_volume',
    'buy_quote_asset_volume',
    'Ignore'
]

"""
QUANTAXIS 和 Bitfinex 的 frequency 常量映射关系
"""
Bitfinex2QA_FREQUENCY_DICT = {
    "1m": '1min',
    "5m": '5min',
    "15m": '15min',
    "30m": '30min',
    "1h": '60min',
    "1d": 'day',
}
"""
Bitfinex 只允许一次获取 200bar，时间请求超过范围则只返回最新200条
"""
FREQUENCY_SHIFTING = {
    "60": 12000,
    "300": 60000,
    "900": 180000,
    "1800": 360000,
    "3600": 720000,
    "86400": 17280000
}


def format_bitfinex_data_fields(datas, symbol, frequency):
    """
    # 归一化数据字段，转换填充必须字段，删除多余字段
    参数名 	类型 	描述
    time 	String 	开始时间
    open 	String 	开盘价格
    high 	String 	最高价格
    low 	String 	最低价格
    close 	String 	收盘价格
    volume 	String 	交易量
    """
    frame = pd.DataFrame(datas, columns=column_names)
    frame['symbol'] = 'BITFINEX.{}'.format(symbol)
    # UTC时间转换为北京时间，接收到的数据有时候 tz-aware 有时候又是变成 non tz-aware，
    # 改了几次代码，既不能单纯 tz_localize 也不能单纯 tz_convert
    # dt.tz_localize(None) 是 Stackoverflow 的解决方案，先观察效果
    frame['datetime'] = pd.to_datetime(
        frame['time']
    ).dt.tz_localize(None).dt.tz_localize('Asia/Shanghai')
    frame['date'] = frame['datetime'].dt.strftime('%Y-%m-%d')
    frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # GMT+0 String 转换为 UTC Timestamp
    frame['time_stamp'] = pd.to_datetime(frame['time']
                                        ).astype(np.int64) // 10**9
    frame['date_stamp'] = pd.to_datetime(
        frame['date']
    ).dt.tz_localize('Asia/Shanghai').astype(np.int64) // 10**9
    frame['created_at'] = int(
        time.mktime(datetime.datetime.now().utctimetuple())
    )
    frame['updated_at'] = int(
        time.mktime(datetime.datetime.now().utctimetuple())
    )
    frame.drop(['time'], axis=1, inplace=True)
    frame['trade'] = 1
    frame['amount'] = frame.apply(
        lambda x: float(x['volume']) *
        (float(x['open']) + float(x['close'])) / 2,
        axis=1
    )
    if (frequency not in ['1day', 'day', '86400', '1d']):
        frame['type'] = OKEx2QA_FREQUENCY_DICT[frequency]
    return frame


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_bitfinex_symbols():
    """
    获取交易币对的列表，查询各币对的交易限制和价格步长等信息。
    限速规则：20次/2s
    HTTP请求 GET/api/spot/v3/instruments
    """
    url = urljoin(Bitfinex_base_url, "/api/v1/exchangeInfo")
    retries = 1
    datas = list()
    while (retries != 0):
        try:
            req = requests.get(url, timeout=TIMEOUT)
            retries = 0
        except (ConnectTimeout, ConnectionError, SSLError, ReadTimeout):
            retries = retries + 1
            if (retries % 6 == 0):
                print(ILOVECHINA)
            print("Retry /api/v1/exchangeInfo #{}".format(retries - 1))
            time.sleep(0.5)

        if (retries == 0):
            # 成功获取才处理数据，否则继续尝试连接
            symbol_lists = json.loads(req.content)
            if len(symbol_lists) == 0:
                return []
            for symbol in symbol_lists:
                datas.append(symbol)

    return datas


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_bitfinex_kline_with_auto_retry(
    symbol,
    start_time,
    end_time,
    frequency,
):
    """
    Get the latest symbol‘s candlestick data raw method
    获取币对的K线数据。K线数据按请求的粒度分组返回，k线数据最多可获取200条(说明文档中2000条系错误)。
    限速规则：20次/2s
    HTTP请求 GET/api/spot/v3/instruments/<instrument_id>/candles
    """
    url = urljoin(
        OKEx_base_url,
        "/api/spot/v3/instruments/{:s}/candles".format(symbol)
    )
    retries = 1
    while (retries != 0):
        try:
            start_epoch = datetime.datetime.fromtimestamp(
                start_time,
                tz=tzutc()
            )
            end_epoch = datetime.datetime.fromtimestamp(end_time, tz=tzutc())
            req = requests.get(
                url,
                params={
                    "granularity": frequency,
                    "start": start_epoch.isoformat().replace("+00:00", "Z"),   # Z结尾的ISO时间 String
                    "end": end_epoch.isoformat() .replace("+00:00", "Z")       # Z结尾的ISO时间 String
                },
                timeout=TIMEOUT
            )
            # 防止频率过快被断连
            time.sleep(0.5)
            retries = 0
        except (ConnectTimeout, ConnectionError, SSLError, ReadTimeout):
            retries = retries + 1
            if (retries % 6 == 0):
                print(ILOVECHINA)
            print("Retry /api/spot/v3/instruments #{}".format(retries - 1))
            time.sleep(0.5)

        if (retries == 0):
            # 成功获取才处理数据，否则继续尝试连接
            msg_dict = json.loads(req.content)

            if ('error_code' in msg_dict):
                print('Error', msg_dict)
                return None

            return msg_dict

    return None


def QA_fetch_bitfinex_kline(
    symbol,
    start_time,
    end_time,
    frequency,
    callback_func=None
):
    """
    Get the latest symbol‘s candlestick data
    时间倒序切片获取算法，是各大交易所获取1min数据的神器，因为大部分交易所直接请求跨月跨年的1min分钟数据
    会直接返回空值，只有将 start_epoch，end_epoch 切片细分到 200/300 bar 以内，才能正确返回 kline，
    火币和binance，OKEx 均为如此，直接用跨年时间去直接请求上万bar 的 kline 数据永远只返回最近200条数据。
    """
    datas = list()
    reqParams = {}
    reqParams['from'] = end_time - FREQUENCY_SHIFTING[frequency]
    reqParams['to'] = end_time

    while (reqParams['to'] > start_time):
        if ((reqParams['from'] > QA_util_datetime_to_Unix_timestamp())) or \
            ((reqParams['from'] > reqParams['to'])):
            # 出现“未来”时间，一般是默认时区设置，或者时间窗口滚动前移错误造成的
            QA_util_log_info(
                'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                .format(
                    symbol,
                    frequency,
                    QA_util_print_timestamp(reqParams['from']),
                    QA_util_print_timestamp(
                        QA_util_datetime_to_Unix_timestamp()
                    )
                )
            )
            # 跳到下一个时间段
            reqParams['to'] = int(reqParams['from'] - 1)
            reqParams['from'] = int(reqParams['from'] - FREQUENCY_SHIFTING[frequency])
            continue

        klines = QA_fetch_okex_kline_with_auto_retry(
            symbol,
            reqParams['from'],
            reqParams['to'],
            frequency,
        )
        if (klines is None) or \
            (len(klines) == 0) or \
            ('error' in klines):
            # 出错放弃
            break

        reqParams['to'] = int(reqParams['from'] - 1)
        reqParams['from'] = int(reqParams['from'] - FREQUENCY_SHIFTING[frequency])

        if (klines is None) or \
            ((len(datas) > 0) and (klines[-1][0] == datas[-1][0])):
            # 没有更多数据
            break

        datas.extend(klines)

        if (callback_func is not None):
            frame = format_okex_data_fields(klines, symbol, frequency)
            callback_func(frame, OKEx2QA_FREQUENCY_DICT[frequency])

    if len(datas) == 0:
        return None

    # 归一化数据字段，转换填充必须字段，删除多余字段
    frame = format_okex_data_fields(datas, symbol, frequency)
    return frame


def QA_fetch_bitfinex_kline_min(
    symbol,
    start_time,
    end_time,
    frequency,
    callback_func=None
):
    """
    Get the latest symbol‘s candlestick data with time slices
    时间倒序切片获取算法，是各大交易所获取1min数据的神器，因为大部分交易所直接请求跨月跨年的1min分钟数据
    会直接返回空值，只有将 start_epoch，end_epoch 切片细分到 200/300 bar 以内，才能正确返回 kline，
    火币和binance，OKEx 均为如此，用上面那个函数的方式去直接请求上万bar 的分钟 kline 数据是不会有结果的。
    """
    reqParams = {}
    reqParams['from'] = end_time - FREQUENCY_SHIFTING[frequency]
    reqParams['to'] = end_time

    requested_counter = 1
    datas = list()
    while (reqParams['to'] > start_time):
        if ((reqParams['from'] > QA_util_datetime_to_Unix_timestamp())) or \
            ((reqParams['from'] > reqParams['to'])):
            # 出现“未来”时间，一般是默认时区设置，或者时间窗口滚动前移错误造成的
            QA_util_log_info(
                'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                .format(
                    symbol,
                    frequency,
                    QA_util_print_timestamp(reqParams['from']),
                    QA_util_print_timestamp(
                        QA_util_datetime_to_Unix_timestamp()
                    )
                )
            )
            # 跳到下一个时间段
            reqParams['to'] = int(reqParams['from'] - 1)
            reqParams['from'] = int(reqParams['from'] - FREQUENCY_SHIFTING[frequency])
            continue

        klines = QA_fetch_okex_kline_with_auto_retry(
            symbol,
            reqParams['from'],
            reqParams['to'],
            frequency,
        )
        if (klines is None) or \
            (len(klines) == 0) or \
            ('error' in klines):
            # 出错放弃
            break

        reqParams['to'] = int(reqParams['from'] - 1)
        reqParams['from'] = int(reqParams['from'] - FREQUENCY_SHIFTING[frequency])

        if (callback_func is not None):
            frame = format_okex_data_fields(klines, symbol, frequency)
            callback_func(frame, OKEx2QA_FREQUENCY_DICT[frequency])

        if (len(klines) == 0):
            return None


if __name__ == '__main__':
    # url = urljoin(Bitfinex_base_url, "/api/v1/exchangeInfo")
    # print(url)
    # a = requests.get(url)
    # print(a.content)
    # print(json.loads(a.content))
    import pytz
    from dateutil.tz import *

    tz = pytz.timezone("Asia/Shanghai")
    url = urljoin(Bitfinex_base_url, "/api/v1/klines")
    start = time.mktime(
        datetime.datetime(2018,
                          6,
                          13,
                          tzinfo=tzutc()).timetuple()
    )
    end = time.mktime(
        datetime.datetime(2018,
                          6,
                          14,
                          tzinfo=tzutc()).timetuple()
    )
    print(start * 1000)
    print(end * 1000)
    data = QA_fetch_bitfinex_kline("ETHBTC", start, end, '1d')
    print(len(data))
    print(data[0])
    print(data[-1])
