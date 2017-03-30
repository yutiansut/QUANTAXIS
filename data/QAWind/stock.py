#coding:utf-8

import time
import datetime,re
import pymongo
from WindPy import w
w.start()


#Stock
def getStockInfo(startDate,endDate,name):
    #get the all stock list on the endDate
    # judge the vaild date
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        #tempStr='date='+endDate+";sectorid=a001010100000000"
        #data=w.wset("sectorconstituent",tempStr)
        data=w.wsd(name, "sec_name,sec_englishname,ipo_date,exch_city,mkt,sec_status,delist_date,issuecurrencycode,curr,RO,parvalue,lotsize,tunit,exch_eng,country,concept,marginornot,SHSC,parallelcode,sec_type,backdoor,backdoordate,windtype", startDate, endDate)
        #print(data)
        if (data.ErrorCode!=0):
            print ("Connent to Wind successfully")
    return data.Data
def getStockData_day(startDate,endDate,name):
    if(is_valid_date(endDate)==False):
        print ("wrong date")
    else :
        data=w.wsd(name,"sec_name,pre_close,open,high,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,lastradeday_s,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,trade_status,susp_days,susp_reason,maxupordown,open3,high3,low3,close3",startDate,endDate, "Fill=Previous;PriceAdj=F")
        print(data)
        if (data.ErrorCode==0):
            print ("Connent to Wind successfully")
    return data.Data
# 期货

def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False
        
def test():
    #a=getStockInfo("2000-01-01","2017-03-29","000001.SZ")
    a=getStockData_day("2000-01-01","2015-03-29","000001.SZ")
    print (a)
test()
