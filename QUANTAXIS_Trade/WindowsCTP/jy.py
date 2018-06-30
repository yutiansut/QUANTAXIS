import ctypes
import os
import sys
import threading
import time
from ctypes import *
from config import api
import numpy as np


ip_hq = 'tcp://180.168.146.187:10011'
ip_trade = 'tcp://180.168.146.187:10001'
broker_id = "9999"
account = input("account")
pwd = input("pwd")
instrument_list = ['j1809', 'rb1810']
count = len(instrument_list)

instrument_list_bytes = []
for items in instrument_list:
    instrument_list_bytes.append(c_char_p(bytes(items, 'utf-8')))

# 转成c++需要的数据格式
instrument = (c_char_p * len(instrument_list))(*instrument_list_bytes)
api.init(c_char_p(bytes(ip_hq, 'utf-8')), c_char_p(bytes(ip_trade, 'utf-8')), c_char_p(bytes(broker_id,
                                                                                             'utf-8')), c_char_p(bytes(account, 'utf-8')), c_char_p(bytes(pwd, 'utf-8')), instrument, c_int(count))
api.creattradeapi()

# 确认账户
time.sleep(5)
api.accountconfirm()
time.sleep(5)

api.checkconfirm.restype = c_int
trade = api.checkconfirm()
time.sleep(5)
print(trade)
if trade == 1:
    print("账户确认成功")
