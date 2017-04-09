#coding=utf-8
from QUANTAXIS.QAUtil import QA_util_log_info

def QA_user_sign_in(name,password,clients):
    coll=clients.quantaxis.user_list
    if (coll.find({'username':name,'password':password}).count() >0):
        QA_util_log_info('success login! your username is:'+str(name))
        return True
    else: 
        QA_util_log_info('Failed to login,please check your password ')
        return False
def QA_user_sign_up(name,password,clients):
    coll=clients.quantaxis.user_list
    if (coll.find({'username':name}).count() >0):
        QA_util_log_info('user name is already exist')
    else :
        coll.insert({'username':name,'password':password})
        QA_util_log_info('Success sign in! please login ')
