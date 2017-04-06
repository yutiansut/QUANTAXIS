from ..QAFetch import QAWind
from ..QAMarket import QAMarket_core,QABid
from ..QAARP import QAAccount,QAPortfolio,QARisk
from .EventManager import QA_Signal_events,QA_Signal_eventManager
from .usualevnet import PublicAccounts,Listener,QA_signal_usual_model
from QUANTAXIS.QAUtil import QA_util_log_info,QA_Setting,QA_util_sql_mongo_setting
from threading import *

import time,datetime,re

def QA_signal_send(from_module,to_module,if_save,message):
    QA_signal_message='[from]: '+str(from_module)+'  [to]:  '+str(to_module)+' [message]: '+str(message)
    QA_util_log_info(QA_signal_message)
    if if_save==True:
        print('save')
        db=QA_Setting.client.quantaxis
        coll=db.log_signal
        coll.insert({"time":datetime.datetime.now(),'message':QA_signal_message})
    else:
        QA_util_log_info('No Saving')
        


def QA_signal_resend(name,QA_signal_send_event,QA_signal_receive_event,listener):
    pass


def QA_signal_test(name,QA_signal_send_event,QA_signal_receive_event,listen_name):
    eventManager = QA_Signal_eventManager()
    for item in range(0,len(listen_name),1):
        listner = Listener(listen_name[item]) #订阅
        eventManager.AddEventListener(name,listner.QA_signal_receive_event)

    #绑定事件和监听器响应函数
    eventManager.Start()
    publicAcc = PublicAccounts(eventManager)
    timer = Timer(1, publicAcc.QA_signal_send_event)
    timer.start()



