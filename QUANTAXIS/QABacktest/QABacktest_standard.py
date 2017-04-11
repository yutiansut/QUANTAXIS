#Encoding:utf-8
from QUANTAXIS.QAUtil import QA_util_log_info,QA_Setting
import datetime,time
"""
标准化输出结果,并且给QAAnalysis喂食QAQ

首先接受QASignal打包出来的标准协议
"""
def QA_backtest_standard_record_market(message,client):
    #client=QA_backtest_get_client(QA_Backtest)
    coll=client.quantaxis.market_history
    """
    bid':{
        'price':str(bid['price']),
        'code':str(bid['code']),
        'amount':str(bid['amount']),
        'time':str(bid['time']),
        'towards':str(bid['towards'])
        },
    market:{
        'open':item['open'],
        'high':item['high'],
        'low':item['low'],
        'close':item['close'],
        'amount':item['amount'],
        'code':item['code']}
    """
    coll.insert({
        'user':message['header']['session']['user'],
        'strategy_name':message['header']['session']['strategy'],
        'time':datetime.datetime.now(),
        'date_stamp':str(datetime.datetime.now().timestamp()),
        'bid':message['body']['bid'],
        'market':message['body']['market']
        })  
def QA_backtest_standard_record_account(message):
    return message

