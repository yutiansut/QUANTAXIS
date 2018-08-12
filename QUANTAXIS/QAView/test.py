import numpy as np
import pandas as pd
import matplotlib
import tushare as ts
import datetime
import time
import talib as ta
from pandas.tseries.offsets import BDay
import re
import os
import sys
import QUANTAXIS as QA


#wh = QA.Warehouse_Daily(source=QA.DATASOURCE.LOCALFILE)

#wh = QA.Warehouse_Daily(source=QA.DATASOURCE.TUSHARE, start = '2017-01-01', end = "2018-06-01")
#print(wh)
#wh.update_realtime()

df = QA.QA_fetch_stock_list_adv()
dict = df.values
print(dict)
for item in dict:
    #print(item)
    if r"00029" in item[0]:
        print(item)


