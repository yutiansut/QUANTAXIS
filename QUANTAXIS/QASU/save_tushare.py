# coding :utf-8 

from QUANTAXIS.QAFetch import QATushare
import tushare as ts
from QUANTAXIS.QAUtil import QA_util_date_stamp,QA_util_time_stamp
from QUANTAXIS.QAUtil import QA_Setting
import datetime,json
import re
import time
import pymongo

def QA_save_stock_day_all():
    dfs = ts.get_stock_basics()

    df=ts.get_stock_basics()
    for i in df.index:  
        print(i)
        date = dfs.ix[i]['timeToMarket']
        if int(str(date)[0:2])==19:
            print(date)
            date=20000101
        dates=str(date)[0:4]+'-'+str(date)[4:6]+'-'+str(date)[6:8]
        print(dates)
        data=ts.get_k_data(i,start=dates)
        data_json=json.loads(data.to_json(orient='records'))
        coll=pymongo.MongoClient().quantaxis.stock_day
        coll.insert_many(data_json)
