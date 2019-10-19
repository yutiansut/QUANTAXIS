import unittest
import pprint

from QUANTAXIS import QUANTAXIS as QA
from QUANTAXIS.QAUtil.QADate import *
from QUANTAXIS.QAUtil.QADate_trade import *

from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_option_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_M_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_SR_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_CU_contract_time_to_market)

from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_C_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_CF_contract_time_to_market)
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_commodity_option_RU_contract_time_to_market)


from QUANTAXIS.QASU.main import *

import numpy as np
import pandas as pd

class TestOptionData(unittest.TestCase):

    def testQA_SU_save_stock_day(self):
        QA_SU_save_option_50etf_day('tdx')

    def testGetOptionMin(self):
        #
        # 去掉商品期权，保留510050开头的50ETF期权
        rows = QA_fetch_get_option_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            # print(aRow)
            print(aRow.code);
            result2 = QA.QA_fetch_get_option_min(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);
        #

    def testGetOptionList(self):
        #
        # 去掉商品期权，保留510050开头的50ETF期权
        rows = QA_fetch_get_option_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            #print(aRow)
            print(aRow.code);
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);
        #
        #pprint.pprint(result)
        #strToday = QA_util_today_str();
        #result2 = QA.QA_fetch_get_option_day(package='tdx', code='10001214', start=strToday, end=strToday)
        #pprint.pprint(result2)

    def testGetCommodityCuOptionList(self):
        rows = QA_fetch_get_commodity_option_CU_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            #print(aRow)
            print("准备获取 ；-》")
            print(aRow)
            print("-------------")
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);



            print("结束获取 ；-》")

    def testGetCommodityRUOptionList(self):
        rows = QA_fetch_get_commodity_option_RU_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            # print(aRow)
            print("准备获取 ；-》")
            print(aRow)
            print("-------------")
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);

            print("结束获取 ；-》")

    def testGetCommodityCOptionList(self):
        rows = QA_fetch_get_commodity_option_C_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            # print(aRow)
            print("准备获取 ；-》")
            print(aRow)
            print("-------------")
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);
            time.sleep(1)

            print("结束获取 ；-》")

    def testGetCommodityCFOptionList(self):
        rows = QA_fetch_get_commodity_option_CF_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            # print(aRow)
            print("准备获取 ；-》")
            print(aRow)
            print("-------------")
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);

            print("结束获取 ；-》")


    def testGetCommoditySROptionList(self):
        rows = QA_fetch_get_commodity_option_SR_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            #print(aRow)
            print("准备获取 ；-》")
            print(aRow)
            print("-------------")
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);



            print("结束获取 ；-》")



    def testGetCommodityMOptionList(self):
        rows = QA_fetch_get_commodity_option_M_contract_time_to_market()
        strToday = QA_util_today_str()
        for aRow in rows:
            #print(aRow)
            print("准备获取 ；-》")
            print(aRow)
            print("-------------")
            result2 = QA.QA_fetch_get_option_day(package='tdx', code=aRow.code, start='2018-01-01', end=strToday)
            pprint.pprint(result2);



            print("结束获取 ；-》")


    def setUp(self):
        pass

    def tearDown(self):
        pass
