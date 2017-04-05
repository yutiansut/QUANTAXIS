from ..QAFetch import QAWind
from ..QAMarket import deal
from ..QAARP import QAAccount,QAPortfolio,QARisk
from QUANTAXIS.QAUtil import QA_util_log_info,QA_Setting,QA_util_sql_mongo_setting
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
        


def QA_signal_resend(from_module,to_module,if_save,message):
    pass

