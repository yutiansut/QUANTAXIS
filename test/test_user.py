#coding:utf-8

import QUANTAXIS as QA
import pymongo
client=pymongo.MongoClient()
QA.QA_user_sign_up('yutiansut','yutiansut',client)
QA.QA_user_sign_in('yutiansut','yutiansut',client)
