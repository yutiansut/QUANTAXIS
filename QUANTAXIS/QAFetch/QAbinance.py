"""
币安api
具体api文档参考:https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
"""
import requests
import json
import datetime
import time
import pandas as pd
from requests.exceptions import ConnectTimeout

from urllib.parse import urljoin
from QUANTAXIS.QAUtil import QA_util_log_expection

Binance_base_url = "https://api.binance.com"
LIMIT_BAR = 1000
TIMEOUT = 10

columne_names = ['start_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                 'quote_asset_volume', 'num_trades', 'buy_base_asset_volume',
                 'buy_quote_asset_volume', 'Ignore']

MESSAGE_NOTICE = "同学！！你知道什么叫做科学上网么？ 如果你不知道的话，那么就加油吧！"


def QA_fetch_symbol():
    url = urljoin(Binance_base_url, "/api/v1/exchangeInfo")
    try:
        req = requests.get(url, timeout=TIMEOUT)
    except ConnectTimeout:
        raise ConnectTimeout(MESSAGE_NOTICE)
    body = json.loads(req.content)
    return body["symbols"]


def QA_fetch_kline(symbol, start_time, end_time, frequency):
    datas = list()
    start_time *= 1000
    end_time *= 1000
    while start_time < end_time:
        url = urljoin(Binance_base_url, "/api/v1/klines")
        try:
            req = requests.get(url, params={"symbol": symbol, "interval": frequency,
                                            "startTime": int(start_time),
                                            "endTime": int(end_time)}, timeout=TIMEOUT)
        except ConnectTimeout:
            raise ConnectTimeout(MESSAGE_NOTICE)
        klines = json.loads(req.content)
        if len(klines) == 0:
            break
        datas.extend(klines)
        start_time = klines[-1][6]
    if len(datas) == 0:
        return None
    frame = pd.DataFrame(datas)
    frame.columns = columne_names
    frame['symbol'] = symbol
    return json.loads(frame.to_json(orient='records'))


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
    start = time.mktime(datetime.datetime(2018, 6, 13,tzinfo=tzutc()).timetuple())
    end = time.mktime(datetime.datetime(2018, 6, 14, tzinfo=tzutc()).timetuple())
    print(start * 1000)
    print(end * 1000)
    data = QA_fetch_kline("ETHBTC", start, end, '1d')
    print(len(data))
    print(data[0])
    print(data[-1])
