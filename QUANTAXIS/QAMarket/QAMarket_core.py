# coding :utf-8

from QUANTAXIS.QAUtil import QA_util_sql_mongo_setting,QA_util_log_info
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QASignal import QA_signal_send
from .QABid import QA_QAMarket_bid
import datetime

class QA_Market():

    #client=QA_Setting.client
    # client=QA.QA_util_sql_mongo_setting()
    # db= client.market
    def market_make_deal(self, bid, client):
        coll=client.quantaxis.stock_day
        item= coll.find_one({"code":str(bid['code'])[0:6], "date": str(bid['time'])[0:10]})
        QA_util_log_info('==== Market Board ====')
        QA_util_log_info('day High'+str(item["high"]))
        QA_util_log_info('your bid price'+str(bid['price']))
        QA_util_log_info('day Low'+str(item["low"]))
        QA_util_log_info('==== Market Board ====')
        if float(bid['price']) < float(item["high"]) and  float(bid['price']) > float(item["low"]) or float(bid['price']) == float(item["low"]) or float(bid['price']) == float(item['high']):
            QA_util_log_info("deal success")
            message = {
                'header':{
                    'source':'market',
                    'status':200,
                    'session':{
                        'user':str(bid['user']),
                        'strategy':str(bid['strategy'])
                        }
                },
                'body':{
                    'bid':{
                        'price':str(bid['price']),
                        'code':str(bid['code']),
                        'amount':str(bid['amount']),
                        'time':str(bid['time']),
                        'towards':str(bid['towards'])
                        },
                    'market':{
                        'open':item['open'],
                        'high':item['high'],
                        'low':item['low'],
                        'close':item['close'],
                        'volume':item['volume'],
                        'code':item['code']
                        }
                    }
                }

            QA_signal_send(message,client)
            return True
        else:
            QA_util_log_info('not success')
            return False
