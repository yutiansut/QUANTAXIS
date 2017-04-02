#coding:utf-8
from . import stock

# 此处属于二次封装API,可以根据自己需要二次封装
# 二次封装基于[QAS-501-1](https://github.com/yutiansut/QUANTAXIS/tree/0.3.8-dev-fetch/docs#qas-501-1-fetch)

def get_stock_Info(name,startDate,endDate):
    return stock.getStock_Info(name,startDate,endDate)

