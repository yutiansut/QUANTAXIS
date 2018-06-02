# coding:utf-8
#
# The MIT License (MIT)
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Author:           604829050@qq.com
# Date:             2018-05-11
# Description:      Unit test for the fetch data

import unittest

from QUANTAXIS import *;
import tushare as QATs
#from QUANTAXIS.QASU.main import (QA_SU_save_stock_list)
from QUANTAXIS.QASU.main import (select_save_engine)



class Test_Query_Advance(unittest.TestCase):
    '''
    读取钱龙数据库进行比对
    '''

    def setUp(self):
        #self.stock_list = QA_fetch_stock_list_adv()
        #print(self.stock_list)

        #stock_list_items = [item for item in collections.find()];
        #if stock_list_items is None:
        #    print("💢 Error QA_fetch_stock_list_adv return None, maybe the DATABASE.stock_list have no DATA!")
        #    return None

        pass

    def tearDown(self):
        pass

    def test_QA_fetch_stock_min_adv(self):
        dataStruct = QA_fetch_stock_min_adv(start='2018-05-28 00:00:00',code = '300439')
        #dataStruct.show()
        pass

    def test_001(self):

        # print("-----------------------------------------------------------------------")
        # df = QATs.get_stock_basics()
        # print(df)
        # print("-----------------------------------------------------------------------")
        data = QA_fetch_get_stock_list(package = "tdx")
        # print(data)
        # print("-----------------------------------------------------------------------")

        engine = select_save_engine(engine="Tushare")
        engine.QA_SU_save_stock_list(client=DATABASE)

        # date = str(datetime.date.today())
        # date_stamp = QA_util_date_stamp(date)
        # print(data)
        # print(date_stamp)
        # #
        # client = DATABASE
        # coll = client.stock_list
        # coll.insert({'date': date, 'date_stamp': date_stamp,
        #              'stock': {'code': data}})
        #return list(df.index)
