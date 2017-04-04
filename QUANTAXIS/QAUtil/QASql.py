#coding:utf-8

import pymongo
import re
import datetime
import time


def QA_util_sql_mongo_setting(ip,port):
    return pymongo.MongoClient(ip,port)