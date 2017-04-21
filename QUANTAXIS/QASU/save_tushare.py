# coding :utf-8 

from QUANTAXIS.QAFetch import QATushare
from QUANTAXIS.QAUtil import QA_util_date_stamp,QA_util_time_stamp
from QUANTAXIS.QAUtil import QA_Setting
import datetime,json
import re
import time
import pymongo

def QA_save_stock_day_all(code):
    code=str(code)[0:6]
    data=QATushare.QA_fetch_get_stock_day_all(code)
    data_json=json.loads(data.to_json(orient='records'))
    pymongo.MongoClient().quantaxis.stock_day.insert(data_json)