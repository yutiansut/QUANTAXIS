import datetime
import unittest


from QUANTAXIS.QAFetch import (QATdx )
from QUANTAXIS.QAUtil import (QADate, QADate_trade )


class Test_QA_Date(unittest.TestCase):
    def test_QA_util(self):
        now = QADate.QA_util_time_now()
        today = QADate.QA_util_date_today()
        self.assertEquals(today.day, now.day)


