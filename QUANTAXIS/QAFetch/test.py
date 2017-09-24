import datetime

import numpy as np
import pandas as pd
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API
from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_date_str2int,
                              QA_util_date_valid, QA_util_get_real_date,
                              QA_util_get_real_datelist, QA_util_log_info,
                              QA_util_time_stamp, QA_util_web_ping,
                              trade_date_sse)
import asyncio
import tushare as ts


def ping(ip):
    api = TdxHq_API()
    __time1 = datetime.datetime.now()
    try:
        with api.connect(ip, 7709):
            if len(api.get_security_list(0, 1)) > 800:
                return datetime.datetime.now() - __time1
    except:
        print('Bad REPSONSE %s' % ip)
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    QA_util_log_info('Selecting the Best Server IP of TDX')
    listx = ['218.75.126.9', '115.238.90.165',
             '124.160.88.183', '60.12.136.250', '218.108.98.244', '218.108.47.69',
             '14.17.75.71', '180.153.39.51']
    data = [ping(x) for x in listx]
    QA_util_log_info('===The BEST SERVER is :  %s ===' %
                     (listx[data.index(min(data))]))
    return listx[data.index(min(data))]


best_ip = select_best_ip()

# return 1 if sh, 0 if sz


def __select_market_code(code):
    code = str(code)
    if code[0] in ['5', '6', '9'] or code[:3] in ["009", "126", "110", "201", "202", "203", "204"]:
        return 1
    return 0


def QA_fetch_get_stock_realtime(code=['000001', '000002'], ip=best_ip, port=7709):
    api = TdxHq_API()
    __data = pd.DataFrame()
    code = [code] if type(code) is str else code






    async def _get_security_quotes(__code):
        """
        """
        assert isinstance(__code, str)

        data=await api.get_security_quotes([(__select_market_code(__code), __code)])
        data=api.to_df(data)
        data['datetime'] = datetime.datetime.now()

        return data[['datetime', 'code', 'open', 'high', 'low', 'price']]

    with api.connect(ip, port):
        coroutines = [asyncio.ensure_future(
            _get_security_quotes(code_)) for code_ in code]

        print(coroutines)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        res = loop.run_until_complete(asyncio.gather(*coroutines))
        print(res)
        return res


if __name__ == '__main__':
    print(QA_fetch_get_stock_realtime())
