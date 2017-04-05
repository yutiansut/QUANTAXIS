# coding :utf-8

from QUANTAXIS.QAUtil import QA_util_sql_mongo_setting,QA_util_log_info
from QUANTAXIS.QAUtil import QA_Setting
import datetime

class market():

    def __init__(self):
        self.bid_price=0
        self.bid_time=datetime.datetime.now()
        self.bid_amount=0
        self.bid_towards=0
        self.bid_code=str()

        self.client=QA_Setting.client
        #self.client=QA.QA_util_sql_mongo_setting()
        #self.db=self.client.market
        
    def market_make_deal(self):
        
        
        self.db=self.client.quantaxis
        self.coll=self.db.stock_day
        item=self.coll.find_one({"code":self.bid_code,"datetime":self.bid_time})
        print(item["high"])
        print(item["low"])
        if (self.bid_price<item["high"] and self.bid_price>item["low"]):
            print ("deal success")
            return True