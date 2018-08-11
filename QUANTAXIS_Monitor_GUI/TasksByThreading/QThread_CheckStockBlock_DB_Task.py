import time



from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list
from QUANTAXIS.QAUtil import DATABASE


from QUANTAXIS.QAUtil import (DATABASE,QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_dict_remove_key,
                              QA_util_log_info, QA_util_code_tolist, QA_util_date_str2int, QA_util_date_int2str,
                              QA_util_sql_mongo_sort_DESCENDING,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse, QADate_trade,QADate)


from QUANTAXIS.QAUtil.QADate_trade import *
from QUANTAXIS.QAUtil.QADate import *

from QUANTAXIS.QAFetch.QAQuery import *
from QUANTAXIS.QAFetch.QAQuery_Advance import *
from QUANTAXIS.QAUtil.QADate_trade import *

import pandas as pd
import numpy as np

from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_RootClass import *
import time


class QThread_Check_StockBlock_DB(QThread_RootClass):

    def QA_statistic_block_data(self):

        # 🛠 todo 直接使用monogodb 数据库去统计
        try:
            block_list_df = QA_fetch_stock_block()
            blockNameList = {}
            block_list_df = block_list_df.set_index(['blockname'])

            for strIndexBlockName in block_list_df.index:
                try:
                    dict = blockNameList[strIndexBlockName]
                    dict['count'] = dict['count'] + 1
                    self.strTaskRunningLog = "正在统计板块{} 股票个数{}".format(strIndexBlockName, dict['count'])

                except Exception as ee:
                    dictNew = {}
                    dictNew['up'] = 0    #上涨家数
                    dictNew['even'] = 0  #平盘家数
                    dictNew['down'] = 0  #下跌家数
                    dictNew['count'] = 0 #板块股票数
                    dictNew['upRatio'] = 0.0 #上涨家数比率
                    dictNew['downRation'] = 0.0 #下跌家数比率
                    blockNameList[strIndexBlockName] = dictNew
                #row2 = block_list_df[i]
            #######################################################################################################

            strToday = QADate.QA_util_today_str()
            strEndDate = QADate_trade.QA_util_get_real_date(date = strToday)
            strStartDate = QADate_trade.QA_util_get_last_day(date= strEndDate)

            codeTwoDayPriceeDict = {}
            stock_list = QA_fetch_stock_list()

            stock_list_len = len(stock_list)
            stock_name_count = 0
            for aStockCode in stock_list:
                stock_name_count = stock_name_count + 1
                strAcode = aStockCode['code']
                strAName = aStockCode['name']
                priceTowDay = QA_fetch_stock_day_adv(code=strAcode, start=strStartDate, end=strEndDate)

                up = None
                if priceTowDay is not None:
                    priceTowDay.to_qfq()
                    # price_len = len(priceTowDay)
                    # print(priceTowDay)

                    price_len = len(priceTowDay)
                    if price_len == 2:
                        closeSerial = priceTowDay.close
                        # todayPrice = priceTowDay[1].close
                        v1 = closeSerial[0]
                        v2 = closeSerial[1]
                        if v1 < v2:
                            up = True
                        else:
                            up = False

                codeTwoDayPriceeDict[strAcode] = {'pricetwoday':priceTowDay,
                                                  'up':up}

                if  codeTwoDayPriceeDict[strAcode]['up'] is not None and codeTwoDayPriceeDict[strAcode]['up'] == True:
                    self.strTaskRunningLog = "正在获取股票价格 {} {} 上涨 ⬆🔺,  进度{}/{} " \
                        .format(strAcode, strAName, stock_name_count, stock_list_len)

                elif codeTwoDayPriceeDict[strAcode]['up'] is not None and codeTwoDayPriceeDict[strAcode]['up'] == False:
                    self.strTaskRunningLog = "正在获取股票价格 {} {} 下跌 ⬇️,  进度{}/{} " \
                        .format(strAcode, strAName, stock_name_count, stock_list_len)

                else:
                    self.strTaskRunningLog = "正在获取股票价格 {} {} 和前一天的无法统计️,  进度{}/{} " \
                        .format(strAcode, strAName, stock_name_count, stock_list_len)
            ##########################################################################################################



            len_block_size = len(blockNameList)
            count = 0
            for blockName in blockNameList.keys():
                count = count + 1
                stocks_in_block = QA_fetch_stock_block_adv(code=None, blockname= blockName)
                self.strTaskRunningLog = "正在统计板块{} ,进度{}/{}".format(blockName,count,len_block_size)
                code_list = stocks_in_block.code

                iCodeLength = len(code_list)
                iCountForCode = 0

                for iCode in code_list:

                    iCountForCode = iCountForCode + 1

                    try:
                        priceTowDay = codeTwoDayPriceeDict[iCode]['pricetwoday']
                        upValue = codeTwoDayPriceeDict[iCode]['up']

                        if priceTowDay is not None:
                            if upValue == True:
                                blockNameList[blockName]['up'] = blockNameList[blockName]['up'] + 1
                            elif upValue == False:
                                blockNameList[blockName]['down'] = blockNameList[blockName]['down'] + 1


                    except Exception as ee:
                        strErrorMsg = ee.__str__()
                        print(strErrorMsg)



                        self.strTaskRunningLog = "正在统计板块{} ,进度{}/{} \n 股票 {}, 进度 {}/{}"\
                            .format(blockName, count, len_block_size, iCode, iCountForCode, iCodeLength)

                    pass
                #print(stocks_in_block)
            #######################################################################################################

        except Exception as eee:
            strErrorMsg = eee.__str__()
            print(strErrorMsg)

        finally:
            return blockNameList


    # 给 Table View 使用
    blockStatisticList = {}
    ##########################################################################################################
    def run(self):
        #统计板块涨跌幅
        self.strTaskRunningLog = "开始统计板块涨跌幅数据"
        self.blockStatisticList = self.QA_statistic_block_data()
        self.strTaskRunningResult = "完成统计板块涨跌幅数据"
        pass