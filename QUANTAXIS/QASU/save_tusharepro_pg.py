# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import talib
import pandas as pd
import numpy as np
import time
import datetime
import pymongo
import tushare as ts
from sqlalchemy import create_engine
import psycopg2  
import warnings
warnings.filterwarnings("ignore")
import QUANTAXIS as QA
from QUANTAXIS.QAUtil.QALogs import (QA_util_log_debug, QA_util_log_expection,
                                     QA_util_log_info)

from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_trade_range
from QUANTAXIS.QAUtil.QADate import (QA_util_date_str2int,QA_util_date_int2str)


token='xxxx'  #你的tusharepro token
pro=ts.pro_api(token)
def cilent_pg():
    Account='postgres'#pg账号
    Password='xxxxx'   #pg密码
    database='quantaxis'  #该数据库需要提前手动建立，应该有自动建立方法，还不会。。。
    client = create_engine('postgresql+psycopg2://'+Account+':'+Password+'@127.0.0.1:5432/'+database)  
    return client 

def save_data_to_postgresql(name_biao,data,if_exists='replace',client=cilent_pg()):
        data.to_sql(name_biao,client,index=False,if_exists=if_exists)
    
def load_data_from_postgresql(mes='',client=cilent_pg()):
    res=pd.read_sql(mes,client)
    return res

def download_day_data_from_tushare(trade_date='20190102'):   
    trade_date = trade_date.replace('-', '') #兼容设置以防日期格式为2001-10-20格式
    lastEx = None
    retry = 10
    for _ in range(retry):
        try:
            df_daily=pro.query('daily',trade_date=trade_date)
            df_daily_basic=pro.query('daily_basic',trade_date=trade_date)
            df_factor=pro.query('adj_factor',trade_date=trade_date)             
            break 
        except Exception as ex:
            lastEx = ex
            QA_util_log_info("[{}]TuSharePro数据异常: {}, retrying...".format(trade_date, ex))
    else:
        QA_util_log_info("[{}]TuSharePro异常: {}, retried {} times".format(trade_date,lastEx, retry))
        return None   
    df=pd.merge(df_daily,df_factor,how='left')
    res=pd.merge(df,df_daily_basic,how='left').sort_values(by = 'ts_code')
    res['code']=res['ts_code'].apply(lambda x:x[:6]) #x[7:9].lower()
    res['trade_date'] = pd.to_datetime(res['trade_date'], format='%Y-%m-%d')
    return res 
      
def QA_fetch_stock_day_pg(code=['000001','000002'],start_date='19000101',end_date='20500118',data='*'):
    name_biao='stock_day'
    if isinstance(code,list):
        code="','".join(code)
        mes='select '+ data+' from '+name_biao+" where  trade_date >= date_trunc('day',timestamp '"+start_date+"') and trade_date <= date_trunc('day',timestamp '"+end_date+"') and code in ('"+code+"');"
        try:   
            t=time.time()        
            res=load_data_from_postgresql(mes=mes)
            t1=time.time()
            QA_util_log_info('load '+ name_biao+ ' success,take '+str(round(t1-t,2))+' S')              
        except Exception as e:
            print(e)
            res=None
    else:
        QA_util_log_info('code type is not list, please cheack it.')         
    return res

def QA_fetch_stock_list_pg(name_biao='stock_list'):
    mes='select * from '+name_biao+";"    
    try:   
        t=time.time()        
        res=load_data_from_postgresql(mes=mes)
        t1=time.time()
        QA_util_log_info('load '+ name_biao+ ' success,take '+str(round(t1-t,2))+' S')              
    except Exception as e:
        print(e)
        res=None
    return res
    
def QA_save_stock_list_pg():    
    stock_list_l= pro.stock_basic(exchange_id='', is_hs='',list_status='L' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_D= pro.stock_basic(exchange_id='', is_hs='',list_status='D' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    stock_list=pd.concat([stock_list_l,stock_list_D],axis=0)
    stock_list=pd.concat([stock_list,stock_list_P],axis=0)
    try:   
        t=time.time()    
        save_data_to_postgresql('stock_list',stock_list)
        t1=time.time()
        QA_util_log_info('save stock_list data success,take '+str(round(t1-t,2))+' S') 
    except Exception as e:        
        print(e)      

def QA_save_stock_day_pg(start_date='19901219'):    
    t = time.localtime(time.time())
    if int(time.strftime('%H%M%S',t))<190000:   #晚上七点之后在更新当天数据，以免不及时
        t = time.localtime(time.time()-3600*24)
        tS = time.strftime("%Y-%m-%d", t)  
    else:                
        tS = time.strftime("%Y-%m-%d", t)    
    end_date=tS
    try: 
        mes='select distinct trade_date from stock_day;'
        trade_data_pg=load_data_from_postgresql(mes=mes).trade_date.tolist()
        for i in range(len(trade_data_pg)):
            trade_data_pg[i]=trade_data_pg[i].strftime("%Y-%m-%d")
    except: #第一次运行
        trade_data_pg=list()
        
    if isinstance(start_date,int):
        start_date=QA_util_date_int2str(start_date)
    elif len(start_date)==8:
        start_date=start_date[0:4]+'-'+start_date[4:6]+'-'+start_date[6:8]
        
    trade_date=QA_util_get_trade_range(start_date,end_date) 
    trade_date2=list(set(trade_date)^set(trade_data_pg))
    trade_date2.sort() 
    if len(trade_date2)==0:
        QA_util_log_info('Stock day is up to date and does not need to be updated')
    for i in trade_date2:
        pass
        try:
            t=time.time()        
            df=download_day_data_from_tushare(i)    
            #i=i[7:10].lower()+i[0:6]
            save_data_to_postgresql('stock_day',df,'append')
            t1=time.time()   
            QA_util_log_info('save '+i+' stock day success,take '+str(round(t1-t,2))+' S')        
        except Exception as e:
            print(e)
if __name__ == '__main__':          
    #储存股票列表 包含ts_pro中股票列表所有信息
    QA_save_stock_list_pg() 
    #储存日线数据  包含ts_pro中"daily" "daily_basic" "adj_factor"所有内容 
    #由于采用日期对比机制进行储存，可以增量储存之前数据
    QA_save_stock_day_pg()  #A_save_stock_day_pg('20180101')储存起始日期

    ##获取股票代码
    #stock_code=QA_fetch_stock_list_pg()['symbol'][:30].tolist()
    ##获取日线数据
    #start_date='20190101'
    #end_date='20190120'
    #data='trade_date,code,open,close,high,low,change,vol,amount,adj_factor,turnover_rate_f,pe' #提取部分项目
    ##获取代码所有日线数据
    #stock_data1=QA_fetch_stock_day_pg(stock_code) 
    ##获取固定日期代码所有日线数据 
    #stock_data2=QA_fetch_stock_day_pg(code=stock_code,start_date=start_date,end_date=end_data)  
    # #获取固定日期代码部分日线数据 
    #stock_data3=QA_fetch_stock_day_pg(code=stock_code,start_date=start_date,end_date=end_date,data=data) 


