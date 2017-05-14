from . import save_tushare as sts
from . import save_wind as sw
from . import update_tushare as uts
from . import update_wind as uw


def QA_SU_save_stock_list(engine,client):
    engine=select_engine(engine)
    engine.QA_SU_save_stock_list(client)

def QA_SU_save_trade_date(engine,client):
    engine=select_engine(engine)
    engine.QA_SU_save_trade_date(client)
def QA_SU_save_stock_info(engine,client):
    engine=select_engine(engine)
    engine.QA_SU_save_stock_info(client)
def QA_SU_save_stock_day(name, startDate, endDate, engine, client):
    engine=select_engine(engine)
    engine.QA_SU_save_stock_day(name, startDate, endDate, client)

def QA_SU_save_stock_day_init(startDate,engine,client):
    engine=select_engine(engine)
    engine.QA_SU_save_stock_day_init(startDate,client)


def QA_SU_update_stock_day( engine, client):
    engine=select_update_engine(engine)
    engine.QA_update_stock_day_all('code',client)

def select_engine(engine):
    if engine in ['wind','Wind','WIND']:
       return sw
    elif engine in ['tushare','ts','Tushare']:
       return sts

def select_update_engine(engine):
    if engine in ['wind','Wind','WIND']:
       return uw
    elif engine in ['tushare','ts','Tushare']:
       return uts

