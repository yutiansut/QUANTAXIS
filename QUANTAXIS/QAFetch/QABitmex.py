"""
bitmex api
具体api文档参考:https://www.bitmex.com/api/explorer/#/
"""

import requests
import json
import datetime
import time
import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from requests.exceptions import ConnectTimeout

from urllib.parse import urljoin
from QUANTAXIS.QAUtil.QAcrypto import TIMEOUT, ILOVECHINA

Bitmex_base_url = "https://www.bitmex.com/api/v1/"

MAX_HISTORY = 750


def QA_fetch_bitmex_symbols(active=False):
    if active:
        url = urljoin(Bitmex_base_url, "instrument/active")
    else:
        url = urljoin(Bitmex_base_url, "instrument")
    try:
        req = requests.get(url, params={"count":500}, timeout=TIMEOUT)
    except ConnectTimeout:
        raise ConnectTimeout(ILOVECHINA)
    body = json.loads(req.content)
    return body


def QA_fetch_bitmex_kline(symbol, start_time, end_time, frequency):
    datas = list()
    while start_time < end_time:
        url = urljoin(Bitmex_base_url, "trade/bucketed")
        try:
            req = requests.get(url, params={"symbol": symbol, "binSize": frequency,
                                            "startTime": start_time.isoformat(),
                                            "endTime": end_time.isoformat(),
                                            "count":MAX_HISTORY}, timeout=TIMEOUT)
        except ConnectTimeout:
            raise ConnectTimeout(ILOVECHINA)
        # 防止频率过快被断连
        remaining = int(req.headers['x-ratelimit-remaining'])
        if remaining <20:
            time.sleep(0.5)
        elif remaining <10:
            time.sleep(5)
        elif remaining <3:
            time.sleep(30)

        klines = json.loads(req.content)
        if len(klines) == 0:
            break
        datas.extend(klines)
        start_time = parse(klines[-1].get("timestamp")) + relativedelta(second=+1)
    if len(datas) == 0:
        return None
    frame = pd.DataFrame(datas)
    frame['timestamp'] = pd.to_datetime(frame['timestamp'])
    return json.loads(frame.to_json(orient='records'))


if __name__ == '__main__':
    print(QA_fetch_bitmex_symbols())