# coding: utf-8

import tushare as QATs


def get_stock_day(name,startDate,endDate):
    if (len(name)!=6):
        name=str(name)[0:6]
    return QATs.get_k_data(name,startDate,endDate,ktype='D')

def get_stock_info(name):
    if (len(name)!=6):
        name=str(name)[0:6]
    return QATs.get_stock_basics()

def get_stock_tick(name,date):
    if (len(name)!=6):
        name=str(name)[0:6]
    return QATs.get_tick_data(name,date)
    
#test

#print(get_stock_day("000001",'2001-01-01','2010-01-01'))
#print(get_stock_tick("000001.SZ","2017-02-21"))