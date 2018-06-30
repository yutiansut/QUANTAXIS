import os
import random
import sys
import threading
import time
from ctypes import *

import numpy as np

from config import *

lock = threading.Lock()
# def get_timingprice(*instrument_list):
#
#     while(1):
#         price = api.getprice(c_char_p(bytes(instrument_list[0], 'utf-8')))
#         global closelist
#         closelist.append(price)

# 启动行情服务


def start_hq(instrument_list, account_info):

    instrument_list_bytes = []

    for items in instrument_list:
        instrument_list_bytes.append(c_char_p(bytes(items, 'utf-8')))

    # 转成c++需要的数据格式
    instrument = (c_char_p * len(instrument_list))(*instrument_list_bytes)
    count = len(instrument_list)

    # 初始化行情接口
    api.init(c_char_p(bytes(account_info['ip_hq'], 'utf-8')), c_char_p(bytes(account_info['ip_trade'], 'utf-8')),
             c_char_p(bytes(account_info['broker_id'], 'utf-8')
                      ), c_char_p(bytes(account_info['account'], 'utf-8')),
             c_char_p(bytes(account_info['pwd'], 'utf-8')), instrument, c_int(count))
    # 创建行情实例
    api.creathqapi()
    time.sleep(2)
    api.subscribemarketdata(instrument, count)
    time.sleep(2)
    # 获取价格
    api.getprice.restype = c_double  # 设置python接受dll函数的返回类
    price = None
    price = api.getprice(c_char_p(bytes(instrument_list[0], 'utf-8')))
    print(price)
    if price:
        return True
    else:
        return False

# 启动交易服务


def start_jy():

    # 创建交易实例
    api.creattradeapi()
    # 确认账户
    time.sleep(2)
    api.accountconfirm()
    time.sleep(2)
    resturntype = api.checkconfirm
    resturntype.restype = c_int
    trade = api.checkconfirm()
    if trade == 1:
        return True
    else:
        return False

# 获取实时行情


def get_instrument_timingprice(instrument_list):

    while(1):
        for instrument in instrument_list:
            price = api.getprice(c_char_p(bytes(instrument, 'utf-8')))
            instrument_price[instrument] = price

# 生成唯一的下单orderid


def get_orderid(index=10):

    global OrderId
    while(1):

        neworderid = str(int(round(time.time() * 1000))+1)[-index:]

        if neworderid == OrderId:
            neworderid = str(int(round(time.time() * 1000)))[-index:]
        else:
            OrderId = neworderid
            break

    return OrderId
