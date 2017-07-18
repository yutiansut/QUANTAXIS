# coding :utf-8

from QUANTAXIS.QAUtil import QA_util_sql_mongo_setting,QA_util_log_info
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QASignal import QA_signal_send
from .QABid import QA_QAMarket_bid
#from .market_config import stock_market,future_market,HK_stock_market,US_stock_market
import datetime

class QA_Market():
    #基础设置
    def init(self):
        self.type='2x'
        self.tick='day'
        self.slipper='0.0005'

    #client=QA_Setting.client
    # client=QA.QA_util_sql_mongo_setting()
    # db= client.market
    def market_make_deal(self, bid, client):
        if self.type=='2x' and self.tick=='day':
            coll=client.quantaxis.stock_day
        elif self.type=='3x' and self.tick=='500ms':
            coll=client.quantaxis.future_ms
        try:
            item= coll.find_one({"code":str(bid['code'])[0:6], "date": str(bid['time'])[0:10]})
            QA_util_log_info('==== Market Board ====')
            QA_util_log_info('date'+str(bid['time']))
            QA_util_log_info('day High'+str(item["high"]))
            QA_util_log_info('your bid price'+str(bid['price']))
            QA_util_log_info('day Low'+str(item["low"]))
            QA_util_log_info('amount'+str(bid["amount"]))
            QA_util_log_info('towards'+str(bid["towards"]))
            QA_util_log_info('==== Market Board ====')
            if (float(bid['price']) < float(item["high"]) and  float(bid['price']) > float(item["low"]) or float(bid['price']) == float(item["low"]) or float(bid['price']) == float(item['high'])) and float(bid['amount'])<float(item['volume'])/8:
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
                            'amount':int(bid['amount']),
                            'time':str(bid['time']),
                            'towards':bid['towards']
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

                #QA_signal_send(message,client)
            # print(message['body']['bid']['amount'])
                return message
            else:
                QA_util_log_info('not success')
                if int(bid['price'])==0:
                    status_mes=401
                else: status_mes=402

                message = {
                    'header':{
                        'source':'market',
                        'status':status_mes,
                        'session':{
                            'user':str(bid['user']),
                            'strategy':str(bid['strategy'])
                            }
                        },
                    'body':{
                        'bid':{
                            'price':str(bid['price']),
                            'code':str(bid['code']),
                            'amount':int(bid['amount']),
                            'time':str(bid['time']),
                            'towards':bid['towards']
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
            # print(message['body']['bid']['amount'])
                return message
        except:
            QA_util_log_info('no market data')
            message = {
                    'header':{
                        'source':'market',
                        'status':500,
                        'session':{
                            'user':str(bid['user']),
                            'strategy':str(bid['strategy'])
                            }
                        },
                    'body':{
                        'bid':{
                            'price':str(bid['price']),
                            'code':str(bid['code']),
                            'amount':int(bid['amount']),
                            'time':str(bid['time']),
                            'towards':bid['towards']
                            },
                        'market':{
                            'open':0,
                            'high':0,
                            'low':0,
                            'close':0,
                            'volume':0,
                            'code':0
                            }
                        }
                    }
            return message
