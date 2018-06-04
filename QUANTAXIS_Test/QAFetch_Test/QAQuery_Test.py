
import unittest

from  QUANTAXIS.QAFetch.QAQuery import (QA_fetch_stock_basic_info_tushare, QA_fetch_stock_to_market_date)
from  QUANTAXIS.QASU.save_to_db_fields_description import quantaxis__db_description


class QAQuery_test(unittest.TestCase):
    def test_QA_fetch_stock_basic_info_tusare(self):
        items = QA_fetch_stock_basic_info_tushare()
        print(type(items))
        print(len(items))
        print("查找 半导体 主营的 股票：")
        # print(items)
        for i in items:
            # print(i)
            if i['industry'] == '半导体':
                print(i)

    def test_QA_fetch_stock_to_market_date(self):
        to_market_date = QA_fetch_stock_to_market_date(stock_code='300439')
        print(to_market_date)
        self.assertEqual(to_market_date,'2015-05-15')


    def test_quantaxis__db_description(self):

        print(quantaxis__db_description)
