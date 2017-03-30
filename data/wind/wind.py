#coding:utf-8

import time
import datetime,re
import pymongo
from WindPy import w
w.start()


#Stock
def getStockInfo(startDate,endDate,name,ifsave):
    #get the all stock list on the endDate
    # judge the vaild date
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        #tempStr='date='+endDate+";sectorid=a001010100000000"
        #data=w.wset("sectorconstituent",tempStr)
        data=w.wsd(name, "sec_name,sec_englishname,ipo_date,exch_city,mkt,sec_status,delist_date,issuecurrencycode,curr,RO,parvalue,lotsize,tunit,exch_eng,country,concept,marginornot,SHSC,parallelcode,sec_type,backdoor,backdoordate,windtype,compindex2", startDate, endDate, "index=1")
        #print(data)
        if (data.ErrorCode!=0):
            print ("Connent to Wind successfully")
    return data.Data
# 期货

def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False

a=getStockInfo("2000-01-01","2017-03-29","000001.SZ","n")
print (a)