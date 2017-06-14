#coding:utf-8

"""
The MIT License (MIT)

Copyright (c) 2016-2017 yutiansut/QUANTAXIS

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


import datetime
import time
import re

def QA_util_date_stamp(date):
    #date function
    datestr=str(date)[0:10]
    date=time.mktime(time.strptime(datestr,'%Y-%m-%d'))
    return date
def QA_util_time_stamp(time):
    time=str(time)[0:10]
    
    return time
def QA_util_ms_stamp(ms):
    return ms

def QA_util_date_valid(date):
    try:
        
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False
def QA_util_realtime(strtime,client):
    time_stamp=QA_util_date_stamp(strtime)
    coll=client.quantaxis.trade_date
    temp_str=coll.find_one({'date_stamp':{"$gte":time_stamp}})
    time_real=temp_str['date']
    time_id=temp_str['num']
    return {'time_real':time_real,'id':time_id}

def QA_util_id2date(id,client):
    coll=client.quantaxis.trade_date
    temp_str=coll.find_one({'num':id})
    return temp_str['date']

def QA_util_is_trade(date,code,client):
    coll=client.quantaxis.stock_day
    date=str(date)[0:10]
    is_trade=coll.find_one({'code':code,'date':date})
    try:
        len(is_trade)
        return True
    except:
        return False



def QA_util_get_real_date(date,trade_list,towards):
        #print(date in trade_list)
        if towards==1:
            while date not in trade_list:
                date= str(datetime.datetime.strptime(date, '%Y-%m-%d')  + datetime.timedelta(days = 1))[0:10]
            else: 
                return date
        elif towards==-1:
            while date not in trade_list:
                date= str(datetime.datetime.strptime(date, '%Y-%m-%d')  - datetime.timedelta(days = 1))[0:10]
            else: 
                return date
def QA_util_get_date_index(date,trade_list):
    return trade_list.index(date)
def QA_util_get_index_date(id,trade_list):
    return trade_list[id]