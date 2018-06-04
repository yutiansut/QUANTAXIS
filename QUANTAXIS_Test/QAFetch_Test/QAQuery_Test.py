
import unittest

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_basic_info_tushare


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
