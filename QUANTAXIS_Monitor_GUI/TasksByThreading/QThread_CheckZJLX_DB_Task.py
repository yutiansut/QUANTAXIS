
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


from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list
from QUANTAXIS.QAUtil.QADate_trade import *

import pandas as pd
import numpy as np

from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_RootClass import *


class QThread_Check_ZJLX_DB_Status(QThread_RootClass):


    #db.getCollection('eastmoney_stock_zjlx').find({ 'stock_code':{'$in': ['000001']}}).sort({date:1})

    '''
    > db.eastmoney_stock_zjlx.aggregate([{$sort:{stock_code:1, date:1}},{$group: {_id:'$stock_code', first_date:{$first:'$date'}, last_date:{$last:'$date'}, total_num:{$sum : 1}}}])

    '''
    def QA_count_eastmoney_stock_xjlc_record_count_by_aggregate(self, collections=DATABASE.eastmoney_stock_zjlx):
        #codeArrayList = QA_util_code_tolist(str_stock_code_list)

        sort = {'$sort':{'stock_code':1, 'date':1}}   #按照count对应的值得降序排序
        group = {'$group': {'_id': '$stock_code', 'first_date':{ '$first':'$date'}, 'last_date':{'$last':'$date'}, 'total_num':{'$sum' : 1}  }}
        pipeline = [group, sort]

        cursor = collections.aggregate(
            [
                {'$sort':{'stock_code':1, 'date':1}},
                {'$group':{'_id': '$stock_code', 'first_date':{ '$first':'$date'}, 'last_date':{'$last':'$date'}, 'total_num':{'$sum' : 1}}}
             ]
        )
        items = [item for item in cursor]

        def takeId_sort(elem):
            return elem['_id']
        items.sort(key=takeId_sort)

        #停牌的股票，过滤
        strToday = QADate.QA_util_today_str()
        strLastTradeDate = QADate_trade.QA_util_get_real_date(strToday)
        strLastTradeDate = QADate_trade.QA_util_get_last_day(strLastTradeDate) #网页版资金流向只更新到前一天

        #比较日期

        yesterTradeDayInt = QADate.QA_util_date_str2int(strLastTradeDate)

        for item in items:
            lastDayIntInDB = QADate.QA_util_date_str2int(item['last_date'])
            if lastDayIntInDB < yesterTradeDayInt:
                item['need_update'] = 'Yes'
            else:
                item['need_update'] = 'No'

        #map( lambda aRecDict: aRecDict['need_update'] = (aRecDict['last_date'] == strLastTradeDate)    , items)
        #
        #map( lambda aRecDict: (aRecDict['need_update'] = (aRecDict['last_date'] == strLastTradeDate))  , items)

        return items


    # 非常慢
    def QA_count_eastmoney_stock_xjlc_record_count_one_by_one(self, str_stock_code, collections=DATABASE.eastmoney_stock_zjlx):

        codeArray = QA_util_code_tolist(str_stock_code)
        cursor = collections.find({
            'stock_code': {'$in': codeArray}
        }).sort('date')

        sizeRec = cursor.count()

        firstRec = None
        lastRec = None
        if sizeRec > 0:
            firstRec = cursor[0]
            lastRec = cursor[sizeRec-1]

        #返回 【code 记录条数 开始日期 结束日期 】
        #print(firstRec)
        #print(lastRec)

        firstRecDate = None
        if firstRec is not None:
            firstRecDate =  firstRec['date']

        lastRecDate = None
        if lastRec is not None:
            lastRecDate = lastRec['date']


        return [str_stock_code, sizeRec ,firstRecDate, lastRecDate]

    # 按照 QUANTAXIS 的风格去 写 2333333333
    # todo 移动到 QUANTAXIS 目录中去， 给命令行调用
    #
    def QA_fetch_eastmoney_stock_zjlx(self,str_stock_code = None, strStartDate = None, strEndDate = None, strFormat='numpy',collections=DATABASE.eastmoney_stock_zjlx):

        codeArray = QA_util_code_tolist(str_stock_code)
        if QA_util_date_valid(strEndDate):

            if strStartDate == None and strEndDate == None:

                cursor = collections.find({
                   'stock_code': {'$in': codeArray}
                })

                items = [item for item in cursor]
                res = pd.DataFrame(items)

                #todo fixhere reset pandas index

                if format in ['P', 'p', 'pandas', 'pd']:
                    return res
                elif format in ['json', 'dict']:
                    return QA_util_to_json_from_pandas(res)
                    # 多种数据格式
                elif format in ['n', 'N', 'numpy']:
                    return np.asarray(res)
                elif format in ['list', 'l', 'L']:
                    return np.asarray(res).tolist()
                else:
                    print(
                        "QA Error QA_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
                    return None
        else:
            cursor2 = collections.find({
                'stock_code': { '$in': codeArray },
                'date': {
                    '$lte': strEndDate,
                    '$gte': strStartDate
                }
            });

            items = [item for item in cursor2]
            res = pd.DataFrame(items)

            # todo fixhere reset pandas index

            if format in ['P', 'p', 'pandas', 'pd']:
                return res
            elif format in ['json', 'dict']:
                return QA_util_to_json_from_pandas(res)
                # 多种数据格式
            elif format in ['n', 'N', 'numpy']:
                return np.asarray(res)
            elif format in ['list', 'l', 'L']:
                return np.asarray(res).tolist()
            else:
                print(
                    "QA Error QA_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
                return None
            #
            # sizeRec = cursor2.count()
            # firstRec = cursor2[0]
            # lastRec = cursor2[sizeRec-1]
            # allItems2 = [item for item in cursor2]
            # print(allItems2)
        pass


    ##########################################################################################################

    '''
        emit the string to the UI log table
    '''
    pyqtSignalToLogTable = None
    '''
        [股票代码, 记录数 , 开始日期, 结束日期, 是否需要获取]
    '''
    zjlxRecNeedUpdateStockCodes = []
    '''
        全部股票列表
    '''
    stockListAll = []

    ####################################################################################################



    ####################################################################################################
    def run(self):

        #
        def find(f, seq):
            """Return first item in sequence where f(item) == True."""
            for item in seq:
                if f(item):
                    return item

        self.zjlxRecNeedUpdateStockCodes.clear();
        self.stockListAll.clear()
        self.stockListAll = QA_fetch_stock_list()

        self.strTaskRunningLog = '正在检查数据库，已经获取的数据'
        itemsInZJLX = self.QA_count_eastmoney_stock_xjlc_record_count_by_aggregate()

        '''
            追究没有获取过的记录，
        '''

        # 非常慢
        # codeNeedAppend = []
        # for aItemInAllStock in self.stockListAll:
        #     code0 = aItemInAllStock['code']
        #     #self.strTaskRunningLog = '正在检查数据 {}'.format(code0)
        #
        #     foundItem = find(lambda aRec: aRec['_id'] == code0, itemsInZJLX)
        #     if foundItem is None:
        #         codeNeedAppend.append(code0)
        #
        #
        # print(codeNeedAppend)

        # 使用 dict
        allItemsByDict = {}
        partItemsByDict = {}

        needToAppendCode = []

        self.strTaskRunningLog = '正在检查数据库，从未获取的记录'

        for iRecWhole in self.stockListAll:
            allItemsByDict[iRecWhole['code']] = iRecWhole['code']

        for iRecPart in itemsInZJLX:
            partItemsByDict[iRecPart['_id']] = iRecPart['_id']

        for iRec in allItemsByDict:
            try:
                stock_code = partItemsByDict[iRec]
            except Exception as ee:
                #part 里面 没有 这个股票代码
                needToAppendCode.append(iRec)
                #print(ee)

        #print(needToAppendCode)

        for codeAppend in needToAppendCode:
            anItem = {'_id': codeAppend, 'first_date': '第一次获取', 'last_date': '第一次获取', 'total_num': 0, 'need_update': 'Yes'}
            itemsInZJLX.append(anItem)

        def takeCode(elem):
            return elem['_id']

        itemsInZJLX.sort(key=takeCode)


        iIndexZJLX = 0
        zjlxCount = len(itemsInZJLX)

        for itemInZjlx in itemsInZJLX:
            try:
                iIndexZJLX = iIndexZJLX + 1
                self.strTaskRunningLog = '正在检查数据:{} 进度:{}/{}'.format(itemInZjlx, iIndexZJLX, zjlxCount)

                # item['_id'], item['start_date'], item['end_date'], item['total_num'], item['need_update']
                col0 = itemInZjlx['_id']
                col1 = itemInZjlx['first_date']
                col2 = itemInZjlx['last_date']
                col3 = itemInZjlx['total_num']
                col4 = itemInZjlx['need_update']
                self.pyqtSignalToLogTable.emit(col0, col1, col2, col3, col4)

                if itemInZjlx['need_update'] == 'Yes':
                    self.zjlxRecNeedUpdateStockCodes.append(col0)


            except Exception as ee:
                print(ee)



        self.strTaskRunningResult = " 任务结束 "
        pass