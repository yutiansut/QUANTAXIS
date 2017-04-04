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
