# -*- coding: utf-8 -*-
import datetime
from gmsdk import md,to_dict
import pandas as pd
md.init('13382753152','940809')
CFFEX = ['IF','IH','IC','T','TF']
CZCE =['CF','FG','MA','RM','SR','TA','ZC']
SHFE = ['AL','BU','CU','HC','NI','RB','RU','SN','ZN']
DCE=['C','CS','I','J','JD','JM','L','M','P','PP','V','Y']
def mtsymbol_list(symbol_list):
    z = len (symbol_list)
    ret = ''
    for i in range(z):
        ret = ret + symbol_list[i] +','
    ret = ret[:len(ret)-1]
    return ret
def to_pd(var,index):
    ret =[]
    for i in var:
        ret.append(to_dict(i))
    ret = pd.DataFrame (ret)
    ret = ret.set_index(index)
    return ret
def get_shse( ):
    var =md.get_instruments('SHSE', 1, 0)
    return to_pd(var,'symbol')
def get_szse():
    var =md.get_instruments('SZSE', 1, 0)
    return to_pd(var,'symbol')
def get_shfe():
    var = md.get_instruments('SHFE', 4, 1)
    return to_pd(var,'symbol')
def get_dce():
    var = md.get_instruments('DCE', 4, 1)
    return to_pd(var,'symbol')
def get_czce():
    var =  md.get_instruments('CZCE', 4, 1)
    return to_pd(var,'symbol')
def get_cffex():
    var = md.get_instruments('CFFEX', 4, 1)
    return to_pd(var,'symbol')
def get_index():
    shse = md.get_instruments('SHSE', 3, 1)
    shse =to_pd(shse,'symbol')
    szse = md.get_instruments('SZSE', 3, 1)
    szse =to_pd(szse,'symbol')
    return shse.append(szse)
def get_etf():
     shse = md.get_instruments('SHSE', 5, 0)
     return to_pd(shse,'symbol')
def get_fund():
    shse = md.get_instruments('SHSE', 2, 0)
    shse =to_pd(shse,'symbol')
    szse = md.get_instruments('SZSE', 2, 0)
    szse =to_pd(szse,'symbol')
    return shse.append(szse)
def get_instruments_by_name(name):#期货接口
    var = md.get_instruments_by_name(name)
    z = len(var)
    for i in range (z):
        k = z-1-i
        if var[k].is_active == 0:
            del var[k]
    return to_pd(var,'symbol')
def get_constituents(index_symbol):#指数权重
    var = md.get_constituents(index_symbol)
    return to_pd(var,'symbol')
def get_financial_index(symbol, t_begin, t_end):
    if len(t_begin) < 10 :
        t_begin = t_begin + ' 00:00:00'
    if len(t_end) < 10 :
        t_end = t_end + ' 15:00:00'
    var =md.get_financial_index(symbol, t_begin, t_end)
    var =to_pd(var,'pub_date')
    return var
def get_last_financial_index(symbol_list):
    var = md.get_last_financial_index(mtsymbol_list(symbol_list))
    var = to_pd(var,'symbol')
    return var
def get_share_index(symbol_list):
    var = md.get_last_share_index(mtsymbol_list(symbol_list))
    var = to_pd(var, 'symbol')
    return var
def get_market_index(symbol_list):
    var = md.get_last_market_index(mtsymbol_list(symbol_list))
    var = to_pd(var, 'symbol')
    return var
def get_calendar(exchange, start_time, end_time):
    var = md.get_calendar(exchange, start_time, end_time)
    ret = []
    for i in var:
        Date = datetime.datetime.utcfromtimestamp(i.utc_time)
        ret.append (Date)
    return ret

####md
def tick_topd(var,index):
    ret = []
    for i in var:
        tmp = {}
        Date = datetime.datetime.utcfromtimestamp(i.utc_time)
        Date = Date + datetime.timedelta(hours=8)
        tmp['date'] = Date
        tmp['code'] = i.exchange + '.' + i.sec_id
        tmp['close'] = i.last_price
        tmp['vol'] = i.last_volume
        tmp['amount'] = i.last_amount
        tmp['opi'] = i.cum_position
        tmp['买一价'] = i.bids[0][0]
        tmp['买一量'] = i.bids[0][1]
        tmp['卖一价'] = i.asks[0][0]
        tmp['卖一量'] = i.asks[0][1]
        ret.append(tmp)
    ret = pd.DataFrame(ret)
    ret = ret.set_index(index)
    return ret
def get_ticks(symbol, begin_time, end_time):
    var = md.get_ticks(symbol, begin_time, end_time)
    ret = tick_topd(var,'date')
    return ret
def bar_topd(var,index):
    ret = []
    z = len(var)
    for j in range (z):
        i =var[j]
        
        tmp = {}
        Date = datetime.datetime.utcfromtimestamp(i.utc_time)
        Date = Date + datetime.timedelta(hours=8)
        tmp['date'] = Date
        tmp['code'] = i.exchange + '.' + i.sec_id
        tmp['close'] = i.close
        tmp['high'] = i.high
        tmp['low'] = i.low
        tmp['open'] = i.open
        tmp['vol'] = i.volume
        tmp['amount'] = i.amount
        if i.exchange in ['SHSE','SZSE'] :
            tmp['adj'] = i.adj_factor
        else:
            tmp['opi'] = i.position
        ret.append(tmp)
    ret = pd.DataFrame(ret)
    ret = ret.set_index(index)
    return ret
def get_bars(symbol, bar_type, begin_time, end_time):
    var = md.get_bars(symbol, bar_type, begin_time, end_time)
    ret = bar_topd(var,'date')
    return ret
def get_dailybars(symbol, begin_time, end_time):
    var = md.get_dailybars(symbol, begin_time, end_time)
    ret = bar_topd(var,'date')
    return ret
def get_last_ticks(symbol_list):
    symbol_list = mtsymbol_list(symbol_list)
    var = md.get_last_ticks(symbol_list)
    ret = tick_topd(var,'code')
    return ret
def get_last_bars(symbol_list, bar_type):
    symbol_list = mtsymbol_list(symbol_list)
    var = md.get_last_bars(symbol_list, bar_type)
    ret = bar_topd(var,'code')
    return ret
def get_last_dailybars(symbol_list):
    symbol_list = mtsymbol_list(symbol_list)
    var = md.get_last_dailybars(symbol_list)
    ret = bar_topd(var,'code')
    return ret
def get_last_n_ticks(symbol, n):
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    var = md.get_last_n_ticks(symbol, n, end_time)
    ret = tick_topd(var,'date')
    return ret
def get_last_n_bars(symbol, bar_type, n):
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    VAR = md.get_last_n_bars(symbol, bar_type, n, end_time)
    z = len(VAR)
    var = []
    for i in range(z):
        var.append(VAR[z-1-i])
    ret = bar_topd(var,'date')
    return ret
def get_last_n_dailybars(symbol, n):
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    VAR = md.get_last_n_dailybars(symbol, n, end_time)
    z = len(VAR)
    var = []
    for i in range(z):
        var.append(VAR[z-1-i])
    ret = bar_topd(var,'date')
    return ret