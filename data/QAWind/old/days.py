# -*- coding:utf-8 -*-
from WindPy import *

from datetime import datetime
import pymongo


client =pymongo.MongoClient('localhost', 27017)  
db = client.wind
coll = db.days
w.start()

days=w.tdays("2000-01-01", "2017-02-22", "")
tradeday=days.Data[0]
for item in tradeday:
    items=item.strftime('%Y-%m-%d')
    coll.insert({"date":items})