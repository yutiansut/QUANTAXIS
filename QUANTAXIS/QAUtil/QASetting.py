from QUANTAXIS.QAUtil import QA_util_log_info,QA_util_sql_mongo_setting


class QA_Setting():
    
    QA_util_sql_mongo_ip='127.0.0.1'
    QA_util_sql_mongo_port='27017'
   
    client=QA_util_sql_mongo_setting(QA_util_sql_mongo_ip,QA_util_sql_mongo_port)
    QA_setting_user_name=''
    QA_setting_user_password=''
