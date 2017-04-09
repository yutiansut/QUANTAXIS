from QUANTAXIS.QAUtil import QA_util_log_info,QA_util_sql_mongo_setting
from QUANTAXIS.QASU.user import QA_user_sign_in,QA_user_sign_up

class QA_Setting():
    
    QA_util_sql_mongo_ip='127.0.0.1'
    QA_util_sql_mongo_port='27017'
    client=QA_util_sql_mongo_setting(QA_util_sql_mongo_ip,QA_util_sql_mongo_port)
    
    QA_setting_user_name=''
    QA_setting_user_password=''
    user={'username':'','password':'','login':False}
    def QA_setting_init(self):
        self.client=QA_util_sql_mongo_setting(self.QA_util_sql_mongo_ip,self.QA_util_sql_mongo_port)
        self.user=self.QA_setting_login()
    def QA_setting_login(self):
        self.username=self.QA_setting_user_name
        self.password=self.QA_setting_user_password
        QA_util_log_info('username:'+str(self.QA_setting_user_name))
        result=QA_user_sign_in(self.username,self.password,self.client)
        if result==True:
            self.user['username']=self.username
            self.user['password']=self.password
            self.user['login']=True
            return self.user
        else:
            QA_util_log_info('failed to login')
