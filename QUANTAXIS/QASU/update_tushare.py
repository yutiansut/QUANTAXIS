# coding:utf-8 

from QUANTAXIS.QAFetch import QATushare
from QUANTAXIS.QAUtil import QA_util_date_stamp,QA_Setting,QA_util_date_valid
import json
import pymongo
import datetime
import re
import time

def QA_update_stock_day(name,startDate,endDate):
    data=QATushare.QA_fetch_get_stock_day(name,startDate,endDate)
    
    
def QA_update_stock_day_all(code,client):
    coll_stocklist=client.quantaxis.stock_list
    stock_list=coll_stocklist.find_one()['stock']['code']
    coll_stock_day=client.quantaxis.stock_day

    for item in stock_list:
        #coll.find({'code':str(item)[0:6]}).count()
        #先拿到最后一个记录的交易日期
        start_date=coll_stock_day.find({'code':str(item)[0:6]})[coll_stock_day.find({'code':str(item)[0:6]}).count()-1]['date']
        end_date=str(datetime.date.today())
        data=QATushare.QA_fetch_get_stock_day(str(item)[0:6],start_date,end_date)[1::]
        coll_stock_day.insert_many(data)


def QA_update_standard_sql():
    print('正在整理和更新数据,请稍等.....')
    coll=pymongo.MongoClient().quantaxis.stock_day
    coll.ensure_index('code')
    """
    for item in coll.find():
        date=item['date']
        date_stamp=QA_util_date_stamp(date)
        coll.update({"_id":item['_id']},{'$set':{'date_stamp':date_stamp}})
    """


