# coding:utf-8

import sys
sys.path.append('c:\\quantaxis')
import QAFetch
import unittest



class QAFetchTest(unittest.TestCase):
    def test_trade_date(self):
        data=QAFetch.get_trade_date('wind',"2005-01-01","SSE")
        print(data)
        self.assertTrue(list(data))
    def test_get_stock_day(self):
        data=QAFetch.get_stock_day('ts',"000001.SZ","2009-01-01","2017-01-01")
        self.assertTrue(list(data))
        print(data)


if __name__ == '__main__':
  unittest.main()