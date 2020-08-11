#coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
QUANTAXIS

Quantitative Financial Strategy Framework

by yutiansut

2017/4/8
"""

__version__ = '1.9.32'
__author__ = 'yutiansut'

import argparse
# check
import sys

# CMD and Cli
import QUANTAXIS.QACmd
from QUANTAXIS.QAAnalysis import *
from QUANTAXIS.QAApplication.QAAnalysis import QA_backtest_analysis_backtest
# Backtest
from QUANTAXIS.QAApplication.QABacktest import QA_Backtest
from QUANTAXIS.QAApplication.QAResult import backtest_result_analyzer
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio, QA_PortfolioView
from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
from QUANTAXIS.QAARP.QAStrategy import QA_Strategy
from QUANTAXIS.QAARP.QAUser import QA_User
from QUANTAXIS.QACmd import QA_cmd
# Data
from QUANTAXIS.QAData import (
    QA_data_calc_marketvalue,
    QA_data_ctptick_resample,
    QA_data_day_resample,
    QA_data_futuremin_resample,
    QA_data_futuremin_resample_series,
    QA_data_futuremin_resample_tb_kq,
    QA_data_futuremin_resample_tb_kq2,
    QA_data_marketvalue,
    QA_data_min_resample,
    QA_data_min_to_day,
    QA_data_stock_to_fq,
    QA_data_tick_resample,
    QA_data_tick_resample_1min,
    QA_data_cryptocurrency_min_resample,
    QA_DataStruct_Day,
    QA_DataStruct_Financial,
    QA_DataStruct_Future_day,
    QA_DataStruct_Future_min,
    QA_DataStruct_Index_day,
    QA_DataStruct_Index_min,
    QA_DataStruct_Indicators,
    QA_DataStruct_Min,
    QA_DataStruct_Series,
    QA_DataStruct_Stock_block,
    QA_DataStruct_Stock_day,
    QA_DataStruct_Stock_min,
    QA_DataStruct_Stock_realtime,
    QA_DataStruct_Stock_transaction,
    QA_DataStruct_CryptoCurrency_day,
    QA_DataStruct_CryptoCurrency_min,
    QDS_IndexDayWarpper,
    QDS_IndexMinWarpper,
    QDS_StockDayWarpper,
    QDS_StockMinWarpper,
    from_tushare
)
from QUANTAXIS.QAData.dsmethods import *
# ENGINE
from QUANTAXIS.QAEngine import (
    QA_AsyncExec,
    QA_AsyncQueue,
    QA_AsyncScheduler,
    QA_AsyncTask,
    QA_AsyncThread,
    QA_Engine,
    QA_Event,
    QA_Task,
    QA_Thread,
    QA_Worker
)
from QUANTAXIS.QAFetch import (
    QA_fetch_get_chibor,
    QA_fetch_get_exchangerate_day,
    QA_fetch_get_exchangerate_list,
    QA_fetch_get_exchangerate_min,
    QA_fetch_get_future_day,
    QA_fetch_get_future_list,
    QA_fetch_get_future_min,
    QA_fetch_get_bond_day,
    QA_fetch_get_bond_min,
    QA_fetch_get_bond_list,
    QA_fetch_get_bond_realtime,
    QA_fetch_get_future_realtime,
    QA_fetch_get_future_domain,
    QA_fetch_get_future_transaction,
    QA_fetch_get_future_transaction_realtime,
    QA_fetch_get_globalfuture_day,
    QA_fetch_get_globalfuture_list,
    QA_fetch_get_globalfuture_min,
    QA_fetch_get_globalindex_day,
    QA_fetch_get_globalindex_list,
    QA_fetch_get_globalindex_min,
    QA_fetch_get_hkfund_day,
    QA_fetch_get_hkfund_list,
    QA_fetch_get_hkfund_min,
    QA_fetch_get_hkindex_day,
    QA_fetch_get_hkindex_list,
    QA_fetch_get_hkindex_min,
    QA_fetch_get_hkstock_day,
    QA_fetch_get_hkstock_list,
    QA_fetch_get_hkstock_min,
    QA_fetch_get_index_day,
    QA_fetch_get_index_list,
    QA_fetch_get_index_min,
    QA_fetch_get_index_realtime,
    QA_fetch_get_macroindex_day,
    QA_fetch_get_macroindex_list,
    QA_fetch_get_macroindex_min,
    QA_fetch_get_option_day,
    QA_fetch_get_option_list,
    QA_fetch_get_option_min,
    QA_fetch_get_security_bars,
    QA_fetch_get_stock_block,
    QA_fetch_get_stock_day,
    QA_fetch_get_stock_indicator,
    QA_fetch_get_stock_info,
    QA_fetch_get_stock_list,
    QA_fetch_get_stock_min,
    QA_fetch_get_stock_realtime,
    QA_fetch_get_stock_transaction,
    QA_fetch_get_stock_transaction_realtime,
    QA_fetch_get_index_transaction,
    QA_fetch_get_stock_xdxr,
    QA_fetch_get_trade_date,
    QA_fetch_get_usstock_day,
    QA_fetch_get_usstock_list,
    QA_fetch_get_usstock_min,
    get_stock_market
)
# fetch methods
from QUANTAXIS.QAFetch.Fetcher import QA_quotation
from QUANTAXIS.QAFetch.QACrawler import (
    QA_fetch_get_sh_margin,
    QA_fetch_get_sz_margin
)
from QUANTAXIS.QAFetch.QAQuery import (
    QA_fetch_account,
    QA_fetch_backtest_history,
    QA_fetch_backtest_info,
    QA_fetch_ctp_tick,
    QA_fetch_etf_list,
    QA_fetch_etf_name,
    QA_fetch_financial_report,
    QA_fetch_future_day,
    QA_fetch_future_list,
    QA_fetch_future_min,
    QA_fetch_future_tick,
    QA_fetch_index_day,
    QA_fetch_index_list,
    QA_fetch_index_min,
    QA_fetch_index_name,
    QA_fetch_quotation,
    QA_fetch_quotations,
    QA_fetch_stock_block,
    QA_fetch_stock_day,
    QA_fetch_stock_adj,
    QA_fetch_stock_full,
    QA_fetch_stock_info,
    QA_fetch_stock_list,
    QA_fetch_stock_min,
    QA_fetch_stock_transaction,
    QA_fetch_index_transaction,
    QA_fetch_stock_name,
    QA_fetch_stock_xdxr,
    QA_fetch_trade_date,
    QA_fetch_cryptocurrency_day,
    QA_fetch_cryptocurrency_min,
    QA_fetch_cryptocurrency_list
)
from QUANTAXIS.QAFetch.QAQuery_Advance import *
from QUANTAXIS.QAIndicator import *
# market
from QUANTAXIS.QAMarket import (
    QA_BacktestBroker,
    QA_Broker,
    QA_Dealer,
    QA_Market,
    QA_Order,
    QA_OrderHandler,
    QA_OrderQueue,
    QA_Position,
    QA_RandomBroker,
    QA_RealBroker,
    QA_SimulatedBroker,
    QA_TTSBroker
)
from QUANTAXIS.QASetting.QALocalize import (
    cache_path,
    download_path,
    log_path,
    qa_path,
    setting_path
)
# save
from QUANTAXIS.QASU.main import (
    QA_SU_save_etf_day,
    QA_SU_save_etf_min,
    QA_SU_save_financialfiles,
    QA_SU_save_future_list,
    QA_SU_save_index_day,
    QA_SU_save_index_list,
    QA_SU_save_index_min,
    QA_SU_save_stock_block,
    QA_SU_save_stock_day,
    QA_SU_save_stock_info,
    QA_SU_save_stock_info_tushare,
    QA_SU_save_stock_list,
    QA_SU_save_stock_min,
    QA_SU_save_stock_min_5,
    QA_SU_save_stock_xdxr
)
from QUANTAXIS.QASU.save_strategy import QA_SU_save_strategy
from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil import (  # QAPARAMETER
    AMOUNT_MODEL, BROKER_EVENT, BROKER_TYPE, DATABASE, DATASOURCE,
    ENGINE_EVENT, EXCHANGE_ID, FREQUENCE, MARKET_ERROR, MARKET_EVENT,
    MARKET_TYPE, ORDER_DIRECTION, ORDER_EVENT, ORDER_MODEL, ORDER_STATUS,
    OUTPUT_FORMAT, RUNNING_ENVIRONMENT, RUNNING_STATUS, TRADE_STATUS,
    QA_Setting, QA_util_calc_time, QA_util_cfg_initial, QA_util_code_tolist,
    QA_util_code_tostr, QA_util_date_gap, QA_util_date_int2str,
    QA_util_code_adjust_ctp, QA_util_stamp2datetime,
    QA_util_date_stamp, QA_util_date_str2int, QA_util_date_today,
    QA_util_date_valid, QA_util_dict_remove_key, QA_util_diff_list,
    QA_util_file_md5, QA_util_format_date2str, QA_util_get_cfg,
    QA_util_get_date_index, QA_util_get_index_date, QA_util_get_last_datetime,
    QA_util_get_last_day, QA_util_get_next_datetime, QA_util_get_next_day,
    QA_util_get_next_trade_date, QA_util_get_order_datetime,
    QA_util_get_pre_trade_date, QA_util_get_real_date,
    QA_util_get_real_datelist, QA_util_get_trade_datetime,
    QA_util_get_trade_gap, QA_util_get_trade_range, QA_util_id2date,
    QA_util_if_trade, QA_util_if_tradetime, QA_util_is_trade,
    QA_util_log_debug, QA_util_log_expection, QA_util_log_info,
    QA_util_make_hour_index, QA_util_make_min_index, QA_util_mongo_infos,
    QA_util_mongo_initial, QA_util_mongo_status, QA_util_ms_stamp,
    QA_util_multi_demension_list, QA_util_random_with_topic, QA_util_realtime,
    QA_util_save_csv, QA_util_select_hours, QA_util_select_min,
    QA_util_send_mail, QA_util_sql_async_mongo_setting,
    QA_util_sql_mongo_setting, QA_util_sql_mongo_sort_ASCENDING,
    QA_util_sql_mongo_sort_DESCENDING, QA_util_tdxtimestamp,
    QA_util_time_delay, QA_util_time_gap, QA_util_time_now, QA_util_time_stamp,
    QA_util_to_datetime, QA_util_to_json_from_pandas,
    QA_util_to_list_from_numpy, QA_util_to_list_from_pandas,
    QA_util_to_pandas_from_json, QA_util_to_pandas_from_list, QA_util_web_ping,
    QATZInfo_CN, future_ip_list, info_ip_list, stock_ip_list, trade_date_sse,
    QA_util_get_next_period)

# Factor
from QUANTAXIS.QAFactor.analyze import FactorAnalyzer
from QUANTAXIS.QAFactor.data import DataApi
from QUANTAXIS.QAFactor.preprocess import (
    QA_fmt_factor,
    QA_fetch_factor_weight,
    QA_fetch_get_factor_groupby,
    QA_standardize_factor,
    QA_winsorize_factor
)
from QUANTAXIS.QAFactor.utils import QA_fmt_code_list

# from QUANTAXIS.QASU.save_backtest import (
#     QA_SU_save_account_message, QA_SU_save_backtest_message, QA_SU_save_account_to_csv)

# event driver

# Account,Risk,Portfolio,User,Strategy

# Setting

# Util

#from QUANTAXIS.QAFetch.QATdx_adv import bat

if sys.version_info.major != 3 or sys.version_info.minor not in [4, 5, 6, 7, 8]:
    print('wrong version, should be 3.4/3.5/3.6/3.7/3.8 version')
    sys.exit()

#QA_util_log_info('Welcome to QUANTAXIS, the Version is {}'.format(__version__))


def __repr__():
    return ' \n \
            ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
            ``########`````##````````##``````````##`````````####````````##```##########````````#``````##``````###```##`````######`` \n \
            `##``````## ```##````````##`````````####````````##`##```````##```````##```````````###``````##````##`````##```##`````##` \n \
            ##````````##```##````````##````````##`##````````##``##``````##```````##``````````####```````#```##``````##```##``````## \n \
            ##````````##```##````````##```````##```##```````##```##`````##```````##`````````##`##```````##`##```````##````##``````` \n \
            ##````````##```##````````##``````##`````##``````##````##````##```````##````````##``###```````###````````##`````##`````` \n \
            ##````````##```##````````##``````##``````##`````##`````##```##```````##```````##````##```````###````````##``````###```` \n \
            ##````````##```##````````##`````##````````##````##``````##``##```````##``````##``````##`````##`##```````##````````##``` \n \
            ##````````##```##````````##````#############````##```````##`##```````##`````###########`````##``##``````##`````````##`` \n \
            ###```````##```##````````##```##```````````##```##```````##`##```````##````##`````````##```##```##``````##```##`````##` \n \
            `##``````###````##``````###``##`````````````##``##````````####```````##```##``````````##``###````##`````##````##`````## \n \
            ``#########``````########```##``````````````###`##``````````##```````##``##````````````##`##``````##````##`````###``### \n \
            ````````#####`````````````````````````````````````````````````````````````````````````````````````````````````````##``  \n \
            ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
            ``````````````````````````Copyright``yutiansut``2018``````QUANTITATIVE FINANCIAL FRAMEWORK````````````````````````````` \n \
            ``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
            ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n \
            ```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````` \n '


__str__ = __repr__
# QA_util_log_info(Logo)
