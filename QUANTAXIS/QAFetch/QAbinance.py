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
币安api
具体api文档参考:https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
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
Binance_base_url = "https://api.binance.com"

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
QUANTAXIS 和 binance 的 frequency 常量映射关系
"""
Binance2QA_FREQUENCY_DICT = {
    "1m": '1min',
    "5m": '5min',
    "15m": '15min',
    "30m": '30min',
    "1h": '60min',
    "1d": 'day',
}
"""
binance 只允许一次获取 500bar，时间请求超过范围则只返回最新500条
"""
FREQUENCY_SHIFTING = {
    "1m": 30000,
    "5m": 150000,
    "15m": 450000,
    "30m": 900000,
    "1h": 1800000,
    "1d": 43200000,
}


def format_binance_data_fields(datas, symbol, frequency):
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
    frame['symbol'] = 'BINANCE.{}'.format(symbol)
    # UTC时间转换为北京时间
    frame['start_time'] = frame.apply(
        lambda x: int(x['start_time'] / 1000),
        axis=1
    )
    frame['date'] = pd.to_datetime(
        frame['start_time'],
        unit='s'
    , utc=False)
    frame['date'] = frame['date'].dt.strftime('%Y-%m-%d')
    frame['datetime'] = pd.to_datetime(
        frame['start_time'],
        unit='s'
    , utc=False)
    frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # GMT+0 String 转换为 UTC Timestamp
    frame['date_stamp'] = pd.to_datetime(frame['date']
                                        ).astype(np.int64) // 10**9
    frame['created_at'] = int(
        time.mktime(datetime.datetime.now().utctimetuple())
    )
    frame['updated_at'] = int(
        time.mktime(datetime.datetime.now().utctimetuple())
    )
    frame.rename(
        {
            'num_trades': 'trade',
            'start_time': 'time_stamp',
            'buy_quote_asset_volume': 'amount'
        },
        axis=1,
        inplace=True
    )
    if (frequency not in ['1day', Binance2QA_FREQUENCY_DICT['1d'], '1d']):
        frame['type'] = Binance2QA_FREQUENCY_DICT[frequency]
    frame.drop(
        ['close_time',
         'quote_asset_volume',
         'buy_base_asset_volume',
         'Ignore'],
        axis=1,
        inplace=True
    )
    return frame


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_binance_symbols():
    url = urljoin(Binance_base_url, "/api/v1/exchangeInfo")
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
            if len(symbol_lists["symbols"]) == 0:
                return []
            for symbol in symbol_lists["symbols"]:
                # 只导入上架交易对
                if (symbol['status'] == 'TRADING'):
                    datas.append(symbol)

    return datas


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_binance_kline_with_auto_retry(
    symbol,
    start_time,
    end_time,
    frequency,
):
    """
    Get the latest symbol‘s candlestick data
    """

    retries = 1
    start_time *= 1000
    end_time *= 1000
    while start_time < end_time:
        url = urljoin(Binance_base_url, "/api/v1/klines")
        try:
            req = requests.get(
                url,
                params={
                    "symbol": symbol,
                    "interval": frequency,
                    "startTime": int(start_time),
                    "endTime": int(end_time)
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
            print("Retry /api/v1/klines #{}".format(retries))
            time.sleep(0.5)

        if (retries == 0):
            # 成功获取才处理数据，否则继续尝试连接
            klines = json.loads(req.content)

            if len(klines) == 0:
                print('Error', klines)
                return None
            return klines


    return None


def QA_fetch_binance_kline(
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

        klines = QA_fetch_binance_kline_with_auto_retry(
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
            frame = format_binance_data_fields(klines, symbol, frequency)
            callback_func(frame, Binance2QA_FREQUENCY_DICT[frequency])

    if len(datas) == 0:
        return None

    # 归一化数据字段，转换填充必须字段，删除多余字段
    frame = format_binance_data_fields(datas, symbol, frequency)
    return frame


def QA_fetch_binance_kline_min(
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

        klines = QA_fetch_binance_kline_with_auto_retry(
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
            frame = format_binance_data_fields(klines, symbol, frequency)
            callback_func(frame, Binance2QA_FREQUENCY_DICT[frequency])

        if (len(klines) == 0):
            return None


if __name__ == '__main__':
    # url = urljoin(Binance_base_url, "/api/v1/exchangeInfo")
    # print(url)
    # a = requests.get(url)
    # print(a.content)
    # print(json.loads(a.content))
    import pytz
    from dateutil.tz import *

    tz = pytz.timezone("Asia/Shanghai")
    url = urljoin(Binance_base_url, "/api/v1/klines")
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
    data = QA_fetch_binance_kline("ETHBTC", start, end, '1d')
    print(len(data))
    print(data[0])
    print(data[-1])
