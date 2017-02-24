# -*- coding:utf-8 -*-
from WindPy import *
w.start()   
from datetime import datetime
import pymongo

#先搞上期
#数据库
# 拼接在市合约和退市合约
# 如果已经退市,直接存入mongodb

#退市合约
data=w.wset("SectorConstituent","date=20170224;sectorId=1000013989000000")
list=data.Data

client =pymongo.MongoClient('localhost', 27017)  
db = client.wind
coll = db.futureList

for i in range(0,len(list[0])):
    date=list[0][i]
    code=list[1][i]
    name=list[2][i]
    if (coll.find({"Code":code}).count()==0):  
        coll.insert({"Code":code,"Name":name})
    else:
        print "already in"