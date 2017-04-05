#coding ：utf-8

"""
QUANTAXIS

Quantitative Financial Strategy Framework

by yutiansut

2017/4/5
"""

from QUANTAXIS.QAFetch import (QA_fetch_get_stock_day,QA_fetch_get_trade_date,
                                QA_fetch_get_stock_indicator)

from QUANTAXIS.QAMarket import (deal)

from QUANTAXIS.QASpider import (QA_spider_select_spider,QA_spider_start_spider,
                                QA_spider_end_spider)

from QUANTAXIS.QATasks import (tasks,control)
from QUANTAXIS.QAARP import (QAAccount,QAPortfolio,QARisk)
from QUANTAXIS.QASignal import (QA_signal_resend,QA_signal_send)
from QUANTAXIS.QAStrategy import (QA_strategy_analysis,QA_strategy_choice,QA_strategy_import,QA_strategy_start)
#from QUANTAXIS.QAStrategy import (start_strategy,import_strategy,analysis_strategy,c)

from QUANTAXIS.QASU.save_wind import ( QA_SU_save_stock_list, QA_SU_save_stock_day,
                                    QA_SU_save_stock_day_init,QA_SU_save_stock_day_init_simple, QA_SU_save_trade_date)

from QUANTAXIS.QAUtil import (QA_util_sql_mongo_setting,QA_util_cfg_initial,
                                QA_util_date_stamp, QA_util_time_stamp, QA_util_ms_stamp,
                                QA_util_log_debug,QA_util_log_expection,QA_util_log_info,
                                QA_start_initial)

import QUANTAXIS.QACmd

QA_util_log_info('Welcome to QUANTAXIS, the Version is 0.3.8-beta')

def QA_start_first_run():
    QA_SU_save_stock_day_init_simple()
    QA_util_log_info('first_run_quantaxis')
    pass


def QA_close():
    pass
def QA_help_fetch():
    QA_util_log_info('QA_fetch_get_stock_day,QA_fetch_get_trade_date,QA_fetch_get_stock_indicator')
def QA_help_su():
    QA_util_log_info('QA_SU_save_stock_list, QA_SU_save_stock_day,QA_SU_save_stock_day_init, QA_SU_save_trade_date')