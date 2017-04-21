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

    
    for i in df.index:  
        print(i)
        data=ts.get_hist_data(i)
        try:
            data_json=json.loads(data.to_json(orient='records'))
            coll=pymongo.MongoClient().quantaxis.stock_day
            coll.insert_many(data_json)
        except:
            print('none data')
