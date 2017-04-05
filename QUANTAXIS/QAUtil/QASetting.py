from QUANTAXIS.QAUtil import QA_util_log_info,QA_util_sql_mongo_setting


class QA_Setting():
    
    QA_util_sql_mongo_ip='127.0.0.1'
    QA_util_sql_mongo_port='3306'
    QA_util_log_info('Welcome to QUANTAXIS, the Version is 0.3.8-beta')
    client=QA_util_sql_mongo_setting(QA_util_sql_mongo_ip,QA_util_sql_mongo_port)
