#coding:utf-8
from QUANTAXIS.QAUtil import QA_util_log_info,QA_Setting,QA_util_sql_mongo_setting
from QUANTAXIS.QAUtil import QA_util_date_valid,QA_util_date_stamp
def QA_fetch_data(variety,level,id,startDate,endDate):
    client=QA_Setting.client
    db=client.quantaxis
    if variety in ['stock','future','options']:
        if level in ['day','min','ms']:
            coll_str=str(variety)+'_'+str(level)
            coll=db.coll_str
            if QA_util_date_valid(endDate)==True:
                for items in coll.find({'code':str(id)[0:6],"date_stamp":{"lte":QA_util_date_stamp(endDate)},"datestamp":{"gte":QA_util_date_stamp(startDate)}}):
                    print(items)
    