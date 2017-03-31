# -*- coding: utf-8 -*-
import QAGmsdk.gmdata as QAGmsdk


###############################################

def get_shse():
    return QAGmsdk.get_shse()
def get_szse():
    return QAGmsdk.get_szse()
def get_dce():
    return QAGmsdk.get_dce()
def get_czce():
    return QAGmsdk.get_czce()
def get_shfe():
    return QAGmsdk.get_shfe()
def get_cffex():
    return QAGmsdk.get_cffex()
def get_index():#证券指数
    return QAGmsdk.get_index()
def get_constituents(index_symbol):#指数权重
    return QAGmsdk.get_constituents(index_symbol)#指数权重
def get_etf():#期权
    return QAGmsdk.get_etf()
def get_fund():
    return QAGmsdk.get_fund()
def get_instruments_by_name(name):#期货接口----这里注意代码大小写，大写是连续合约，小写是具体的合约
    return QAGmsdk.get_instruments_by_name(name)
def get_financial_index(symbol, t_begin, t_end):
    return QAGmsdk.get_financial_index(symbol, t_begin, t_end)
def get_last_financial_index(symbol_list):
    return QAGmsdk.get_last_financial_index(symbol_list)
def get_share_index(symbol_list):
    return QAGmsdk.get_share_index(symbol_list)
def get_market_index(symbol_list):
    return QAGmsdk.get_market_index(symbol_list)
def get_ticks(symbol, begin_time, end_time):
    return QAGmsdk.get_ticks(symbol, begin_time, end_time)#tick
def get_last_ticks(symbol_list):
    return QAGmsdk.get_last_ticks(symbol_list)
def get_last_n_ticks(symbol, n):
    return QAGmsdk.get_last_n_ticks(symbol, n)#n tick 
def get_bars(symbol, bar_type, begin_time, end_time):#分钟K
    return QAGmsdk.get_bars(symbol, bar_type, begin_time, end_time)
def get_last_bars(symbol_list, bar_type):#最后一个分钟K
    return QAGmsdk.get_last_bars(symbol_list, bar_type)
def get_last_n_bars(symbol, bar_type, n):#N个分钟K
    return QAGmsdk.get_last_n_bars(symbol, bar_type, n)
def get_dailybars(symbol, begin_time, end_time):#日线BAR
    return QAGmsdk.get_dailybars(symbol, begin_time, end_time)
def get_last_dailybars(symbol_list):#最后
    return QAGmsdk.get_last_dailybars(symbol_list)
def get_last_n_dailybars(symbol, n):#N个日线K
    return QAGmsdk.get_last_n_dailybars(symbol, n)

