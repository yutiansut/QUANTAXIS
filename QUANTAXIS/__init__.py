#coding :utf-8

"""
QUANTAXIS

Quantitative Financial Strategy Framework

by yutiansut

2017/4/8
"""
# fetch methods

from QUANTAXIS.QAFetch import (QA_fetch_get_stock_day,QA_fetch_get_trade_date,
                                QA_fetch_get_stock_indicator)
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_data

from QUANTAXIS.QASpider import (QA_spider_select_spider,QA_spider_start_spider,
                                QA_spider_end_spider)

# job center
from QUANTAXIS.QATask import (tasks,control)

# save
from QUANTAXIS.QASU.main import ( QA_SU_save_stock_list, QA_SU_save_stock_day,
                                    QA_SU_save_stock_day_init,  QA_SU_save_trade_date)
from QUANTAXIS.QASU.user import (QA_user_sign_in,QA_user_sign_up)
# event driver
from QUANTAXIS.QASignal import (QA_signal_resend, QA_signal_send, QA_Signal_eventManager,
                                QA_Signal_events, QA_Signal_Sender, QA_Signal_Listener,QA_signal_usual_model)
# market

from QUANTAXIS.QAMarket import (QA_QAMarket_bid,QA_Market)

# Account,Risk,Portfolio
from QUANTAXIS.QAARP import (QAAccount,QAPortfolio,QARisk)
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QARisk import QA_Risk
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
# Backtest
from QUANTAXIS.QABacktest.QABacktest import QA_Backtest
from QUANTAXIS.QABacktest.QABacktest_standard import QA_backtest_standard_record_account,QA_backtest_standard_record_market                   

# Util
from QUANTAXIS.QAUtil import (QA_util_sql_mongo_setting, QA_util_cfg_initial, QA_util_realtime,
                                QA_util_date_stamp, QA_util_time_stamp, QA_util_ms_stamp,
                                QA_util_log_debug, QA_util_log_expection, QA_util_log_info,
                                QA_start_initial,QA_Setting)
# CMD and Cli
import QUANTAXIS.QACmd

from QUANTAXIS.QACmd import QA_cmd
import argparse
QA_util_log_info('Welcome to QUANTAXIS, the Version is 0.3.8-dev-RC-ARP')


def QA_help_fetch(self):
    QA_util_log_info('QA_fetch_get_stock_day,QA_fetch_get_trade_date,QA_fetch_get_stock_indicator')
def QA_help_su(self):
    QA_util_log_info('QA_SU_save_stock_list, QA_SU_save_stock_day,QA_SU_save_stock_day_init, QA_SU_save_trade_date')


def main():
    QA_cmd()