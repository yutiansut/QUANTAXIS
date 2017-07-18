# coding:utf-8

import pymongo
import QUANTAXIS as QA
import json,datetime,time

# setting config
unit_strategy=input('strategy_name:   ')
unit_cookie=''
unit_code=input('code name:  ')

# client setting
client=pymongo.MongoClient()
db=client.quantaxis
coll_info=db.backtest_info
coll_history=db.backtest_history

# get cookie and history
info=coll_info.find_one({'stock_list':unit_code,'strategy':unit_strategy})
cookie=info['account_cookie']
days=info['exist']
trade=coll_history.find({'cookie':cookie})[coll_history.find({'cookie':cookie}).count()-1]
# reappeared the performance
message={
    'header':{
        'source':'account',
        'cookie':trade['cookie'],
        'session':{
            'user':trade['user'],
            'strategy':trade['strategy'],
            'code':trade['bid']['code']
        }
        
        },
    'body':{
        'account':{
            'init_assest':trade['init_assest'],
            'portfolio':trade['portfolio'],
            'history':trade['history'],
            'assest_now':trade['assest_now'],
            'assest_history':trade['assest_history'],
            'assest_free':trade['assest_free'],
            #'total_assest_free':trade['total_assest_free'],
            'assest_fix':trade['assest_fix'],
            'profit':trade['profit'],
            'account_date':trade['account_date'],
            'total_profit':trade['total_profit'],
            'total_date':trade['total_date'],
            'cur_profit_present':trade['cur_profit_present'],
            'cur_profit_present_total':trade['cur_profit_present_total'],
            'hold':trade['hold']
        },
        'bid':trade['bid'],
        'market':trade['market'],
        'time':trade['time'],
        'date_stamp':trade['time_stamp']
    }
}
print(QA.QA_backtest_analysis_start(client,message,days))

