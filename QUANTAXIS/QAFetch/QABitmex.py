"""
bitmex api
具体api文档参考:https://www.bitmex.com/api/explorer/#/
"""

import requests
import json
import datetime
import time
import pandas as pd
import numpy as np
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from requests.exceptions import ConnectTimeout, SSLError, ReadTimeout, ConnectionError
from retrying import retry

from urllib.parse import urljoin
TIMEOUT = 10
ILOVECHINA = "同学！！你知道什么叫做科学上网么？ 如果你不知道的话，那么就加油吧！蓝灯，喵帕斯，VPS，阴阳师，v2ray，随便什么来一个！我翻墙我骄傲！"
Bitmex_base_url = "https://www.bitmex.com/api/v1/"

MAX_HISTORY = 750
"""
QUANTAXIS 和 Bitmex 的 frequency 常量映射关系
"""
Bitmex2QA_FREQUENCY_DICT = {
    "1m": '1min',
    "5m": '5min',
    "15m": '15min',
    "30m": '30min',
    "60m": '60min',
    "1d": '1day',
    "1h": '60min'
}


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_bitmex_symbols(active=True):
    """
    默认为获取活跃交易对，不获取下架交易对数据
    """
    if active:
        url = urljoin(Bitmex_base_url, "instrument/active")
    else:
        url = urljoin(Bitmex_base_url, "instrument")

    retries = 1
    while (retries != 0):
        try:
            req = requests.get(url, params={"count": 500}, timeout=TIMEOUT)
            retries = 0
        except (ConnectTimeout, ConnectionError, SSLError, ReadTimeout):
            retries = retries + 1
            if (retries % 6 == 0):
                print(ILOVECHINA)
            print("Retry instrument/active #{}".format(retries - 1))
            time.sleep(0.5)
    body = json.loads(req.content)
    return body


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_bitmex_kline(symbol, start_time, end_time, frequency):
    """
    Get the latest symbol‘s candlestick data
    """
    market = 'bitmex'
    retries = 1
    datas = list()
    url = urljoin(Bitmex_base_url, "trade/bucketed")
    while start_time < end_time:
        try:
            req = requests.get(
                url,
                params={
                    "symbol": symbol,
                    "binSize": frequency,
                    "startTime": start_time.isoformat(),
                    "endTime": end_time.isoformat(),
                    "count": MAX_HISTORY
                },
                timeout=TIMEOUT
            )
            time.sleep(0.5)
            retries = 0
        except (ConnectTimeout, ConnectionError, SSLError, ReadTimeout):
            retries = retries + 1
            if (retries % 6 == 0):
                print(ILOVECHINA)
            print("Retry trade/bucketed #{}".format(retries - 1))
            time.sleep(0.5)

        if (retries == 0):
            # 防止频率过快被断连
            remaining = int(req.headers['x-ratelimit-remaining'])
            if remaining < 20:
                time.sleep(0.5)
            elif remaining < 10:
                time.sleep(5)
            elif remaining < 3:
                time.sleep(30)

            # 成功获取才处理数据，否则继续尝试连接
            klines = json.loads(req.content)
            if len(klines) == 0:
                break
            datas.extend(klines)
            start_time = parse(klines[-1].get("timestamp")
                              ) + relativedelta(second=+1)

    if len(datas) == 0:
        return None

    # 归一化数据字段，转换填充必须字段，删除多余字段
    frame = pd.DataFrame(datas)
    frame['market'] = 'bitmex'
    # UTC时间转换为北京时间
    frame['date'] = pd.to_datetime(frame['timestamp']
                                  ).dt.tz_convert('Asia/Shanghai')
    frame['date'] = frame['date'].dt.strftime('%Y-%m-%d')
    frame['datetime'] = pd.to_datetime(frame['timestamp']
                                      ).dt.tz_convert('Asia/Shanghai')
    frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # GMT+0 String 转换为 UTC Timestamp
    frame['time_stamp'] = pd.to_datetime(frame['timestamp']
                                        ).astype(np.int64) // 10**9
    frame['date_stamp'] = pd.to_datetime(frame['date']
                                        ).astype(np.int64) // 10**9
    frame['created_at'] = int(
        time.mktime(datetime.datetime.now().utctimetuple())
    )
    frame['updated_at'] = int(
        time.mktime(datetime.datetime.now().utctimetuple())
    )
    frame.rename({'trades': 'trade'}, axis=1, inplace=True)
    frame['amount'] = frame['volume'] * (frame['open'] + frame['close']) / 2
    if (frequency != '1d'):
        frame['type'] = Bitmex2QA_FREQUENCY_DICT[frequency]
    frame.drop(
        [
            'foreignNotional',
            'homeNotional',
            'lastSize',
            'timestamp',
            'turnover',
            'vwap'
        ],
        axis=1,
        inplace=True
    )
    return json.loads(frame.to_json(orient='records'))


if __name__ == '__main__':
    print(QA_fetch_bitmex_symbols())
