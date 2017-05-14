# encoding: UTF-8
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QAUtil import QA_util_date_valid,QA_util_date_stamp
from pandas import DataFrame
from bson.objectid import ObjectId
import numpy
import datetime

"""
按要求从数据库取数据，并转换成dataframe结构

"""
def QA_fetch_data(code,startDate,endDate,collections):
    #print(datetime.datetime.now())
    startDate=str(startDate)[0:10]
    endDate=str(endDate)[0:10]

    coll=collections
    if QA_util_date_valid(endDate)==True:

        list_a=[[],[],[],[],[],[],[]]

        for item in coll.find({'code':str(code)[0:6],"date_stamp":{"$lte":QA_util_date_stamp(endDate),"$gte":QA_util_date_stamp(startDate)}}):
            #print(item['code'])
            list_a[0].append(item['code'])
            list_a[1].append(item['open'])
            list_a[2].append(item['high'])
            list_a[3].append(item['low'])
            list_a[4].append(item['close'])
            list_a[5].append(item['volume'])
            list_a[6].append(item['date'])
            #print(datetime.datetime.now())
        data=numpy.asarray(list_a).transpose()
        #data=DataFrame(list_a).transpose()
        #print(datetime.datetime.now())
        return data
    else:
        QA_util_log_info('something wrong with date')


def QA_fetch_trade_date(collections):
    return collections.find()
def QA_fetch_stock_day(code,collections):
    list_a=[[],[],[],[],[],[],[]]
    
    for item in collections.find({'code':str(code)[0:6]}):
        #print(item['code'])
        list_a[0].append(item['code'])
        list_a[1].append(item['open'])
        list_a[2].append(item['high'])
        list_a[3].append(item['low'])
        list_a[4].append(item['close'])
        list_a[5].append(item['volume'])
        list_a[6].append(item['date'])
        #print(datetime.datetime.now())
    data=numpy.asarray(list_a).transpose()
    return data