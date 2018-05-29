import unittest

import sys
import time

#from QUANTAXIS.QAFetch import (QATdx );
from QUANTAXIS.QAUtil import (QADate, QADate_trade );

#from pandas import Series
import pandas as pd
import matplotlib as mpl


class Test_QA_None(unittest.TestCase):


    def fab(self,max):
        n, a, b = 0, 0, 1
        while n < max:
            print (b)
            a, b = b, a + b
            n = n + 1

    def test_Generator(self):
        self.fab(10)

    def test_None(self):

        print("----------------------------")
        obj = pd.Series([3,4,-2,2])
        print(obj)


        pd.Series([1, 23, 4]).plot()

        #now = QADate.QA_util_time_now()
        #print( type(now) )

        #today = QADate.QA_util_date_today()
        #print( type(today))

        #print("okok---> do the task")

        # for i in range(101):
        #     s1 = "\r%d%%[%s%s]" % (i, "*" * i, " " * (100 - i))
        #     time.sleep(1)
        #     sys.stdout.write(s1)
        #     sys.stdout.flush()
        # pass


