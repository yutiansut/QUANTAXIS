#coding:utf-8
from . import stock,tradeday

# 此处属于二次封装API,可以根据自己需要二次封装
# 二次封装基于[QAS-501-1](https://github.com/yutiansut/QUANTAXIS/tree/0.3.8-dev-fetch/docs#qas-501-1-fetch)

def get_stock_Info(name,startDate,endDate):
    return stock.getStock_Info(name,startDate,endDate)

def get_stock_day(name,startDate,endDate):
    return stock.getStock_Day(name,startDate,endDate)

def get_trade_date(endDate,exchange):
    return tradeday.get_trade_date(endDate,exchange)

def get_stock_min():
    pass
def get_stock_tick():
    pass
def get_stock_indicator():
    pass
def get_future_day():
    pass
def get_future_min():
    pass
def get_future_tick():
    pass
def get_future_info():
    pass
def get_options_day():
    pass
def get_options_min():
    pass
def get_options_tick():
    pass
def get_options_info():
    pass
def save_stock():
    pass
def save_future():
    pass
def save_options():
    pass
def save_all():
    pass
