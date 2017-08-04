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