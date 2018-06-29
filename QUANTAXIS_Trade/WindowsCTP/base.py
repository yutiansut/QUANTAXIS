import ctypes
import os
import sys
import time
from ctypes import *

import numpy as np


class FullMarketInfo(Structure):
    _fields_ = [('BidPrice1', c_double), ('BidVolume1', c_int), ('AskPrice1', c_double), ('AskVolume1', c_int),
                ('BidPrice2', c_double), ('BidVolume2',
                                          c_int), ('AskPrice2', c_double), ('AskVolume2', c_int),
                ('BidPrice3', c_double), ('BidVolume3',
                                          c_int), ('AskPrice3', c_double), ('AskVolume3', c_int),
                ('BidPrice4', c_double), ('BidVolume4',
                                          c_int), ('AskPrice4', c_double), ('AskVolume4', c_int),
                ('BidPrice5', c_double), ('BidVolume5',
                                          c_int), ('AskPrice5', c_double), ('AskVolume5', c_int),
                ]


fullmarketinfo = FullMarketInfo()


# # 获取账户权益信息
# class AccountEqulity(Structure):
#     _fields_ = [('prebalance', c_double),
#                 ('balance', c_double),
#                 ('available', c_double),
#                 ]
#
#
# acountinfo = AccountEqulity()
# api.getaccountequity.restype = POINTER(AccountEqulity)
# acountinfo = api.getaccountequity()
#
# print(acountinfo.contents.prebalance)
# print(acountinfo.contents.balance)
# print(acountinfo.contents.available)
