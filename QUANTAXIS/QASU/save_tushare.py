#coding:utf-8 

from QUANTAXIS.QAFetch import QATushare
import tushare as ts
from QUANTAXIS.QAUtil import QA_util_date_stamp,QA_util_time_stamp
from QUANTAXIS.QAUtil import QA_Setting
import datetime,json
import re
import time
import pymongo


def QA_save_stock_day_all():
    df= ts.get_stock_basics()
    for i in df.index:  
        print('Now Saving %s' %(i) )    
        try:
            data=ts.get_hist_data(str(i))
            
            data_json=json.loads(data.to_json(orient='records'))
            
            
            for i in range(0,len(data_json),1):
                data_json[i]['date_stamp']=QA_util_date_stamp(list(data.index)[i])
                data_json[i]['date']=list(data.index)[i]
           
            
            coll=pymongo.MongoClient().quantaxis.stock_day
            coll.insert_many(data_json)
        except:
            print('error in saving'+str(i))

def QA_SU_save_stock_list(client):
    data=QATushare.QA_fetch_get_stock_list()
    date=str(datetime.date.today())
    date_stamp=QA_util_date_stamp(date)
    coll=client.quantaxis.stock_list
    coll.insert({'date':date,'date_stamp':date_stamp,'stock':{'code':data}})
def QA_SU_save_trade_date_all():
    data=QATushare.QA_fetch_get_trade_date('','')
    coll=pymongo.MongoClient().quantaxis.trade_date
    coll.insert_many(data)

def QA_SU_save_stock_info(client):
    data=QATushare.QA_fetch_get_stock_info('all')
    coll=client.quantaxis.stock_info
    coll.insert_many(data)
