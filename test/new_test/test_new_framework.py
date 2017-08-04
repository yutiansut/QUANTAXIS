# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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


import QUANTAXIS as QA
from QUANTAXIS import QA_Backtest_stock_day as QB


"""
写在前面:




"""







@QB.backtest_init
def init():
    #
    QB.setting.QA_util_sql_mongo_ip='192.168.4.189'

    QB.account.init_assest=2500000
    QB.benchmark_code='hs300'

    QB.strategy_stock_list=['000001','000002','600010','601801','603111']
    QB.strategy_start_date='2017-03-01'
    QB.strategy_end_date='2017-07-01'
    QB.backtest_bid_model='market_price'
    

@QB.before_backtest
def before_backtest():
    global risk_position
    QA.QA_util_log_info(QB.account.message)
    
    
    
@QB.load_strategy
def strategy():
    print(QB.account.message)

    #获取数据的第一种办法[这个是根据回测时制定的股票列表初始化的数据]
    print(QB.QA_backtest_get_data_from_market(QB,'000001',QB.today))
    #获取数据的第二种办法[这个是直接从数据库里面拉数据]
    print(QA.QA_fetch_stock_day('000001','2017-03-05','2017-03-08'))
    
@QB.end_backtest
def after_backtest():
    print(dir(QB))