# coding:utf-8

import sys
import typing
import unittest
sys.path.append('c:\\quantaxis')
import QAFetch


class QAFetchTest(unittest.TestCase):
    def test_trade_date(self):
        data=QAFetch.get_trade_date("2005-01-01","SSE")
        self.assertTrue(list(data))
    def test_get_stock_day(self):
        data=QAFetch.get_stock_day("000001.SZ","2009-01-01","2017-01-01")
        self.assertTrue(list(data))
    


if __name__ == '__main__':
  unittest.main()