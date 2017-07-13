#coding:utf-8
import pymongo
import csv
import json
l=[]

for item in pymongo.MongoClient().quantaxis.trade_date.find():
    l.append(item['date'])
    #d[item['num']]=item['date']
print(l)
#print(d)