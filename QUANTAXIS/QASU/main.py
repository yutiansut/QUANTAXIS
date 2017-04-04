from . import save_tushare as sts
from . import save_wind as sw
from . import update_tushare as uts
from . import update_wind as uw


def save_stock_list():
    sw.save_stock_list()

def save_trade_date():
    sw.save_trade_date()

def save_stock_day(name,startDate,endDate):
    sw.save_stock_day(name,startDate,endDate)

def save_stock_day_init():
    sw.save_stock_day_init()