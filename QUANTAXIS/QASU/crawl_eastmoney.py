import os
from QUANTAXIS.QASetting import QALocalize
#from QUANTAXIS_CRAWLY.run_selenium_alone import (read_east_money_page_zjlx_to_sqllite, open_chrome_driver, close_chrome_dirver)
from QUANTAXIS_CRAWLY.run_selenium_alone import *
import urllib
import pandas as pd
import time

from QUANTAXIS.QAUtil import (DATABASE)



def QA_request_eastmoney_zjlx( param_stock_code_list ):
    # 改用
    strUrl = "http://data.eastmoney.com/zjlx/{}.html".format(param_stock_code_list[0])

    # 延时
    time.sleep(1.223)

    response = urllib.request.urlopen(strUrl)
    content = response.read()

    # 🛠todo 改用 re 正则表达式做匹配
    strings = content.decode("utf-8", "ignore")
    string_lines = strings.split("\r\n")

    values = []
    for aline in string_lines:
        aline = aline.strip()
        if 'EM_CapitalFlowInterface' in aline:
            aline = aline.strip()
            if aline.startswith('var strUrl = '):
                if 'var strUrl = ' in aline:
                    aline = aline[len('var strUrl = '):]
                    values = aline.split('+')

            break

    print(values)

    for iStockCode in range(len(param_stock_code_list)):
        requestStr = ""

        strCode =  param_stock_code_list[iStockCode]
        if strCode[0:2] == '60':
            _stockMarke = '1'
        elif strCode[0:2] == '00' or strCode[0:2] == '30':
            _stockMarke = '2'
        else:
            print(strCode + " 暂不支持， 60， 00， 30 开头的股票代码")
            return

        for iItem in values:
            if '_stockCode' in iItem:
                requestStr = requestStr + param_stock_code_list[iStockCode]
            elif '_stockMarke' in iItem:
                requestStr = requestStr + _stockMarke
            else:
                if 'http://ff.eastmoney.com/' in iItem:
                    requestStr = 'http://ff.eastmoney.com/'
                else:
                    iItem = iItem.strip(' "')
                    iItem = iItem.rstrip(' "')
                    requestStr = requestStr + iItem

        # 延时
        time.sleep(1.456)

        response = urllib.request.urlopen(requestStr)
        content2 = response.read()

        strings = content2.decode("utf-8", "ignore")

        list_data_zjlx = []

        if 'var aff_data=({data:[["' in strings:
            leftChars = strings[len('var aff_data=({data:[["'):]
            dataArrays = leftChars.split(',')
            for aItemIndex in range(0, len(dataArrays), 13):
                '''
                日期
                收盘价
                涨跌幅
                主力净流入 净额 净占比
                超大单净流入 净额 净占比
                大单净流入 净额 净占比
                中单净流入 净额 净占比
                小单净流入 净额 净占比
                '''
                dict_row = {}

                dict_row['stock_code'] = param_stock_code_list[iStockCode]

                # 日期
                data01 = dataArrays[aItemIndex]
                data01 = data01.strip('"')

                dict_row['date'] = data01

                # 主力净流入 净额
                data02 = dataArrays[aItemIndex + 1]
                data02 = data02.strip('"')

                dict_row['zljll_je_wy'] = data02

                # 主力净流入 净占比
                data03 = dataArrays[aItemIndex + 2]
                data03 = data03.strip('"')

                dict_row['zljll_jzb_bfb'] = data03

                # 超大单净流入 净额
                data04 = dataArrays[aItemIndex + 3]
                data04 = data04.strip('"')

                dict_row['cddjll_je_wy'] = data04

                # 超大单净流入 净占比
                data05 = dataArrays[aItemIndex + 4]
                data05 = data05.strip('"')

                dict_row['cddjll_je_jzb'] = data05

                # 大单净流入 净额
                data06 = dataArrays[aItemIndex + 5]
                data06 = data06.strip('"')

                dict_row['ddjll_je_wy'] = data06

                # 大单净流入 净占比
                data07 = dataArrays[aItemIndex + 6]
                data07 = data07.strip('"')

                dict_row['ddjll_je_jzb'] = data07

                # 中单净流入	 净额
                data08 = dataArrays[aItemIndex + 7]
                data08 = data08.strip('"')

                dict_row['zdjll_je_wy'] = data08

                # 中单净流入	 净占比
                data09 = dataArrays[aItemIndex + 8]
                data09 = data09.strip('"')

                dict_row['zdjll_je_jzb'] = data09

                # 小单净流入	 净额
                data10 = dataArrays[aItemIndex + 9]
                data10 = data10.strip('"')

                dict_row['xdjll_je_wy'] = data10

                # 小单净流入	 净占比
                data11 = dataArrays[aItemIndex + 10]
                data11 = data11.strip('"')

                dict_row['xdjll_je_jzb'] = data11

                # 收盘价
                data12 = dataArrays[aItemIndex + 11]
                data12 = data12.strip('"')

                dict_row['close_price'] = data12

                # 涨跌幅
                data13 = dataArrays[aItemIndex + 12]
                data13 = data13.strip('"')
                data13 = data13.strip('"]]})')

                dict_row['change_price'] = data13

                # 读取一条记录成功 
                list_data_zjlx.append(dict_row)

        # print(list_data_zjlx)

        df = pd.DataFrame(list_data_zjlx)

        # print(df)

        client = DATABASE
        coll_stock_zjlx = client.eastmoney_stock_zjlx

        # coll_stock_zjlx.insert_many(QA_util_to_json_from_pandas(df))

        for i in range(len(list_data_zjlx)):
            aRec = list_data_zjlx[i]

            # 🛠todo 当天结束后，获取当天的资金流相，当天的资金流向是瞬时间点的
            ret = coll_stock_zjlx.find_one(aRec)
            if ret == None:
                coll_stock_zjlx.insert_one(aRec)
                print("🤑 插入新的记录 ", aRec)
            else:
                print("😵 记录已经存在 ", ret)


'''
    作为测试用例来获取， 对比 reqeust 方式的获取数据是否一致
'''
def QA_read_eastmoney_zjlx_web_page_to_sqllite(stockCodeList = None):

    # todo 🛠 check stockCode 是否存在有效合法
    # todo 🛠 QALocalize 从QALocalize 目录中读取 固定位置存放驱动文件

    print("📨当前工作路径文件位置 : ",os.getcwd())
    path_check = os.getcwd()+"/QUANTAXIS_WEBDRIVER"
    if os.path.exists(path_check) == False:
        print("😵 确认当前路径是否包含selenium_driver目录 😰 ")
        return
    else:
        print(os.getcwd()+"/QUANTAXIS_WEBDRIVER"," 目录存在 😁")
    print("")

    # path_for_save_data = QALocalize.download_path + "/eastmoney_stock_zjlx"
    # isExists = os.path.exists(path_for_save_data)
    # if isExists == False:
    #     os.mkdir(path_for_save_data)
    #     isExists = os.path.exists(path_for_save_data)
    #     if isExists == True:
    #         print(path_for_save_data,"目录不存在！ 成功建立目录 😢")
    #     else:
    #         print(path_for_save_data,"目录不存在！ 失败建立目录 🤮, 可能没有权限 🈲")
    #         return
    # else:
    #     print(path_for_save_data,"目录存在！准备读取数据 😋")

    browser = open_chrome_driver()

    for indexCode in range(len(stockCodeList)):
        #full_path_name = path_for_save_data + "/" + stockCodeList[indexCode] + "_zjlx.sqlite.db"
        read_east_money_page_zjlx_to_sqllite(stockCodeList[indexCode], browser)
        pass
    close_chrome_dirver(browser)
    #创建目录
    #启动线程读取网页，写入数据库
    #等待完成