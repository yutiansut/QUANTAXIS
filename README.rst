QUANTAXIS quantitative financial strategy framework
==========================

QUANTAXIS quantitative framework to achieve the stock and futures market, the whole species back to the test.Through the distributed crawler for data capture, to build a response to the data cleaning and market push engine to build a multi-language open response frame. And build interactive visualization of clients and websites.


0.4.0-beta Release Note
---------------------------------

QUANTAXIS Quantitative Financial Strategy Framework is a quantitative analysis solution for small and medium-sized strategy teams.We can quickly implement scene-oriented customization solutions with highly decoupled modularity and standardized protocols. QUANTAXIS is a progressive open Framework, you can according to their own needs, the introduction of their own data, analysis programs, visualization process, you can also RESTful interface, the rapid realization of multi-LAN / WAN collaboration.

QUANTAXIS and many excellent domestic quantitative platform is the difference, QA more concerned about the user experience and the actual situation, for the user needs will be more optimized, so will pay more attention to openness, the introduction of custom convenience, and the team Collaborative details are handled, such as custom data introductions, custom policy chart comparison, custom risk and policy portfolio management, and so on.

**  Welcome group discussion: [group link] (https://jq.qq.com/?_wv=1027&k=4CEKGzn)

** For more information, see https://github.com/yutiansut/QUANTAXIS/blob/0.4-beta/update_log.md

** If you have any questions, you can send [issue] (https://github.com/yutiansut/QUANTAXIS/issues) on github, or contact us at QQ 279336410, QQ group 563280067
=============

More info on https://github.com/yutiansut/quantaxis


An EXAMPLE of QUANTAXIS BACKTEST like that below:

.. code-block:: python

    
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