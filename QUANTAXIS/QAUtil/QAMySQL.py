

from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_stock_list_adv, QA_fetch_stock_block_adv,
                                               QA_fetch_stock_day_adv, QA_fetch_financial_report_adv
,QA_fetch_stock_financial_calendar_adv,QA_fetch_stock_divyield_adv)

from QUANTAXIS.QAFetch.QAQuery import ( QA_fetch_stock_basic_info_tushare, QA_fetch_stock_xdxr)

from QUANTAXIS.QAUtil.QASql import QA_util_sql_store_mysql
from QUANTAXIS.QAUtil.QAEtl import QA_util_process_financial

import pandas as pd
import datetime


def QA_etl_stock_list():
    QA_util_sql_store_mysql(QA_fetch_stock_list_adv().reset_index(drop=True), "stock_list",if_exists='replace')

def QA_etl_stock_info():
    data = pd.DataFrame(QA_fetch_stock_basic_info_tushare())
    data = data.drop("_id", axis=1)
    QA_util_sql_store_mysql(data, "stock_info",if_exists='replace')

def QA_etl_stock_xdxr(type = "day", mark_day = str(datetime.date.today())):
    if type == "all":
        data = QA_fetch_stock_xdxr(list(QA_fetch_stock_list_adv()['code'])).reset_index(drop=True).fillna(0)
        QA_util_sql_store_mysql(data, "stock_xdxr",if_exists='replace')
    elif type == "day":
        data = QA_fetch_stock_xdxr(list(QA_fetch_stock_list_adv()['code']), mark_day)
        if data is None:
            print("We have no XDXR data for the day {}".format(str(datetime.date.today())))
        else:
            data = data.reset_index(drop=True).fillna(0)
            QA_util_sql_store_mysql(data, "stock_xdxr",if_exists='append')

def QA_etl_stock_day(type = "day", mark_day = str(datetime.date.today())):
    if type == "all":
        data = QA_fetch_stock_day_adv(list(QA_fetch_stock_list_adv()['code'])).data.reset_index()
        QA_util_sql_store_mysql(data, "stock_market_day",if_exists='replace')
    elif type == "day":
        data = QA_fetch_stock_day_adv(list(QA_fetch_stock_list_adv()['code']), mark_day)
        if data is None:
            print("We have no MARKET data for the day {}".format(str(datetime.date.today())))
        else:
            data = data.data.reset_index()
            QA_util_sql_store_mysql(data, "stock_market_day",if_exists='append')

def QA_etl_stock_financial(type = "all", mark_day = str(datetime.date.today())):
    if type == 'all':
        data = QA_fetch_financial_report_adv(list(QA_fetch_stock_list_adv()['code']),'1990-01-01',end=datetime.date.today()).data.reset_index(drop=True).drop("_id",1).fillna(0)
        QA_util_sql_store_mysql(data, "stock_financial",if_exists='replace')
    else:
        raise DeprecationWarning('你的代码有点问题 我删掉了这部分')


def QA_etl_stock_calendar(type = "day", mark_day = str(datetime.date.today())):
    if type == "all":
        data = QA_fetch_stock_financial_calendar_adv(list(QA_fetch_stock_list_adv()['code'])).data.reset_index(drop=True)
        QA_util_sql_store_mysql(data, "stock_calendar",if_exists='replace')
    elif type == "day":
        data = QA_fetch_stock_financial_calendar_adv(list(QA_fetch_stock_list_adv()['code']), mark_day).data
        if data is None:
            print("We have no calendar data for the day {}".format(str(datetime.date.today())))
        else:
            data = data.reset_index(drop=True)
            QA_util_sql_store_mysql(data, "stock_calendar",if_exists='append')

def QA_etl_stock_block():
    data = QA_fetch_stock_block_adv(list(QA_fetch_stock_list_adv()['code'])).data.reset_index()
    QA_util_sql_store_mysql(data, "stock_block",if_exists='replace')

def QA_etl_stock_divyield(type = "day", mark_day = str(datetime.date.today())):
    if type == "all":
        data = QA_fetch_stock_divyield_adv(list(QA_fetch_stock_list_adv()['code'])).data.reset_index()
        QA_util_sql_store_mysql(data, "stock_divyield",if_exists='replace')
    elif type == "day":
        data = QA_fetch_stock_divyield_adv(list(QA_fetch_stock_list_adv()['code']), mark_day).data
        if data is None:
            print("We have no Divyield data for the day {}".format(str(datetime.date.today())))
        else:
            data = data.reset_index()
            QA_util_sql_store_mysql(data, "stock_divyield",if_exists='append')

def QA_etl_process_financial_day(type = "all"):
    if type == "all":
        QA_util_process_financial(str(datetime.date.today()))
    elif type == "financial":
        QA_util_process_financial(str(datetime.date.today()),type == "financial")
    elif type == "analysis":
        QA_util_process_financial(str(datetime.date.today()),type == "analysis")