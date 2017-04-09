from QUANTAXIS.QAUtil import QA_util_log_info,QA_util_sql_mongo_setting


class QA_Setting():
    
    QA_util_sql_mongo_ip='127.0.0.1'
    QA_util_sql_mongo_port='27017'
    client=''
    
    QA_setting_user_name=''
    QA_setting_user_password=''
    
    def QA_setting_init(self):
        self.client=QA_util_sql_mongo_setting(self.QA_util_sql_mongo_ip,self.QA_util_sql_mongo_port)
        
    def QA_setting_login(self):
        self.username=self.QA_setting_user_name
        self.password=self.QA_setting_user_password
        QA_util_log_info('username:'+str(self.QA_setting_user_name))