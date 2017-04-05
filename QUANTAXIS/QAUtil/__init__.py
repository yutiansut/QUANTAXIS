# coding:utf-8

""""
yutiansut
util tool
"""


from .QADate import(QA_util_date_stamp,QA_util_time_stamp,QA_util_ms_stamp)
from .QASql import (QA_util_sql_mongo_setting)
from .QALogs import (QA_util_log_debug,QA_util_log_expection,QA_util_log_info)
from .QACfg import (QA_util_cfg_initial)

def QA_start_initial(files):
    QA_inital_setting=QA_util_cfg_initial(files)
    QA_sql_mongo_client=QA_util_sql_mongo_setting(QA_inital_setting[0],int(QA_inital_setting[1]))
    QA_util_log_info('Data Enging'+str(QA_inital_setting[2]))
    return QA_sql_mongo_client