# coding :utf-8 

from QUANTAXIS.QAFetch import QATushare
from QUANTAXIS.QAUtil import QA_util_date_stamp,QA_Setting,QA_util_date_valid
import json
import pymongo
import datetime
import re
import time

def QA_update_stock_day_new():
    pass
def QA_update_stock_day_all(code):
    pass

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


