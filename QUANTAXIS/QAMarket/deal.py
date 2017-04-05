# coding :utf-8

from QUANTAXIS.QAUtil import QA_util_sql_mongo_setting,QA_util_log_info
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QASignal import QA_signal_send
import datetime



class bid():
    def __init__(self):
        self.price=5
        self.time=datetime.datetime.now()
        self.amount=10
        self.towards=1
        self.code=str('000001.SZ')
    def renew_bid(self):
        pass
class market():
    def __init__(self):
        self.bid=bid()
        self.client=QA_Setting.client
    #self.client=QA.QA_util_sql_mongo_setting()
    #self.db=self.client.market
        
    def market_make_deal(self):
        
        
        self.db=self.client.quantaxis
        self.coll=self.db.stock_day
        item=self.coll.find_one({"code":self.bid.code,"datetime":self.bid.time})
        print(item["high"])
        print(item["low"])
        if (self.bid.price<item["high"] and self.bid.price>item["low"]):
            QA_util_log_info("deal success")
            QA_signal_message={'trade_status':'success','price':str(self.bid.price),
            'code':str(self.bid.code),'amount':str(self.bid.amount),'time':str(self.bid.time),
            'towards':str(self.bid.towards)}
            QA_signal_send('market','strategy',True,QA_signal_message)
            return True
        else:
            QA_util_log_info('not success')
            return False
