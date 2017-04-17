from ..QAFetch import QAWind
from ..QAUtil import QA_util_date_stamp,QA_util_time_stamp,QA_util_log_info
from QUANTAXIS.QAUtil import QA_Setting
import pymongo
import datetime
import re
import time


# get all stock data,save
# under QUANTAXIS_Standard_501[QAS 501]
def QA_SU_save_stock_list(client):
    datestr=datetime.datetime.now().strftime("%Y-%m-%d")
    data=QAWind.QA_fetch_get_stock_list(datestr)
    #QA_util_log_info(stocklist)
    coll=client.quantaxis.stock_list
    coll.insert({'date':data[0][0],'date_stamp':data[0][0].timestamp(),"stock":{'code':data[1],'name':data[2]}})
def QA_SU_save_trade_date(client):
    datestr=datetime.datetime.now().strftime("%Y-%m-%d")
    data=QAWind.QA_fetch_get_trade_date(datestr,'SSE')
    coll=client.quantaxis.trade_date
    #QA_util_log_info(stocklist)
    for i in range(0,len(data[0]),1):
        coll.insert({'date':data[0][i],'date_stamp':data[0][i].timestamp(),'exchangeName':'SSE'})
def QA_SU_save_stock_day(name,startDate,endDate,client):
    coll=client.quantaxis.stock_day
    #find if have the same
    start_date_stamp=QA_util_date_stamp(startDate)
    end_date_stamp=QA_util_date_stamp(endDate)
    if (coll.find({"code":name,"last_trade_day":{"$gte":int(end_date_stamp),"$lte":int(start_date_stamp)}}).count()==0):
        QA_util_log_info(str(name)+'--'+str(startDate)+'--'+str(endDate))
        data=QAWind.QA_fetch_get_stock_day(name,startDate,endDate)
        QA_util_log_info(len(data[0]))
        for i in range(0,len(data[0]),1):
            QA_util_log_info('now saving====='+str(name)+'===date===='+str(data[16][i]))
            #sec_name,pre_close,open,high,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,lastradeday_s,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,trade_status,susp_days,susp_reason,maxupordown,open3,high3,low3,close3
            coll.insert({'code':name,'name':data[0][i],'pre_close':data[1][i],'open':data[2][i],'high':data[3][i],'low':data[4][i],'close':data[5][i],'volume':data[6][i],'amt':data[7][i],'dealnum':data[8][i],'chg':data[9][i],'pct_chg':data[10][i],'swing':data[11][i],'vwap':data[12][i],'adjfactor':data[13][i],'turn':data[14][i],'free_turn':data[15][i],'lastradeday_s':data[16][i],'last_trade_day':data[17][i],'rel_ipo_chg':data[18][i],'rel_ipo_pct_chg':data[19][i],'trade_status':data[20][i],'susp_days':data[21][i],'susp_reason':data[22][i],'maxupordown':data[23][i],'open3':data[24][i],'high3':data[25][i],'low3':data[26][i],'close3':data[27][i]})
    else:
        QA_util_log_info('there is something wrong with the date')
def QA_SU_save_stock_day_simple(name,startDate,endDate,client):
    coll=client.quantaxis.stock_day
    #find if have the same
    start_date_stamp=QA_util_date_stamp(startDate)
    end_date_stamp=QA_util_date_stamp(endDate)
    if (coll.find({"code":name,"last_trade_day":{"$gte":int(end_date_stamp),"$lte":int(start_date_stamp)}}).count()==0):
        QA_util_log_info(str(name)+'--'+str(startDate)+'--'+str(endDate))
        data=QAWind.QA_fetch_get_stock_day_simple(name,startDate,endDate)
        QA_util_log_info(len(data[0]))
        for i in range(0,len(data[0]),1):
            QA_util_log_info('now saving====='+str(name)+'===date===='+str(data[16][i]))
            #sec_name,pre_close,open,high,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,lastradeday_s,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,trade_status,susp_days,susp_reason,maxupordown,open3,high3,low3,close3
            coll.insert({'code':name,'name':data[0][i],'pre_close':data[1][i],'open':data[2][i],'high':data[3][i],'low':data[4][i],'close':data[5][i],'volume':data[6][i]})
    else:
        QA_util_log_info('there is something wrong with the date')

def QA_SU_save_stock_day_init(startDate,client):
    #just for first using
    coll_get=client.quantaxis.stock_list
    item=coll_get.find_one({"date_stamp":{"$gte":1483200000.0}})
    for stock_name in item['stock']['code']:
        QA_util_log_info('now init the stock_day of---'+str(stock_name))

        QA_SU_save_stock_day(str(stock_name),startDate,str(datetime.date.today()),client)
def QA_SU_save_stock_day_init_simple(startDate,client):
    #just for first using
    coll_get=client.quantaxis.stock_list
    item=coll_get.find_one({"date_stamp":{"$gte":1483200000.0}})
    for stock_name in item['stock']['code']:
        QA_util_log_info('now init the stock_day of---'+str(stock_name))

        QA_SU_save_stock_day_simple(str(stock_name),startDate,str(datetime.date.today()),client)
