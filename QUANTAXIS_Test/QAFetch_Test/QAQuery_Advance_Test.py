# coding:utf-8
#
# The MIT License (MIT)
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Author:           604829050@qq.com
# Date:             2018-06-05
# Description:      Unit test for the fetch data

import unittest

import fnmatch
import os
import time
import struct

import pathlib

import sqlite3



from QUANTAXIS import *;
import sqlite3
import tushare as QATs
#from QUANTAXIS.QASU.main import (QA_SU_save_stock_list)
from QUANTAXIS.QASU.main import (select_save_engine)



class Test_Query_Advance(unittest.TestCase):
    '''
    mac or linux 可以使用wine 来运行 ， 需要指定字符集防止乱码
    安装
    env LC_ALL=zh_CN.UTF-8 wine instjd_1000.exe
    运行
    env LC_ALL=zh_CN.UTF-8 wine ~/.wine/drive_c/qianlong/jindian/JD/JD.exe

    设置 钱龙金典 数据下载目录 http://download2.ql18.com.cn/download/software/instjd_1000.exe

    读取 钱龙软件   本地数据文件进行比对 ✅
    读取 同花顺软件  本地数据文件进行比对⭕️
    读取 通达信     本地数据文件进行比对⭕️

钱龙数据文件格式

    上海日线存储路径为:\ml30\data\shase\day,文件扩展名为:.day
    上海周线存储路径为:\ml30\data\shase\week,文件扩展名为: .wek
    上海月线存储路径为:\ml30\data\shase\month,文件扩展名为: .mnt
    深圳日线存储路径为:\ml30\data\sznse\day
    深圳周线存储路径为:\ml30\data\sznse\week
    深圳月线存储路径为:\ml30\data\sznse\month
    以深发展日线为例:
    1A76:0100 D6 CD 2F 01 52 07 01 00-52 07 01 00 52 07 01 00
    1A76:0110 52 07 01 00 86 0F 00 00-4D 02 00 00 00 00 00 00
    1A76:0120 00 00 00 00 00 00 00 00-D7 CD 2F 01 60 03 01 00
    1A76:0130 60 03 01 00 60 03 01 00-60 03 01 00 82 05 00 00
    1A76:0140 D4 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00

    每一条记录的长度为40字节:
    1-4字节为日期,D6 CD 2F 01转换为十进制是:19910102
    5-8字节为开盘价*1000
    9-12字节为最高价*1000
    13-16字节为最低价*1000
    17-20字节为收盘价*1000
    21-24字节为成交量(手)
    25-28字节为成交金额
    其余12字节未使用


通达信数据文件格式

    ？？

同花顺数据文件格式

    '''


    def parse_day_file_to_mysql_lite_db(self, day_file_path, db_file_save_dir, day_file):
        #time.sleep(1)
        file_size = os.path.getsize(day_file_path)
        assert((file_size % 40) == 0)
        #print(("%s 文件大小 %d Bytes"%(day_file_path, file_size)) + ("40Bytes/recrod, found %d records!"%(file_size / 40)))
        item_len = file_size // 40;

        db_file_save_file = db_file_save_dir
        db_file_save_file = db_file_save_file + "/" + day_file[0:6] + '.sqlite_db'
        conn = sqlite3.connect(db_file_save_file)
        c = conn.cursor()
        # Create table
        c.execute('''DROP TABLE IF EXISTS stocks''')
        c.execute('''CREATE TABLE stocks (date int, open_price real, high_price real, low_price real, close_price real, volumn real, amount real)''')


        # 钱龙只下载 800 天到历史数据记录， 经一步研究如何下载完整到数据
        with open(file=day_file_path, mode='rb') as f:
            #读取每条记录， 然后写到 mysql lite 数据库中
            for i in range(item_len):
                read_data_section = f.read(40)
                values = struct.unpack("<LLLLLLL",read_data_section[0:28])
                c.execute("INSERT INTO stocks(date,open_price,high_price,low_price,close_price,volumn,amount)  VALUES (%d,%f,%f,%f,%f,%d,%d)"
                          %(values[0], values[1]/1000, values[2]/1000, values[3]/1000, values[4]/1000,values[5],values[6]))
            f.closed
        conn.commit()
        c.close()
        conn.close()
        pass


    def setUp(self):

        #替换 运行环境下本地路径
        self.strQianLong_QLDATA_ = '/Users/jerryw/.wine/drive_c/qianlong/jindian/QLDATA/'


        isExists = os.path.exists(self.strQianLong_QLDATA_)
        if not isExists:
            print("🔍查找路径不存在 %s ⛔️"%self.strQianLong_QLDATA_)
            return


        self.strQianLong_SHASE_day    = self.strQianLong_QLDATA_ + ('history/SHASE/day/')
        self.strQianLong_SHASE_weight = self.strQianLong_QLDATA_ + ('history/SHASE/weight/')
        self.strQianLong_SHASE_nmn    = self.strQianLong_QLDATA_ + ('history/SHASE/nmn/')

        self.strQianLong_SZNSE_day    = self.strQianLong_QLDATA_ + ('history/SZNSE/day/')
        self.strQianLong_SZNSE_weight = self.strQianLong_QLDATA_ + ('history/SZNSE/weight/')
        self.strQianLong_SZNSE_nmn    = self.strQianLong_QLDATA_ + ('history/SZNSE/nmn/')

        #获取目录文件名，股票代码
        #读取数据
        #写到sqllite

        # current_dir = os.path.curdir
        # curdir= os.path.dirname(current_dir)
        #
        curdir = os.getcwd()
        print("📊准备写入📝db🗃文件到目录📂%s"%(curdir+"/data"))
        path_for_save_data = curdir + "/data"
        path_for_save_data = path_for_save_data.rstrip("\\")
        isExists = os.path.exists(path_for_save_data)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path_for_save_data)

            print(path_for_save_data + ' 创建成功😊')
            #return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path_for_save_data + ' 目录已存在😅')
            #return False

        # path1.mkdir()
        # bExist = pathlib.Path.exists(path1)
        # assert(bExist)
        #os.path(curdir+"/data")

        stock_count = len(os.listdir(self.strQianLong_SHASE_day))
        iCount = 0
        for day_file in os.listdir(self.strQianLong_SHASE_day):

            iii = round((iCount / stock_count) * 100.0)
            s1 = "\r🐌读取股票数据%s %d%%[%s%s]" % (day_file, iii, "*" * iii, " " * (100 - iii))
            sys.stdout.write(s1)
            sys.stdout.flush()

            if fnmatch.fnmatch(day_file, '*.day'):
                fullPathFileName = self.strQianLong_SHASE_day + day_file
                #print("解析文件 ", fullPathFileName)
                self.parse_day_file_to_mysql_lite_db(fullPathFileName, path_for_save_data, day_file)

                iCount = iCount + 1
        print("\n😇读取数据完成")
        pass

    def tearDown(self):

        pass

    def test_QA_fetch_stock_min_adv(self):
        # dataStruct = QA_fetch_stock_min_adv(start='2018-05-28 00:00:00',code = '300439')
        # print("获取1分钟数据")
        # print(dataStruct)
        # #dataStruct.show()
        pass

    #def test_001(self):
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


'''
'''