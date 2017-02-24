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
        print data.Data[0][0]

        coll.update({"Code":codes} , { "$push" : {"lasttrade_date": data.Data[0][0]}});
        coll.update({"Code":codes} , { "$push" : {"lastdelivery_date":data.Data[1][0]}});
        coll.update({"Code":codes} , { "$push" : {"dlmonth":data.Data[2][0]}});
        coll.update({"Code":codes} , { "$push" : {"lprice":data.Data[3][0]}});
        coll.update({"Code":codes} , { "$push" : {"sccode":data.Data[4][0]}});
        coll.update({"Code":codes} , { "$push": {"changelt":data.Data[6][0]}});
        coll.update({"Code":codes} , { "$push" : {"punit":data.Data[7][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"mfprice":data.Data[8][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"contractmultiplier":data.Data[9][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"cdmonths":data.Data[10][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"thours":data.Data[11][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"ltdated":data.Data[12][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"ftmargins":data.Data[13][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"trade_hiscode":data.Data[14][0]}}); 
    else:
        print 'nodata'

