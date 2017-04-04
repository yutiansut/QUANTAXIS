from ..QAFetch import QAWind
from ..QAUtil import util_date_stamp,util_time_stamp
import pymongo
import datetime
import re
import time
# get all stock data,save
# under QUANTAXIS_Standard_501[QAS 501]
def save_stock_list():
    datestr=datetime.datetime.now().strftime("%Y-%m-%d")
    data=QAWind.get_stock_list(datestr)
    #print(stocklist)
    coll=pymongo.MongoClient().quantaxis.stock_list
    coll.insert({'date':data[0][0],'datestamp':data[0][0].timestamp(),"stock":{'code':data[1],'name':data[2]}})
def save_trade_date():
    datestr=datetime.datetime.now().strftime("%Y-%m-%d")
    data=QAWind.get_trade_date(datestr,'SSE')
    coll=pymongo.MongoClient().quantaxis.trade_date
    #print(stocklist)
    for i in range(0,len(data[0]),1):
        coll.insert({'date':data[0][i],'datestamp':data[0][i].timestamp(),'exchangeName':'SSE'})
def save_stock_day(name,startDate,endDate):
    coll=pymongo.MongoClient().quantaxis.stock_day
    #find if have the same
    start_date_stamp=util_date_stamp(startDate)
    end_date_stamp=util_date_stamp(endDate)
    coll.find({'last_trade_day'})
    
    data=QAWind.get_stock_day(name,startDate,endDate)
    
    for i in range(0,len(data[0]),1):
        #sec_name,pre_close,open,high,close,volume,amt,dealnum,chg,pct_chg,swing,vwap,adjfactor,turn,free_turn,lastradeday_s,last_trade_day,rel_ipo_chg,rel_ipo_pct_chg,trade_status,susp_days,susp_reason,maxupordown,open3,high3,low3,close3
        coll.insert({'code':name,'name':data[0][i],'pre_close':data[1][i],'open':data[2][i],'high':data[3][i],'close':data[4][i],'volume':data[5][i],'amt':data[6][i],'dealnum':data[7][i],'chg':data[8][i],'pct_chg':data[9][i],'swing':data[10][i],'vwap':data[11][i],'adjfactor':data[12][i],'turn':data[13][i],'free_turn':data[14][i],'lastradeday_s':data[15][i],'last_trade_day':data[16][i],'rel_ipo_chg':data[17][i],'rel_ipo_pct_chg':data[18][i],'trade_status':data[19][i],'susp_days':data[20][i],'susp_reason':data[21][i],'maxupordown':data[22][i],'open3':data[23][i],'high3':data[24][i],'low3':data[25][i],'close3':data[26][i]})

