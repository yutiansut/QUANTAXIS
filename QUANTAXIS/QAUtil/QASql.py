#coding:utf-8

import pymongo
import re
import datetime
import time
from ..QAUtil import QA_util_log_info

def QA_util_sql_mongo_setting(ip,port):
    QA_sql_mongo_client=pymongo.MongoClient(ip,port)
    QA_util_log_info('ip:'+str(ip)+'   port:'+str(port))
    return QA_sql_mongo_client
