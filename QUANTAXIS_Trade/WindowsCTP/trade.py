import ctypes
import os
import sys
import threading
import time
from ctypes import *
from config import api,account_info
import numpy as np
sys.path.append(os.path.dirname(__file__))
api = cdll.LoadLibrary('hqdll.dll')

ip_hq = 'tcp://180.168.146.187:10011'
ip_trade = 'tcp://180.168.146.187:10001'
broker_id = "9999"
instrument_list = ['T1806', 'rb1810']
count = len(instrument_list)

instrument_list_bytes = []
for items in instrument_list:
    instrument_list_bytes.append(c_char_p(bytes(items, 'utf-8')))

orderid = str(123)
print(orderid)
input()
api.tradeorder(c_char_p(bytes(instrument_list[0], 'utf-8')), c_int(1), c_int(5), c_double(1840),
               c_char_p(bytes(orderid, 'utf-8')))
