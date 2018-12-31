QUANTAXIS quantitative financial strategy framework
==========================

QUANTAXIS quantitative framework to achieve the stock and futures market, the whole species back to the test.Through the distributed crawler for data capture, to build a response to the data cleaning and market push engine to build a multi-language open response frame. And build interactive visualization of clients and websites.

.. image:: https://badge.waffle.io/yutiansut/QUANTAXIS.svg?label=ready&title=Ready 
 :target: https://waffle.io/yutiansut/QUANTAXIS 
 :alt: 'Stories in Ready'
 
 
.. image:: https://img.shields.io/pypi/dw/quantaxis.svg
   :target: https://pypi.python.org/quantaxis/
   :alt: PyPI Downloads

 
0.4.x Release Note
---------------------------------

QUANTAXIS Quantitative Financial Strategy Framework is a quantitative analysis solution for small and medium-sized strategy teams.We can quickly implement scene-oriented customization solutions with highly decoupled modularity and standardized protocols. QUANTAXIS is a progressive open Framework, you can according to their own needs, the introduction of their own data, analysis programs, visualization process, you can also RESTful interface, the rapid realization of multi-LAN / WAN collaboration.

QUANTAXIS and many excellent domestic quantitative platform is the difference, QA more concerned about the user experience and the actual situation, for the user needs will be more optimized, so will pay more attention to openness, the introduction of custom convenience, and the team Collaborative details are handled, such as custom data introductions, custom policy chart comparison, custom risk and policy portfolio management, and so on.

*  Welcome group discussion: [group link] (https://jq.qq.com/?_wv=1027&k=4CEKGzn)

* For more information, see https://github.com/yutiansut/QUANTAXIS/blob/0.4-beta/update_log.md

* If you have any questions, you can send [issue] (https://github.com/yutiansut/QUANTAXIS/issues) on github, or contact us at QQ 279336410, QQ group 563280067
=============

More info on https://github.com/yutiansut/quantaxis


An EXAMPLE of QUANTAXIS BACKTEST like that below:

.. code:: python

    
    import QUANTAXIS as QA
    from QUANTAXIS import QA_Backtest_stock_day as QB


    """
    Written Before:
    ===============QUANTAXIS BACKTEST STOCK_DAY's Constant
    Constant:
    QB.account.message  
    QB.account.cash  
    QB.account.hold  
    QB.account.history  
    QB.account.assets 
    QB.account.detail 
    QB.account.init_assest 



    QB.strategy_stock_list 
    QB.strategy_start_date 
    QB.strategy_end_date  


    QB.today  

    QB.benchmark_code  




    Function:
    get the market data (based on gap):
    QB.QA_backtest_get_market_data(QB,code,QB.today)
    get the market data as you want:
    QA.QA_fetch_stock_day(code,start,end,model)


    Order :
    QB.QA_backtest_send_order(QB, code,amount,towards,order: dict)

    order has three model:
    1.Limited order order['order_model']=0 or l,L
    attention: this model should have a order['price'] key
    order['price']=xxxx

    2.Market order order['order_model']=1 or m,M,market,Market
    3.Strict model order['order_model']=2 or s,S
        which is buy in the highest price or sell in the lowest price

    Query the hold amount

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
                QB.QA_backtest_send_order(QB,item,10000,1,{'order_model':'Market'})

        
            else:
                #print(QB.QA_backtest_hold_amount(QB,item))
                QB.QA_backtest_send_order(QB,item,10000,-1,{'order_model':'Market'})
        
    @QB.end_backtest
    def after_backtest():
        pass
