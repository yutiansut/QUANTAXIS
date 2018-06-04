import datetime
import unittest

from QUANTAXIS.QAFetch import QATdx
from QUANTAXIS.QAUtil import QADate, QADate_trade


class Test_QA_Date_trade(unittest.TestCase):
    def test_QA_util_if_trade(self):

        now = QADate.QA_util_time_now()
        str_from_today = '%04d-%02d-%02d' % (now.year, now.month, now.day)

        nDayLeft = 1000
        while nDayLeft > 0:

            toDayIsTradeDay = QADate_trade.QA_util_if_trade(str_from_today)
            realTradeDay = QADate_trade.QA_util_get_real_date(str_from_today)

            QADate.QA_util_date_valid(realTradeDay)

            if toDayIsTradeDay == False:
                prev_trade_day = QADate_trade.QA_util_get_last_day(
                    str_from_today, -1)
                realTradeDay = QADate_trade.QA_util_get_real_date(
                    prev_trade_day)
                self.assertEquals(realTradeDay, toDayIsTradeDay)
            else:
                self.assertEquals(realTradeDay, realTradeDay)

            str_from_today = QADate_trade.QA_util_get_last_day(str_from_today)
            nDayLeft = nDayLeft - 1

        print("okok")
