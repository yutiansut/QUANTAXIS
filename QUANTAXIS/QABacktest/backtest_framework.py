# coding:utf-8


import csv
import datetime
import json
import os
import random
import re
import sys
import time

import apscheduler
import numpy as np
import pandas as pd
import pymongo
from QUANTAXIS import *
from QUANTAXIS import (QA_Market, QA_Portfolio, QA_QAMarket_bid, QA_Risk,
                       __version__)
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QABacktest.QAAnalysis import QA_backtest_analysis_start
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_index_day, QA_fetch_stock_day,
                                       QA_fetch_stock_info,
                                       QA_fetch_stocklist_day,
                                       QA_fetch_trade_date)
from QUANTAXIS.QASU.save_backtest import (QA_SU_save_account_message,
                                          QA_SU_save_account_to_csv)
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_get_real_date,
                              QA_util_log_info)

from QUANTAXIS.QATask import QA_Queue
from tabulate import tabulate

import configparser
import queue


try:
    sys.path.append(os.getcwd())
    #QA_util_log_info('loading strategy from'+ os.getcwd())
    import user_strategy
    from user_strategy import before_backtest, before_trading, handle_bar, end_trading, end_backtest
except:
    QA_util_log_info(Exception)


def strategy_dec(func, *a, **b):

    def deoc(*a, **b):

        before_trading()

        handle_bar()
        func(*a, **b)

        end_trading()
    return deoc


def backtest_dec(func, *a, **b):

    def inside_backtest(*a, **b):
        before_backtest()
        func(*a, **b)
        end_backtest()
    return inside_backtest


class backtest():

    @backtest_dec
    @strategy_dec
    def exec_bid(self):
        QA_util_log_info(
            'from backtest_framework: exec bid market and account')


if __name__ == '__main__':
    backtest().exec_bid()
