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
===============QUANTAXIS BACKTEST STOCK_DAY中的变量
常量:
QB.account.message  当前账户消息
QB.account.cash  当前可用资金
QB.account.hold  当前账户持仓
QB.account.history  当前账户的历史交易记录
QB.account.assets 当前账户总资产
QB.account.detail 当前账户的交易对账单
QB.account.init_assest 账户的最初资金



QB.strategy_stock_list 回测初始化的时候  输入的一个回测标的
QB.strategy_start_date 回测的开始时间
QB.strategy_end_date  回测的结束时间


QB.today  在策略里面代表策略执行时的日期

QB.benchmark_code  策略业绩评价的对照行情




函数:
获取市场(基于gap)行情:
QB.QA_backtest_get_market_data(QB,code,QB.today)
获取市场自定义时间段行情:
QA.QA_fetch_stock_day(code,start,end,model)


报单:
QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)

order有三种方式:
1.限价成交 order['bid_model']=0或者l,L
  注意: 限价成交需要给出价格:
  order['price']=xxxx

2.市价成交 order['bid_model']=1或者m,M,market,Market
3.严格成交模式 order['bid_model']=2或者s,S
    及 买入按bar的最高价成交 卖出按bar的最低价成交

查询当前一只股票的持仓量
QB.QA_backtest_hold_amount(QB,code)


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

@QB.before_backtest
def before_backtest():
    global risk_position
    QA.QA_util_log_info(QB.account.message)
    
    
    
@QB.load_strategy
def strategy():
    #print(QB.account.message)
    #print(QB.account.cash)
    
    for item in QB.strategy_stock_list:
        if QB.QA_backtest_hold_amount(QB,item)==0:
        #获取数据的第一种办法[这个是根据回测时制定的股票列表初始化的数据]
            QB.QA_backtest_send_order(QB,item,10000,1,{'bid_model':'Market'})

    
        else:
            #print(QB.QA_backtest_hold_amount(QB,item))
            QB.QA_backtest_send_order(QB,item,10000,-1,{'bid_model':'Market'})
    
@QB.end_backtest
def after_backtest():
    pass