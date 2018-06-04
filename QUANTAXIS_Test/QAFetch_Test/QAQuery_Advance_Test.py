# coding:utf-8
#
# The MIT License (MIT)
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Author:           604829050@qq.com
# Date:             2018-05-11
# Description:      Unit test for the fetch data

import unittest

import fnmatch
import os


from QUANTAXIS import *;
import sqlite3
import tushare as QATs
#from QUANTAXIS.QASU.main import (QA_SU_save_stock_list)
from QUANTAXIS.QASU.main import (select_save_engine)



class Test_Query_Advance(unittest.TestCase):
    '''
    清洗数据。

    # 读取钱龙数据库 ,
    # 存取数据到 SQLite


    # 🛠 todo
    读取同花顺数据库进行比对
    读取通达信数据库进行比对


    '''

    def setUp(self):
        #
        # mac or linux 可以使用wine 来运行 ， 需要指定字符集防止乱码
        # env LC_ALL=zh_CN.UTF-8 wine instjd_1000.exe
        #
        #设置 钱龙金典 数据下载目录 http://download2.ql18.com.cn/download/software/instjd_1000.exe
        self.strQianLong_QLDATA_ = '/Users/jerryw/.wine/drive_c/qianlong/jindian/QLDATA'

        self.strQianLong_SHASE_day    = self.strQianLong_QLDATA_ + ('/history/SHASE/day')
        self.strQianLong_SHASE_weight = self.strQianLong_QLDATA_ + ('/history/SHASE/weight')
        self.strQianLong_SHASE_nmn    = self.strQianLong_QLDATA_ + ('/history/SHASE/nmn')

        self.strQianLong_SZNSE_day    = self.strQianLong_QLDATA_ + ('/history/SZNSE/day')
        self.strQianLong_SZNSE_weight = self.strQianLong_QLDATA_ + ('/history/SZNSE/weight')
        self.strQianLong_SZNSE_nmn    = self.strQianLong_QLDATA_ + ('/history/SZNSE/nmn')

        #获取目录文件名，股票代码
        #读取数据
        #写到sqllite

        for file in os.listdir(self.strQianLong_SHASE_day):
            if fnmatch.fnmatch(file, '*.day'):
                print(file)
                
        print(" ")

        pass

    def tearDown(self):

        pass

    def test_QA_fetch_stock_min_adv(self):
        # dataStruct = QA_fetch_stock_min_adv(start='2018-05-28 00:00:00',code = '300439')
        # print("获取1分钟数据")
        # print(dataStruct)
        # #dataStruct.show()
        pass

    def test_001(self):

        # print("-----------------------------------------------------------------------")
        # df = QATs.get_stock_basics()
        # print(df)
        # print("-----------------------------------------------------------------------")
        #data = QA_fetch_get_stock_list(package = "tdx")
        # print(data)
        # print("-----------------------------------------------------------------------")

        #engine = select_save_engine(engine="Tushare")
        #engine.QA_SU_save_stock_list(client=DATABASE)

        # date = str(datetime.date.today())
        # date_stamp = QA_util_date_stamp(date)
        # print(data)
        # print(date_stamp)
        # #
        # client = DATABASE
        # coll = client.stock_list
        # coll.insert({'date': date, 'date_stamp': date_stamp,
        #              'stock': {'code': data}})
        #return list(df.index)
        pass