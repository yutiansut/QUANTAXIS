# -*- coding:utf-8 -*-
from WindPy import *

from datetime import datetime
import pymongo

client =pymongo.MongoClient('localhost', 27017)  
db = client.wind
coll = db.futureList
w.start()
for item in coll.find():
    print item["Code"]
    codes=item["Code"]
    data=w.wsd(item["Code"], "lasttrade_date,lastdelivery_date,dlmonth,lprice,sccode,margin,changelt,punit,mfprice,contractmultiplier,cdmonths,thours,ltdated,ftmargins,trade_hiscode", "2017-01-25", "2017-01-26", "Fill=Previous")
    
    if (data.ErrorCode==0):
        print data.Data[0][0][0]

    else:
        print 'nodata'

