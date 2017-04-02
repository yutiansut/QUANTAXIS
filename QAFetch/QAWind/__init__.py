#coding:utf-8
from . import stock

# 此处属于二次封装API,可以根据自己需要二次封装

def get_stock_Info(name,startDate,endDate):
    return stock.getStock_Info(name,startDate,endDate)

