#coding:utf-8

import QUANTAXIS as QA
import pymongo

QA.QA_save_stock_day_all()
QA.QA_update_standard_sql()
QA.QA_SU_save_stock_list('ts',pymongo.MongoClient())
QA.QA_SU_save_trade_date_all()


#仅仅是为了初始化才在这里插入用户,如果想要注册用户,要到webkit底下注册
pymongo.MongoClient().quantaxis.user_list.insert({'username':'admin','password':'admin'})


