import pymongo
import datetime
from QUANTAXIS import QA_util_date_stamp
coll=pymongo.MongoClient().quantaxis.stock_day
print(datetime.datetime.now())
startDate='2016-04-01'
endDate='2016-06-01'
for item in coll.find({'code':str(600010)[0:6],"date_stamp":{"$lte":QA_util_date_stamp(endDate),"$gte":QA_util_date_stamp(startDate)}}):
    print (item['code'])
    print(datetime.datetime.now())
print(datetime.datetime.now())