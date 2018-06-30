import ctypes
import os
import sys
import threading
import time
from ctypes import *

import numpy as np


def get_timingprice(*instrument_list):

    while(1):
        price = api.getprice(c_char_p(bytes(instrument_list[0], 'utf-8')))
        global closelist
        closelist.append(price)


ip_hq = 'tcp://180.168.146.187:10011'
ip_trade = 'tcp://180.168.146.187:10001'
broker_id = "9999"
account = input("account")
pwd = input("pwd")
instrument_list = ['j1809', 'rb1810']
count = len(instrument_list)
api = cdll.LoadLibrary('E:\\research\\strategry\\crerathapi\\hqdll.dll')

instrument_list_bytes = []
for items in instrument_list:
    instrument_list_bytes.append(c_char_p(bytes(items, 'utf-8')))

# 转成c++需要的数据格式
instrument = (c_char_p * len(instrument_list))(*instrument_list_bytes)

api.init(c_char_p(bytes(ip_hq, 'utf-8')), c_char_p(bytes(ip_trade, 'utf-8')), c_char_p(bytes(broker_id,
                                                                                             'utf-8')), c_char_p(bytes(account, 'utf-8')), c_char_p(bytes(pwd, 'utf-8')), instrument, c_int(count))
api.creathqapi()
time.sleep(5)
api.subscribemarketdata(instrument, 2)
time.sleep(5)

# 获取价格
api.getprice.restype = c_double  # 设置python接受dll函数的返回类型
price = api.getprice(c_char_p(bytes(instrument_list[0], 'utf-8')))
print(price)


# 创建交易实例
api.creattradeapi()
# 确认账户
time.sleep(5)
api.accountconfirm()
time.sleep(5)
resturntype = api.checkconfirm
resturntype.restype = c_int
trade = api.checkconfirm()
time.sleep(5)
print(trade)
if trade == 1:
    print("账户确认成功")

# 下单逻辑
baseprice = 3492
closelist = []

# 起一个线程获取实时价格
getprice = threading.Thread(target=get_timingprice, args=(instrument_list[0],))
getprice.start()
p1, p2, p3 = 0, 0, 0
# orderid = int(round(time.time() * 1000))
times = 0
orderid = ''
api.getdealstatus.restype = c_double
api.getorderstatus.restype = c_double

while(1):

    try:

        price = closelist[-1]
        p = p1
        p1 = p2
        p2 = p3
        p3 = price
        times = times + 1
        orderid = str(times+1)
        # 调整的价格必须是期货品种的跳数
        if p3 > p2 and p2 > p1:
            api.tradeorder(c_char_p(bytes(instrument_list[0], 'utf-8')), c_int(1), c_int(5), c_double(price),
                           c_char_p(bytes(orderid, 'utf-8')))
        if p3 < p2 and p2 < p1:
            api.tradeorder(c_char_p(bytes(instrument_list[0], 'utf-8')), c_int(-1), c_int(5), c_double(price),
                           c_char_p(bytes(orderid, 'utf-8')))

        # 撤掉上一笔没有成交的报单
        time.sleep(1)
        deal_num = -1
        status = -1

        try:
            deal_num = api.getdealstatus(c_char_p(bytes(orderid, 'utf-8')))
            status = api.getorderstatus(c_char_p(bytes(orderid, 'utf-8')))
        except:
            pass

        if deal_num < 5 and status != 5.0 and status != -1:
            try:
                api.cancelorder(c_char_p(
                    bytes(instrument_list[0], 'utf-8')), c_char_p(bytes(orderid, 'utf-8')))
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)
        print("error")


# orderid = 'abc' # 下单id,以时间戳创建
# times = 1
# orderid = str(times)
# # 调整的价格必须是期货品种的跳数
# api.tradeorder(c_char_p(bytes(instrument_list[0], 'utf-8')), c_int(1), c_int(1), c_double(price - 1),c_char_p(bytes(orderid, 'utf-8')))
#
#

# 下单
# orderid = 'abc' # 下单id,以时间戳创建
# times = 1
# while(times < 5):
#     orderid = str(times)
#     # 调整的价格必须是期货品种的跳数
#     api.tradeorder(c_char_p(bytes(instrument_list[0], 'utf-8')), c_int(1), c_int(10), c_double(price - 1),c_char_p(bytes(orderid, 'utf-8')))
#     time.sleep(5)
#     # api.getorderstatus.restype = c_double
#     # status = api.getorderstatus(c_char_p(bytes(orderid, 'utf-8')))
#     # print(status)
#     # api.getdealstatus.restype = c_double
#     # deal = api.getdealstatus(c_char_p(bytes(orderid, 'utf-8')))
#     # print(deal)
#     # 撤单
#
#     api.cancelorder(c_char_p(bytes(instrument_list[0], 'utf-8')), c_char_p(bytes(orderid, 'utf-8')))
#     time.sleep(5)
#     times +=1
