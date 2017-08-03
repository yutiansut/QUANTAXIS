import QUANTAXIS as QA
from QUANTAXIS import QA_Backtest_stock_day as QB


@QB.backtest_init
def init():
        #
    QB.setting.QA_util_sql_mongo_ip='192.168.4.189'
    QB.account.init_assest=250000
    QB.strategy_start_date='2017-03-01'
    QB.backtest_bid_model='market_price'
    

@QB.before_backtest
def before_backtest():
    global risk_position
    QA.QA_util_log_info(QB.account.message)
    
    
    
@QB.load_strategy
def strategy():
    print(QB.account)
    print(QB.market_data)
    
@QB.end_backtest
def after_backtest():
    print(dir(QB))