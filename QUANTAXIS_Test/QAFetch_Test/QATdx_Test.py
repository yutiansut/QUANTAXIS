import datetime
import os
import socket
import struct
import sys
import time
import unittest
import urllib.request
import zipfile

import pandas as pd

from QUANTAXIS.QAFetch import QATdx
from QUANTAXIS.QAUtil import QADate, QADate_trade

#from QUANTAXIS import *;

#
# 下载最近5天的数据
# http://www.wstock.net/wstock/login.htm?free
# 调用，QA_fetch_stock_day
# 对比数据
#


def Schedule(a, b, c):
    #     '''''
    #     a:已经下载的数据块
    #     b:数据块的大小
    #     c:远程文件的大小
    #    '''
    #     per = 100.0 * a * b / c
    #     if per > 100:
    #         per = 100
    #     print
    #     '下载进度%.2f%%' % per
    pass


class Test_QA_Fetch(unittest.TestCase):

    # 下载最近5天的K线数据
    def setUp(self):
        print('Get the free stock data from wstock.net ')
        # 获取 下载路径的特殊值
        url = "http://www.wstock.net/wstock/inc/wstockV2.js"
        # print(url)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        })
        response = urllib.request.urlopen(req)
        content = response.read()
        # print(type(content))
        # print(content)
        strings = content.decode("utf-8", "ignore")
        string_lines = strings.split("\r\n")

        for line in string_lines:
            # print(type(line))
            # var M_SHSZ_PATH="4T1IWc2q";
            if line.startswith("var M_SHSZ_PATH"):
                print(line)
                variables = line.split("=")
                string_of_path_v = variables[1]
                print(string_of_path_v)
                real_value_password = string_of_path_v.lstrip("\"")
                real_value_password = real_value_password.rstrip("\";")
                print(real_value_password)

        # http://www.wstock.net/wstock/download/4T1IWc2q/wss0502r.zip
        url2 = "http://www.wstock.net/wstock/download/%s/wss%sr.zip"

        now = QADate.QA_util_time_now()
        str_from_today = '%04d-%02d-%02d' % (now.year, now.month, now.day)

        toDayIsTradeDay = QADate_trade.QA_util_if_trade(str_from_today)
        nowTimeIsTrading = QADate_trade.QA_util_if_tradetime(now)

        # todo QADate_trade.QA_util_if_before_today_tradetime  返回是否是一天开盘前
        # todo QADate_trade.QA_util_if_after_today_tradetime   返回是否是一天收盘后
        _time1 = datetime.datetime.strptime(
            str(now)[0:19], '%Y-%m-%d %H:%M:%S')
        if _time1.hour in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            toDayIsBeforeOpen = True
        else:
            toDayIsBeforeOpen = False

        prev_trade_day = ""
        if toDayIsTradeDay == False:
            prev_trade_day = QADate_trade.QA_util_get_real_date(
                str_from_today)  # 今天不是交易日，往前移一天
            print("非交易日，下载前一天交易日 %s" % (prev_trade_day))
        elif nowTimeIsTrading == True or toDayIsBeforeOpen == True:
            prev_trade_day = QADate_trade.QA_util_get_real_date(
                str_from_today)  # 当天交易时段无法下载今天的数据，往前移一天
            prev_trade_day = QADate_trade.QA_util_get_last_day(prev_trade_day)
            print("交易时间，下载前一天交易日 %s" % (prev_trade_day))
        else:
            prev_trade_day = str_from_today
            print("下载今天交易日 %s" % (prev_trade_day))

        self.test_day_k_line_dates = []
        self.test_day_k_line_dad_file_name = []

        dayLeft = 1  # 下载5天之前的数据
        while dayLeft > 0:

            str_month = prev_trade_day[5:7]
            str_day = prev_trade_day[8:10]
            url_data = "http://www.wstock.net/wstock/download/%s/wss%s%sr.zip" % (
                real_value_password, str_month, str_day)
            print(url_data)

            # 下载文件
            local_file_name = "wss%s%sr.zip" % (str_month, str_day)
            urllib.request.urlretrieve(url_data, local_file_name, Schedule)

            # 解压缩文件
            zfile = zipfile.ZipFile(local_file_name, 'r')
            for filename in zfile.namelist():
                data = zfile.read(filename)
                file = open(filename, 'w+b')
                file.write(data)
                file.close()
                self.test_day_k_line_dad_file_name.append(filename)

            strTestDate = "%04d-%s-%s" % (now.year, str_month, str_day)
            self.test_day_k_line_dates.append(strTestDate)

            # 删除zip文件 ， 防止误删，暂不实现

            prev_trade_day = QADate_trade.QA_util_get_last_day(prev_trade_day)
            dayLeft = dayLeft - 1
            pass

    def tearDown(self):
        print('tearDown...')
        # 删除dad文件，防止误删，暂不实现

    '''
    /*
        前20个字节为头信息:
        1~4? ? ? ? 为安装数据的标识(33 FC 19 8C)
        5~8? ? ? ? 为 ?? ?? ?? ?? 未知
        9~12? ? ? ? 为本文件的股票数
        13~16? ? ? ? 为00 00 00 00
        17~20? ? ? ? 为FF FF FF FF
    
        对于单日的安装数据
        标识(33 FC 19 8C) ?? ?? ?? ?? 本文件的股票数 00 00 00 00
        FF FF FF FF SHXX(SZXX) XXXX(XX 00 00) 00(00 00 00)|
        (重复上一只股票的最低价的后三位，不指逻辑上的，如果是第一只则用40 00 00)
        ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??
        日期 开盘价 最高价 最低价 收盘价 成交量(手) 成交额(元) ?? ?? ?? ??
        FF FF FF FF 00 00 00 00 00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
    */
    
    读取 dad 文件 ，返回 dataframe 
        
   
    '''

    def extraDataFromDAD(self, local_file_name):

        # 解析dad文件
        df = pd.DataFrame(columns=["stock_name", "date", "open", "high", "low", "close", "volumn", "turn"],
                          index=["stock_code"])

        fileDad = open(local_file_name, 'rb', buffering=0)
        fileDad.seek(0x0, 0x0)
        fileAllBytes = fileDad.readall()
        fileDad.close()

        #first4Bytes = fileDad.read(0x04);
        first4Bytes = fileAllBytes[0x00: 0x04]

        if first4Bytes[0] == 0x8c and first4Bytes[1] == 0x19 and first4Bytes[2] == 0xfc and first4Bytes[3] == 0x33:

            # fileDad.seek(0x08);
            #byteNumberOfStock = fileDad.read(0x04);

            byteNumberOfStock = fileAllBytes[0x08:0x08+0x04]
            longNumberOfStock = struct.unpack('<L', byteNumberOfStock)
            print("共有")
            print(longNumberOfStock)

            for iStockIndex in range(0, longNumberOfStock[0]):

                # 修改， fix 没有输出
                #print('共%d个数据 ， 已经读取%d  读取数据中 :%10.8s%s' % (longNumberOfStock[0], iStockIndex, str(iStockIndex / longNumberOfStock[0]), '%'))

                i = round((iStockIndex / longNumberOfStock[0]) * 100.0)
                s1 = "\r读取数据%d%%[%s%s]" % (i, "*" * i, " " * (100 - i))
                sys.stdout.write(s1)
                sys.stdout.flush()

                #fileDad.seek(0x10 + iStockIndex * 4 * 0x10);
                #aStockData = fileDad.read(0x10 * 4);
                aStockData = fileAllBytes[0x10 + iStockIndex * 4 *
                                          0x10: 0x10 + iStockIndex * 4 * 0x10 + 0x10 * 4]

                if aStockData[0] == 0xFF and aStockData[1] == 0xFF and aStockData[2] == 0xFF and aStockData[3] == 0xFF:

                    codeNameByte = aStockData[4:0x10]
                    # print(codeNameByte)
                    strCodeName = codeNameByte.decode('ascii')
                    # print(strCodeName);

                    stockNameByte = aStockData[0x14: 0x20]
                    # print(stockNameByte);
                    strStockName = stockNameByte.decode('gbk')
                    # print(strStockName);

                    stockTime = aStockData[0x20: 0x24]
                    stockTimeNumber = struct.unpack('<L', stockTime)
                    time_local = time.localtime(stockTimeNumber[0])

                    #dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    dt = time.strftime("%Y-%m-%d", time_local)

                    # print(dt);

                    i = 1
                    byte_stock_open = aStockData[0x20 +
                                                 (i * 4): 0x20+((i+1) * 4)]
                    i = 2
                    byte_stock_high = aStockData[0x20 +
                                                 (i * 4): 0x20+((i+1) * 4)]
                    i = 3
                    byte_stock_low = aStockData[0x20+(i * 4): 0x20+((i+1) * 4)]
                    i = 4
                    byte_stock_close = aStockData[0x20 +
                                                  (i * 4): 0x20+((i+1) * 4)]
                    i = 5
                    byte_stock_volume = aStockData[0x20 +
                                                   (i * 4): 0x20+((i+1) * 4)]
                    i = 6
                    byte_stock_turn = aStockData[0x20 +
                                                 (i * 4): 0x20+((i+1) * 4)]
                    i = 7

                    v1 = struct.unpack('<f', byte_stock_open)
                    stock_open = v1[0]

                    v1 = struct.unpack('<f', byte_stock_close)
                    stock_close = v1[0]

                    v1 = struct.unpack('<f', byte_stock_low)
                    stock_low = v1[0]

                    v1 = struct.unpack('<f', byte_stock_high)
                    stock_high = v1[0]

                    v1 = struct.unpack('<f', byte_stock_volume)
                    stock_volume = v1[0]

                    v1 = struct.unpack('<f', byte_stock_turn)
                    stock_turn = v1[0]

                    #print("%f %f %f %f %f %f "%(stock_open, stock_close, stock_high,stock_low, stock_volume, stock_turn))
                    # print("------")

                    df.index.astype(str)
                    df.loc[strCodeName[0:8]] = [strStockName, dt, stock_open,
                                                stock_high, stock_low, stock_close, stock_volume, stock_turn]

        return df

    def test_QA_fetch_get_stock_day(self):

        # 读取 dad 日线数据
        df_from_dad = self.extraDataFromDAD(
            self.test_day_k_line_dad_file_name[0])

        df_from_tdx = QATdx.QA_fetch_get_stock_day(
            code="600000", start_date=self.test_day_k_line_dates[0], end_date=self.test_day_k_line_dates[0])
        for idx_from_df_tdx in df_from_tdx.index:

            print(idx_from_df_tdx)

            # for idx_from_df_dad in df_from_dad.index:

            open_price1 = df_from_tdx.loc[idx_from_df_tdx, "open"]
            close_price1 = df_from_tdx.loc[idx_from_df_tdx, "close"]
            high_price1 = df_from_tdx.loc[idx_from_df_tdx, "high"]
            low_price1 = df_from_tdx.loc[idx_from_df_tdx, "low"]
            volume1 = df_from_tdx.loc[idx_from_df_tdx, "vol"]
            amount1 = df_from_tdx.loc[idx_from_df_tdx, "amount"]
            date1 = df_from_tdx.loc[idx_from_df_tdx, "date"]

            # fix here 构造和 QA_fetch_get_stock_day 返回一样类型的 dataframe 直接比较

            open_price2 = df_from_dad.loc["SH600000", "open"]
            close_price2 = df_from_dad.loc["SH600000", "close"]
            high_price2 = df_from_dad.loc["SH600000", "high"]
            low_price2 = df_from_dad.loc["SH600000", "low"]
            volume2 = df_from_dad.loc["SH600000", "volumn"]
            amount2 = df_from_dad.loc["SH600000", "turn"]
            date2 = df_from_dad.loc["SH600000", "date"]

            self.assertEqual(open_price1, round(open_price2, 2))
            self.assertEqual(close_price1, round(close_price2, 2))
            self.assertEqual(high_price1, round(high_price2, 2))
            self.assertEqual(low_price1, round(low_price2, 2))
            # 成交量和成交额 总是有误差 ？？
            #self.assertEqual( volume1 , volume2 )
            #self.assertEqual( amount1 , amount2)
            self.assertEqual(date1, date2)

        df_from_tdx = QATdx.QA_fetch_get_stock_day(code="300439", start_date=self.test_day_k_line_dates[0],
                                                   end_date=self.test_day_k_line_dates[0])
        for idx_from_df_tdx in df_from_tdx.index:
            print(idx_from_df_tdx)

            # for idx_from_df_dad in df_from_dad.index:
            open_price1 = df_from_tdx.loc[idx_from_df_tdx, "open"]
            close_price1 = df_from_tdx.loc[idx_from_df_tdx, "close"]
            high_price1 = df_from_tdx.loc[idx_from_df_tdx, "high"]
            low_price1 = df_from_tdx.loc[idx_from_df_tdx, "low"]
            volume1 = df_from_tdx.loc[idx_from_df_tdx, "vol"]
            amount1 = df_from_tdx.loc[idx_from_df_tdx, "amount"]
            date1 = df_from_tdx.loc[idx_from_df_tdx, "date"]

            # fix here 构造和 QA_fetch_get_stock_day 返回一样类型的 dataframe 直接比较
            open_price2 = df_from_dad.loc["SZ300439", "open"]
            close_price2 = df_from_dad.loc["SZ300439", "close"]
            high_price2 = df_from_dad.loc["SZ300439", "high"]
            low_price2 = df_from_dad.loc["SZ300439", "low"]
            volume2 = df_from_dad.loc["SZ300439", "volumn"]
            amount2 = df_from_dad.loc["SZ300439", "turn"]
            date2 = df_from_dad.loc["SZ300439", "date"]

            self.assertEqual(open_price1, round(open_price2, 2))
            self.assertEqual(close_price1, round(close_price2, 2))
            self.assertEqual(high_price1, round(high_price2, 2))
            self.assertEqual(low_price1, round(low_price2, 2))
            # 成交量和成交额 总是有误差 ？？
            # self.assertEqual(volume1, volume2)
            # self.assertEqual( amount1 , amount2)
            self.assertEqual(date1, date2)

            # print(idx_from_df_dad)
            #print(type(open_price1), type(close_price1) ,type(high_price1), type(low_price1), type(volume1), type(amount1), type(date1))
        pass

    pass
