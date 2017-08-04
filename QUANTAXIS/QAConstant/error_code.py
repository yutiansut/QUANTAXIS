#coding:utf-8

class QUANTAXIS_Error():
    QUANTAXIS_Error_framework_error          = 0100



# QUANTAXIS 框架错误代码 0000-0999
QUANTAXIS_error={}
# 数据获取/数据库读取错误代码 1000-1999
QA_fetch_error={}
# 数据错误代码 保存部分 2000-2499
QA_save_error={}

# 数据错误代码  更新部分 2500-2599
QA_update_error={}
# 交易错误代码(模拟market返回) 3000-3999
QA_market_error={}

# 回测错误代码 4000-4999
QA_backtest_error={
    # 通用错误代码 
    'total':{

    },
    # 特定错误代码
    'QA_backtest_stock_day':{

    },
    'QA_backtest_stock_min':{},
    'QA_backtest_stock_tick':{},
    'QA_backtest_future_day':{},
    'QA_backtest_future_min':{},
    'QA_backtest_future_tick':{}

}


