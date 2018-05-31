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


class Test_Query_Advance(unittest.TestCase):
    def test_QA_fetch_stock_min_adv(self):

        dataStruct = QA_fetch_stock_min_adv(start='2018-05-28 00:00:00',code = '300439')
        #dataStruct.show()

        pass