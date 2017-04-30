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
        'volume':item['volume'],
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
    
    
def QA_backtest_standard_record_account(message,client):
    coll=client.quantaxis.market_history
    coll.insert({
        'user':message['header']['session']['user'],
        'strategy_name':message['header']['session']['strategy'],
        'time':datetime.datetime.now(),
        'date_stamp':str(datetime.datetime.now().timestamp()),
        'bid_date':message['body']['bid']['time'],
        'bid':message['body']['bid'],
        'market':message['body']['market'],
        'account':message['body']['account'],
        'cookie':message['header']['coookie']
        })
    


"""
               'header':{
                    'source':'account',
                    'cookie':self.account_cookie,
                    'session':{
                        'user':update_message['user'],
                        'strategy':update_message['strategy']
                    }
                    
                    },
                'body':{
                    'account':{
                        'init_assest':self.assets,
                        'portfolio':self.portfolio,
                        'history':self.history_trade,
                        'assest_now':self.assets,
                        'assest_history':self.total_assest,
                        'assest_free':self.assets_free,
                        'assest_fix':self.assets_market_hold_value,
                        'profit':self.portfit,
                        'cur_profit':self.cur_profit
                    },
                    'bid':update_message['bid'],
                    'market':update_message['market'],
                    'time':datetime.datetime.now(),
                    'date_stamp':str(datetime.datetime.now().timestamp())
"""