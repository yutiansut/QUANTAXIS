# coding:utf-8

from pytdx.hq import TdxHq_API
import pandas as pd
import numpy as np
from QUANTAXIS.QAUtil import QA_util_date_valid, QA_util_log_info,QA_util_web_ping

# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#

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



    ip_addr=[]
    for item in ip_list:
        ip_addr.append(item.split(':')[0])



    def select_best(url_list):
        ms_list=[]
        for item in url_list:
            ms_list.append(QA_util_web_ping(item))
        return url_list[ms_list.index(min(ms_list))]

    #ip_job.put({'fn':print(select_best(ip_addr))})






"""
from Pytdx/api-main
    api = TdxHq_API()
    if api.connect('101.227.73.20', 7709):
        log.info("获取股票行情")
        stocks = api.get_security_quotes([(0, "000001"), (1, "600300")])
        pprint.pprint(stocks)
        log.info("获取k线")
        data = api.get_security_bars(9,0, '000001', 4, 3)
        pprint.pprint(data)
        log.info("获取 深市 股票数量")
        pprint.pprint(api.get_security_count(0))
        log.info("获取股票列表")
        stocks = api.get_security_list(1, 255)
        pprint.pprint(stocks)
        log.info("获取指数k线")
        data = api.get_index_bars(9,1, '000001', 1, 2)
        pprint.pprint(data)
        log.info("查询分时行情")
        data = api.get_minute_time_data(TDXParams.MARKET_SH, '600300')
        pprint.pprint(data)
        log.info("查询历史分时行情")
        data = api.get_history_minute_time_data(TDXParams.MARKET_SH, '600300', 20161209)
        pprint.pprint(data)
        log.info("查询分时成交")
        data = api.get_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 30)
        pprint.pprint(data)
        log.info("查询历史分时成交")
        data = api.get_history_transaction_data(TDXParams.MARKET_SZ, '000001', 0, 10, 20170209)
        pprint.pprint(data)
        log.info("查询公司信息目录")
        data = api.get_company_info_category(TDXParams.MARKET_SZ, '000001')
        pprint.pprint(data)
        log.info("读取公司信息-最新提示")
        data = api.get_company_info_content(0, '000001', '000001.txt', 0, 10)
        pprint.pprint(data)
        log.info("读取除权除息信息")
        data = api.get_xdxr_info(1, '600300')
        pprint.pprint(data)
        log.info("读取财务信息")
        data = api.get_finance_info(0, '000001')
        pprint.pprint(data)

        api.disconnect()
"""
def QA_fetch_get_stock_day(code, date,ip='119.147.212.81',port=7709):
    with api.connect(ip, port):
        data = api.get_security_bars(9, 0, code, 0, 10)  # 返回普通list
        data = api.to_df(api.get_security_bars(
            9, 0, '000001', 0, 10))  # 返回DataFrame
    return data
def QA_fetch_get_stock_list(code, date,ip='119.147.212.81',port=7709):
    with api.connect(ip, port):
        stocks = api.get_security_list(1, 255)
        return stocks
def QA_fetch_get_stock_realtime(code, date,ip='119.147.212.81',port=7709):
    with api.connect(ip, port):
        stocks = api.get_security_quotes([(0, "000001")])
        return stocks
    
def QA_fetch_get_index_day(code, date,ip='119.147.212.81',port=7709):
    with api.connect(ip, port):
        stocks = api.get_index_bars(9,1, '000001', 1, 2)
    return stocks
 