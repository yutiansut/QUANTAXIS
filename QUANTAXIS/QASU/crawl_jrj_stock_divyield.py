
from QUANTAXIS.QAFetch.QAdivyield import *
from QUANTAXIS.QAUtil import (DATABASE,QA_util_getBetweenQuarter, QA_util_get_next_day,
                              QA_util_get_real_date, QA_util_log_info,QA_util_add_months,
                              QA_util_to_json_from_pandas, trade_date_sse,QA_util_today_str,
                              QA_util_datetime_to_strdate)
import pandas as pd
import pymongo

def QA_SU_save_stock_divyield_day(client=DATABASE, ui_log = None, ui_progress = None):
    '''
     save stock_day
    保存财报日历
    历史全部数据
    :return:
    '''
    END_DATE = QA_util_datetime_to_strdate(QA_util_add_months(QA_util_today_str(),-3))
    START_DATE = QA_util_datetime_to_strdate(QA_util_add_months(QA_util_today_str(),-12))

    date_list = list(pd.DataFrame.from_dict(QA_util_getBetweenQuarter(START_DATE,END_DATE)).T.iloc[:,1])
    stock_divyield = client.stock_divyield
    stock_divyield.create_index([("a_stockcode", pymongo.ASCENDING), ("dir_dcl_date", pymongo.ASCENDING)], unique=True)
    err = []

    def __saving_work(report_date, stock_divyield):
        try:
            QA_util_log_info(
                '##JOB01 Now Saving stock_divyield==== {}'.format(str(report_date)), ui_log)

            stock_divyield.insert_many(QA_util_to_json_from_pandas(
                QA_fetch_get_stock_divyield(report_date)), ordered=False)
        except Exception as error0:
            print(error0)
            err.append(str(report_date))

    for item in date_list:

        QA_util_log_info('The {} of Total {}'.format
                         ((date_list.index(item) +1), len(date_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {}'.format(str(float((date_list.index(item) +1) / len(date_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float((date_list.index(item) +1) / len(date_list) * 100))
        QA_util_log_info(strProgressToLog, ui_log= ui_log, ui_progress= ui_progress, ui_progress_int_value= intProgressToLog)

        __saving_work( item, stock_divyield)

    if len(err) < 1:
        QA_util_log_info('SUCCESS save stock divyield ^_^',  ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ',  ui_log)
        QA_util_log_info(err, ui_log)


def QA_SU_save_stock_divyield_his(client=DATABASE, ui_log = None, ui_progress = None):
    '''
    save stock_day
    保存财报日历
    反向查询四个季度财报
    :return:
    '''
    START_DATE = '2007-01-01'
    END_DATE = QA_util_datetime_to_strdate(QA_util_add_months(QA_util_today_str(),-3))
    date_list = list(pd.DataFrame.from_dict(QA_util_getBetweenQuarter(START_DATE,END_DATE)).T.iloc[:,1])
    stock_divyield = client.stock_divyield
    stock_divyield.create_index([("a_stockcode", pymongo.ASCENDING), ("report_date", pymongo.ASCENDING)], unique=True)
    err = []

    def __saving_work(report_date, stock_divyield):
        try:
            QA_util_log_info(
                '##JOB01 Now Saving stock_divyield==== {}'.format(str(report_date)), ui_log)
            stock_divyield.insert_many(QA_util_to_json_from_pandas(
                QA_fetch_get_stock_divyield(report_date)), ordered=False)
        except Exception as error0:
            print(error0)
            err.append(str(report_date))

    for item in date_list:
        QA_util_log_info('The {} of Total {}'.format
                         ((date_list.index(item) +1), len(date_list)))

        strProgressToLog = 'DOWNLOAD PROGRESS {}'.format(str(float((date_list.index(item) +1) / len(date_list) * 100))[0:4] + '%', ui_log)
        intProgressToLog = int(float((date_list.index(item) + 1)/ len(date_list) * 100))
        QA_util_log_info(strProgressToLog, ui_log= ui_log, ui_progress= ui_progress, ui_progress_int_value= intProgressToLog)

        __saving_work( item, stock_divyield)

    if len(err) < 1:
        QA_util_log_info('SUCCESS save stock divyield ^_^',  ui_log)
    else:
        QA_util_log_info(' ERROR CODE \n ',  ui_log)
        QA_util_log_info(err, ui_log)