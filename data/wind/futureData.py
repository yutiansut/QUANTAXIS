# -*- coding:utf-8 -*-
from WindPy import *

from datetime import datetime
import pymongo
import re

client =pymongo.MongoClient('localhost', 27017)  
db = client.wind
coll = db.futureList
w.start()

for item in coll.find({"Code":re.compile('IC.CFE')}):
    print item["Code"]
    target=item["Code"]
    result=w.wsd(target,"lasttrade_date,lastdelivery_date,thours", "2000-01-01", "2017-02-25", "Fill=Previous")
    coll2 = db.futureData
    
    for items in result[0]
    coll2.insert({"code":target,"lasttrade_date"})
    