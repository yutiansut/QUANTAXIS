# coding :utf-8

import QAFetch

def get_stock_day(name):
    return QAFetch.get_stock_day(name,'2000-01-01','2017-04-02')