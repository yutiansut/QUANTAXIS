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
#from QUANTAXIS.QAStrategy import (start_strategy,import_strategy,analysis_strategy,c)
from QUANTAXIS.QASU.save_wind import (save_stock_list,save_stock_day,save_stock_day_init,save_trade_date)
from QUANTAXIS.QAUtil import (sql_mongo_setting,util_date_stamp,util_time_stamp,util_ms_stamp,QALog)

print('Welcome to QUANTAXIS, the Version is 0.3.8-beta')

def first_run():
    save_stock_day_init()
    QALog('first_run_quantaxis')
    pass

def initial():
    pass