#coding:utf-8

import QUANTAXIS as QA
import pymongo

QA.QA_save_stock_day_all()
QA.QA_update_standard_sql()
QA.QA_SU_save_stock_list('ts',pymongo.MongoClient())
