#coding:utf-8
from QUANTAXIS.QAUtil import QA_util_log_info,QA_Setting,QA_util_sql_mongo_setting
from QUANTAXIS.QAUtil import QA_util_date_valid,QA_util_date_stamp
from pandas import DataFrame
from bson.objectid import ObjectId
import numpy

"""
按要求从数据库取数据，并转换成dataframe结构

"""
def QA_fetch_data(variety,level,id,startDate,endDate):
    startDate=str(startDate)[0:10]
    endDate=str(endDate)[0:10]
    client=QA_Setting.client
    db=client.quantaxis
    if variety in ['stock','future','options']:
        if level in ['day','min','ms']:
            coll_str='db.'+str(variety)+'_'+str(level)
            coll=db.stock_day
            if QA_util_date_valid(endDate)==True:

                list_a=[[],[],[],[],[],[],[]]

                for item in coll.find({'code':str(id)[0:6],"date_stamp":{"$lte":QA_util_date_stamp(endDate),"$gte":QA_util_date_stamp(startDate)}}):
                    #print(item['code'])
                    list_a[0].append(item['code'])
                    list_a[1].append(item['high'])
                    list_a[2].append(item['low'])
                    list_a[3].append(item['open'])
                    list_a[4].append(item['close'])
                    list_a[5].append(item['volume'])
                    list_a[6].append(item['date'])
                data=DataFrame(list_a).transpose()
                return data
            else:
                QA_util_log_info('something wrong with date')
                    