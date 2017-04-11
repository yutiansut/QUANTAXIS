#Encoding:utf-8
from QUANTAXIS.QAUtil import QA_util_log_info,QA_Setting
from .QABacktest import QA_backtest_get_client,QA_Backtest
"""
标准化输出结果,并且给QAAnalysis喂食QAQ

首先接受QASignal打包出来的标准协议
"""
def QA_backtest_standard_record_market(message):
    client=QA_backtest_get_client(QA_Backtest)
    coll=client.quantaxis.market_history
    coll.insert({})  
def QA_backtest_standard_record_account(message):
    return message

