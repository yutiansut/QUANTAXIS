import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_data
from pymongo import  MongoClient
from QUANTAXIS.QAUtil import QA_util_date_stamp,QA_util_log_info
from QUANTAXIS.QAMarket import QA_QAMarket_bid,QA_market
from QUANTAXIS.QABacktest import QA_Backtest
from QUANTAXIS.QAARP import QAAccount,QAPortfolio,QARisk
from QUANTAXIS.QASignal import QA_signal_send
from QUANTAXIS.QASignal import (QA_Signal_eventManager,QA_Signal_events,
                                QA_Signal_Listener,QA_Signal_Sender,QA_signal_usual_model)
import pandas
from threading import *


class backtest(QA_Backtest):
    def QA_backtest_init(self):
        pass
    def QA_backtest_start(self):
        pass
    def signal_handle(self):
        pass
    
    def message_center(self,name,listener_name):
        class QASS(QA_Signal_Sender):
            def QAS_send(self):
                pass
        class QASL(QA_Signal_Listener):
            def QA_receive(self,event):
                pass
        eventManager = QA_Signal_eventManager()
        for item in range(0,len(listener_name),1):
            listner = QASL(listener_name[item]) #订阅
            eventManager.AddEventListener(name,listner.QA_receive)

        #绑定事件和监听器响应函数
        eventManager.Start()
        publicAcc = QASS(eventManager)
        timer = Timer(1, publicAcc.QAS_send)
        timer.start()


###运行
backtest=backtest()
backtest.QA_backtest_init()
backtest.QA_backtest_start()