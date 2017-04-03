# coding :utf-8

import pymongo
import datetime

class market():

    def __init__(self):
        self.bid_price=0
        self.bid_time=datetime.datetime.now()
        self.bid_amount=0
        self.bid_towards=0
        self.bid_variety=str()
        self.client=pymongo.MongoClient("127.0.0.1",27017)
        self.db=self.client.market
        
    def market_make_deal(self):
        
        self.coll=self.db.stock
        
        item=self.coll.find_one({"variety_name":self.bid_variety,"datetime":self.bid_time})
        print(item["high"])
        print(item["low"])
        if (self.bid_price<item["high"] and self.bid_price>item["low"]):
            print ("deal success")
            return True