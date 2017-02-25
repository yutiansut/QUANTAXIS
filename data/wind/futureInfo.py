# -*- coding:utf-8 -*-
from WindPy import *

from datetime import datetime
import pymongo

client =pymongo.MongoClient('localhost', 27017)  
db = client.wind
coll = db.futureList
w.start()
# for item in coll.find().sort("Code",pymongo.DESCENDING):
for item in coll.find():
    print item["Code"]
    codes=item["Code"]
    data=w.wsd(item["Code"], "lasttrade_date,lastdelivery_date,dlmonth,lprice,sccode,margin,changelt,punit,mfprice,contractmultiplier,cdmonths,thours,ltdated,ftmargins,trade_hiscode", "2017-01-25", "2017-01-26", "Fill=Previous")
    
    if (data.ErrorCode==0):

        lasttrade_date=data.Data[0][0]
        lastdelivery_date=data.Data[1][0]
        dlmonth=data.Data[2][0]
        lprice=data.Data[3][0]
        sccode=data.Data[4][0]
        margin=data.Data[5][0]
        changelt=data.Data[6][0]
        punit=data.Data[7][0]
        mfprice=data.Data[8][0]
        contractmultiplier=data.Data[9][0]
        cdmonths=data.Data[10][0]
        thours=data.Data[11][0]
        ltdated=data.Data[12][0]
        ftmargins=data.Data[13][0]
        trade_hiscode=data.Data[14][0]
        coll.update({"Code":codes} , { "$set" : {"lasttrade_date": lasttrade_date}});
        coll.update({"Code":codes} , { "$set" : {"lastdelivery_date":lastdelivery_date}});
        coll.update({"Code":codes} , { "$set" : {"dlmonth":dlmonth}});
        coll.update({"Code":codes} , { "$set" : {"lprice":lprice}});
        coll.update({"Code":codes} , { "$set" : {"sccode":sccode}});
        coll.update({"Code":codes} , { "$set" : {"margin":margin}});
        coll.update({"Code":codes} , { "$set": {"changelt":changelt}});
        coll.update({"Code":codes} , { "$set" : {"punit":punit}}); 
        coll.update({"Code":codes} , { "$set" : {"mfprice":mfprice}}); 
        coll.update({"Code":codes} , { "$set" : {"contractmultiplier":contractmultiplier}}); 
        coll.update({"Code":codes} , { "$set" : {"cdmonths":cdmonths}}); 
        coll.update({"Code":codes} , { "$set" : {"thours":thours}}); 
        coll.update({"Code":codes} , { "$set" : {"ltdated":ltdated}}); 
        coll.update({"Code":codes} , { "$set" : {"ftmargins":ftmargins}}); 
        coll.update({"Code":codes} , { "$set" : {"trade_hiscode":trade_hiscode}}); 
    else:
        print 'nodata'

