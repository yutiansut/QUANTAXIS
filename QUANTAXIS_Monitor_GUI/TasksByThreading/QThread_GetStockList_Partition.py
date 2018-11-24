
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_list

from QUANTAXIS_Monitor_GUI.TasksByThreading.QThread_RootClass import *
'''
    获取股票列表
'''
class QThread_GetStockList_Partition(QThread_RootClass):




    def run(self):
        #time.sleep(2)
        print("QThread_GetStockList is running")
        # 检查数据库是否已经开启

        try:
            self.stockListAll = QA_fetch_stock_list()
        except   Exception as ee:
            # print(ee)
            self.strTaskRunningResult = ee.__str__()
            self.stockListAll = None
            self.stockCountAll = 0
            return

        self.stockCountAll = len(self.stockListAll)
        self.strTaskRunningResult= "成功获取 股票列表， 🔗 数据库成功 , 共 {} 个股票 😄".format(self.stockCountAll)
        pass