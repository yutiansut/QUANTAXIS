import unittest

import QUANTAXIS as QA


class QABacktestSimple_Test(unittest.TestCase):

    def setUp(self):
        #准备数据
        code = '300439'
        start = '2017-01-01'
        end = '2018-01-01'

        stock_data_300439_2017 = QA.QA_fetch_stock_day_adv(code, start, end).to_qfq()
        print(stock_data_300439_2017)
        print(len(stock_data_300439_2017))

    def test_simpleQABacktest(self):
        pass
