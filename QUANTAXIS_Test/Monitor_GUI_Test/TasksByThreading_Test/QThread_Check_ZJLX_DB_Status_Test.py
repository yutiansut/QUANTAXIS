import unittest

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list
from QUANTAXIS.QAUtil import DATABASE


from QUANTAXIS.QAUtil import (DATABASE, QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_dict_remove_key,
                              QA_util_log_info, QA_util_code_tolist, QA_util_date_str2int, QA_util_date_int2str,
                              QA_util_sql_mongo_sort_DESCENDING,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse, QADate, QADate_trade)


from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_CheckZJLX_DB_Task import *
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list

class QThread_Check_ZJLX_Db_Status_Test(unittest.TestCase):

    def test_QA_count_eastmoney_stock_xjlc_record_count_by_aggregate(self):
        qthread = QThread_Check_ZJLX_DB_Status()
        qthread.QA_count_eastmoney_stock_xjlc_record_count_by_aggregate()

    def test_QThread_Check_ZJLX_DB_Count(self):
        qthread = QThread_Check_ZJLX_DB_Status()
        stockListAll = QA_fetch_stock_list()
        for iRec in stockListAll:
            stockCode = iRec['code']
            lstRet = qthread.QA_count_eastmoney_stock_xjlc_record_count_one_by_one(str_stock_code=stockCode)
            print(lstRet)

    def test_QThread_Check_ZJLX_DB_Recs(self):

        qthread = QThread_Check_ZJLX_DB_Status()

        #东方财富只提高近100天的数据
        #获取近100天的交易日段
        dateEnd = QADate.QA_util_date_today()
        dateEnd = QADate_trade.QA_util_get_real_date(dateEnd)
        dateStart = QADate_trade.QA_util_get_last_day(dateEnd,100)
        stockCode = '600004'

        #qthread.QA_fetch_eastmoney_stock_zjlx(strStockCode = stockCode, strStartDate = dateStart, strEndDate = dateEnd, strFormat='numpy')
        qthread.QA_fetch_eastmoney_stock_zjlx(str_stock_code=stockCode,strStartDate=dateStart, strEndDate=dateEnd)
        pass