QUANTAXIS quantitative financial strategy framework
==========================

QUANTAXIS quantitative framework to achieve the stock and futures market, the whole species back to the test.Through the distributed crawler for data capture, to build a response to the data cleaning and market push engine to build a multi-language open response frame. And build interactive visualization of clients and websites.


0.4.0-beta Release Note
---------------------------------


Taking into account such a scenario, an organization's strategy team is generally composed of CS + Finance, Finance students are very good at data analysis, strategy, but not very understanding of the underlying structure of the code, code style and standards are different While CS students are well aware of the code and framework, they are struggling with the financial theory of boring holes, and the current domestic support for quantitative services can not solve this common scene pain points, or for financial students Easy to operate the analysis system, but for IT in terms of the lack of customizable part; either for the underlying IT data and transaction interface, and for financial students want to package out from the underlying interface, a set of available efficient framework It is difficult to ascend to heaven.

QUNATAXIS is committed to solving this problem, and we solve this problem by creating a standard framework within a RESTful-based LAN that is separated from front and back, and we hope that our framework is highly scalable and easy to access The company's individual strategy team's individual needs (this is the most critical, basically every company will have its own data, their own trading interface, their own specific functional goals), so we want to build a standardized, high Scalable, easy to deploy scaffolding, rather than a complete hard to customize solution.

QUANTAXIS front and back completely separated, highly split, each component relies on RESTful standard URI to communicate, which also gives us an open framework of infinite possibilities, can achieve Matlab, r, python, javascript, C, C + +, rust And other users of the harmonious coexistence, rather than increase the cost of learning to learn a common language.At the same time, as long as a public network IP and server, you can also go beyond the LAN restrictions, to achieve the needs of remote teams.


=============

More info on https://github.com/yutiansut/quantaxis


.. code-block:: python
   :linenos:
   
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
    QB.setting.QA_util_sql_mongo_ip='127.0.0.1'

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
    #input()
    
    for item in QB.strategy_stock_list:
        QA.QA_util_log_info(QB.QA_backtest_get_market_data(QB,item,QB.today))
        if QB.QA_backtest_hold_amount(QB,item)==0:
            QB.QA_backtest_send_order(QB,item,10000,1,{'bid_model':'Market'})

    
        else:
            #print(QB.QA_backtest_hold_amount(QB,item))
            QB.QA_backtest_send_order(QB,item,10000,-1,{'bid_model':'Market'})
    
@QB.end_backtest
def after_backtest():
    pass