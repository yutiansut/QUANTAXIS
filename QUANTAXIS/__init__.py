#coding ：utf-8

"""
QUANTAXIS
Quantitative Financial Strategy Framework
by yutiansut
2017/4/3 
"""
from WindPy import w
w.start()
from QUANTAXIS.QAFetch.main import (get_stock_day,get_trade_date,get_stock_indicator)
from QUANTAXIS.QAMarket import (deal)
from QUANTAXIS.QASpider import (select_spider,start_spider,end_spider)
from QUANTAXIS.QATasks import (tasks,control)
from QUANTAXIS.QASU.save_wind import (save_stock_list)
from QUANTAXIS.QAUtil import (sql_mongo_setting,util_date_stamp,util_time_stamp,util_ms_stamp)

print('Welcome to QUANTAXIS, the Version is 0.3.8-beta')

def first_run():
    pass

def initial():
    pass