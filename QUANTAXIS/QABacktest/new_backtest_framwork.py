#coding:utf-8



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




def strategy(func,*a,**b):
    def before_day(): 
        print('before of day in strategy')
    def end_day():
        print('end of day in strategy')
    def deoc(*a,**b):
        before_day()
        func(*a,**b)
        end_day()
    return deoc

def backtest(func,*a,**b):
    def before_backtest():
        print('before backtest')

    def end_backtest():
        print('end_backtest')

    def inside_backtest(*a,**b):
        before_backtest()
        func(*a,**b)
        end_backtest()
    return inside_backtest

@backtest
@strategy
def exec_bid():
    print('exec bid market and account')


"""
before backtest
before of day in strategy
exec bid market and account
end of day in strategy
end_backtest
"""

if __name__=='__main__':
    exec_bid()

    