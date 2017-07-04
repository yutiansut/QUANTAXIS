# coding:utf-8

from pytdx.hq import TdxHq_API
import pandas as pd
import numpy as np
from QUANTAXIS.QAUtil import QA_util_date_valid, QA_util_log_info

# 基于Pytdx的实现,具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#
# pytdx.hq.GetCompanyInfoCategory()
api = TdxHq_API()


def __select_best_ip():
    ip_list = [
        '119.147.212.81:7709',
        '221.231.141.60:7709',
        '101.227.73.20:7709',
        '101.227.77.254:7709',
        '14.215.128.18:7709'
        '59.173.18.140:7709',
        '58.23.131.163:7709',
        '218.6.170.47:7709',
        '123.125.108.14:7709',
        '60.28.23.80:7709',
        '218.60.29.136:7709',
        '218.85.139.19:7709',
        '218.85.139.20:7709',
        '122.192.35.44:7709',
        '122.192.35.44:7709'
    ]


def QA_fetch_get_stock_day(code, date):
    with api.connect('119.147.212.81', 7709):
        data = api.get_security_bars(9, 0, '000001', 0, 10)  # 返回普通list
        data = api.to_df(api.get_security_bars(
            9, 0, '000001', 0, 10))  # 返回DataFrame
    return data
