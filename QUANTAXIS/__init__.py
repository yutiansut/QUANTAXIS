#coding ：utf-8

"""
QUANTAXIS
Quantitative Financial Strategy Framework
by yutiansut
2017/4/3 
"""

from QUANTAXIS.QAFetch.main import (get_stock_day,get_trade_date,get_stock_indicator)
from QUANTAXIS.QAMarket import (deal)
from QUANTAXIS.QASpider import (select_spider,start_spider,end_spider)
from QUANTAXIS.QATasks import (tasks,control)
from QUANTAXIS.QAUpdate.windsave import (save_stock_list)
from QUANTAXIS.QAUtil import (util_date_stamp,util_time_stamp,util_ms_stamp)

print('Welcome to QUANTAXIS, the Version is 0.3.8-beta')