import QUANTAXIS as QA
from QUANTAXIS import QA_Backtest_stock_day

QB=QA_Backtest_stock_day()
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
    print(QB.market_data)
    
@QB.end_backtest
def after_backtest():
    print(dir(QB))