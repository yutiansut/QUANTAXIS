# -*- coding: utf-8 -*-
""" test QAIndicatorStuct
"""
from unittest import TestCase
import unittest
#  import datetime
import QUANTAXIS as qa
from QUANTAXIS.QAUtil.QACache import QA_util_cache as qacache
#  import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


class testQAIndicatorStuct(unittest.TestCase):
    """"""
    def test_get_timerange(self):
        """测试QA_DataStruct_Indicators.get_timerange((self, start, end, code=None)
        code为空时，是否返回日期段内所有的数据"""
        num = 50
        # codelist = self.getCodeList(count=num)
        codelist = self.getCodeList(count=num, isTesting=False)
        startdate = datetime.strptime('2017-08-01', '%Y-%m-%d')
        endday = '2018-10-21'
        data = qa.QA_fetch_stock_day_adv(codelist, '2017-08-01', '2018-10-21').to_qfq()
        ind = data.add_func(qa.QA_indicator_MA, 10)
        inc = qa.QA_DataStruct_Indicators(ind)
        startdate, enddate = '2018-08-01', '2018-08-31'
        #  相同时间段数据对比
        dftest = self.getTimeRange(inc, startdate, enddate, isUsingQA=False)
        dforgin = inc.get_timerange(startdate, enddate)
        self.assertTrue(dftest.equals(dforgin) , "两种计算方式结果应该一致。\n{} {}".format(dftest.tail(), dforgin.tail()))


    def getTimeRange(self, inc, startdate, enddate, code=None, isUsingQA=False):
        if isUsingQA:
            # 源码中bug修复时，使用以下代码
            dfindicator = inc.get_timerange(startdate, enddate, code)  # QAUANTAXIS源码中有bug，code不起作用

        else:
            # 源码中bug未修复时，使用以下代码
            if code is None:  # QAUANTAXIS源码中有bug，code为空时，不返回数据
                dfindicator = inc.data.loc[(slice(pd.Timestamp(startdate),
                                                  pd.Timestamp(self.str2date(enddate)))), :]
            else:
                dfindicator = inc.data.loc[(slice(pd.Timestamp(startdate),
                                                  pd.Timestamp(self.str2date(enddate))), code),
                              :]
        return dfindicator

    def str2date(self, dayStr):
        if isinstance(dayStr, str):
            return datetime.strptime(dayStr, '%Y-%m-%d')
        else:
            return dayStr

    def getCodeList(self, isTesting=True, count=5000):
        """
        isTesting: 是否使用测试数据
        count： 返回最多结果集数量
        """
        if isTesting:
            # 2018.8首板个股，测试用，减少调试时间
            codelist = ['000023', '000068', '000407', '000561', '000590', '000593', '000608', '000610', '000626',
                        '000638',
                        '000657', '000659', '000663', '000669', '000677', '000705', '000759', '000766', '000780',
                        '000792',
                        '000815', '000852', '000885', '000909', '000913', '000921', '000928', '000931', '002006',
                        '002012',
                        '002034']
        else:
            codelist = qa.QA_fetch_stock_list_adv().code.tolist()
        return codelist[:count]

if __name__ == '__main__':
    unittest.main()
