# -*- coding: utf-8 -*-
import pydata.getdata as gt
import pydata.gmdata as mt

def get_financial(symbol):#3大财报
    return gt.get_financial(symbol)
def get_ipo():#新股
    return gt.ths_ipo()
def get_tfp(Date):#停复牌
    return gt.get_tfp(Date)
def get_brief(symbol_list):# 公司概况
    return gt.get_brief(symbol_list)
def get_lastest(symbol_list):#最新资料
    return  gt.get_lastest(symbol_list)
def get_dividend(symbol):#分红
    return gt.get_dividend(symbol)
def get_allotment(symbol):#配股
    return gt.get_allotment(symbol)
def get_fh_all():#当年全部股票的分红资料
    return gt.get_fh_all()
def get_stocklist():#全部股票列表
    return gt.get_stocklist()
def get_last_daybar(symbol_list):#股票日线截面数据
    return gt.get_last_dailybar(symbol_list)
def get_last_tick(symbol_list):#最后1个tick
    return gt.get_last_tick(symbol_list)
def get_last100_ticks(symbol_list):#最后100个tick
    return gt.get_last100_ticks(symbol_list)
def get_all_ticks(symbol_list):#当日全部tick
    return gt.get_all_ticks(symbol_list)
def get_moneyflow(symbol_list):#当日资金流量截面数据
    return gt.get_moneyflow(symbol_list)
def get_money_on_minute(symbol):#当日资金流量每分钟数据
    return gt.get_money_on_minute(symbol)
def get_tick_history(symbol,Date):#历史TICK接口
    return gt.get_tick_history(symbol,Date)
def get_fjb(tick):
    return tick.groupby(['close']).sum()
def tick_to_min(tick,n):
    return gt.tick_to_min(tick,n)
def get_last_n_daybar(symbol,n,Type):#cs =['600100', 200, 'qfq']
    cs= [symbol,n,Type]
    return gt.get_last_n_dailybars(cs)
def get_all_daybar(symbol,Type):#cs=['600100','qfq']#
    cs =[symbol,Type]
    return gt.get_all_dailybars(cs)
def get_yearlist(symbol):
    cs =[symbol,'bfq']
    return gt.get_yearlist(cs)
def get_daybar_year(symbol,year,Type):
    cs = [symbol,year,Type]
    return gt.get_dailybars_year(cs)
def get_stock_bar(symbol,Type):#实时行情接口
    cs=[symbol,Type]
    return gt.get_bars(cs)
def get_money_30days(symbol):#30天的资金流量数据
    return gt.get_money_30days(symbol)
def get_future_list(id):#分类合约,id = 'dce'  id = 'dce.c
    return gt.get_future_list(id)
def get_future_symbol(id):#某个品种的全部合约代码
    var =get_future_list(id)
    return list(var[0].index)
def get_zhuli():#得到主力合约
    return gt.get_zhuli()
def get_future_bars(symbol,Type):#期货分钟及日K
    cs=[symbol,Type]
    return gt.get_future_bars(cs)
def get_future_info(symbol):#期货合约基本信息
    return gt.future_info(symbol)
def get_calendar(starttime,endtime):#交易日历
    return  gt.get_calendar(starttime,endtime)
def get_future_tick(symbol):#期货TICK数据
    return gt.get_future_tick(symbol)
###############################################
#myquant接口
def get_shse():
    return mt.get_shse()
def get_szse():
    return mt.get_szse()
def get_dce():
    return mt.get_dce()
def get_czce():
    return mt.get_czce()
def get_shfe():
    return mt.get_shfe()
def get_cffex():
    return mt.get_cffex()
def get_index():#证券指数
    return mt.get_index()
def get_constituents(index_symbol):#指数权重
    return mt.get_constituents(index_symbol)#指数权重
def get_etf():#期权
    return mt.get_etf()
def get_fund():
    return mt.get_fund()
def get_instruments_by_name(name):#期货接口----这里注意代码大小写，大写是连续合约，小写是具体的合约
    return mt.get_instruments_by_name(name)
def get_financial_index(symbol, t_begin, t_end):
    return mt.get_financial_index(symbol, t_begin, t_end)
def get_last_financial_index(symbol_list):
    return mt.get_last_financial_index(symbol_list)
def get_share_index(symbol_list):
    return mt.get_share_index(symbol_list)
def get_market_index(symbol_list):
    return mt.get_market_index(symbol_list)
def get_ticks(symbol, begin_time, end_time):
    return mt.get_ticks(symbol, begin_time, end_time)#tick
def get_last_ticks(symbol_list):
    return mt.get_last_ticks(symbol_list)
def get_last_n_ticks(symbol, n):
    return mt.get_last_n_ticks(symbol, n)#n tick 
def get_bars(symbol, bar_type, begin_time, end_time):#分钟K
    return mt.get_bars(symbol, bar_type, begin_time, end_time)
def get_last_bars(symbol_list, bar_type):#最后一个分钟K
    return mt.get_last_bars(symbol_list, bar_type)
def get_last_n_bars(symbol, bar_type, n):#N个分钟K
    return mt.get_last_n_bars(symbol, bar_type, n)
def get_dailybars(symbol, begin_time, end_time):#日线BAR
    return mt.get_dailybars(symbol, begin_time, end_time)
def get_last_dailybars(symbol_list):#最后
    return mt.get_last_dailybars(symbol_list)
def get_last_n_dailybars(symbol, n):#N个日线K
    return mt.get_last_n_dailybars(symbol, n)

