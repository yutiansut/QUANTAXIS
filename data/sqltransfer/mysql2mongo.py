# -*- coding:utf-8 -*-

from WindPy import *
import pymongo
import pymysql
import re

client =pymongo.MongoClient('localhost', 27017)  
db = client.stock
coll = db.ts

w.start()

conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='940809',db='quantaxis',charset='utf8')
cursor=conn.cursor()
cursor.execute("select * from stocklist")
result = cursor.fetchall()
days=w.tdays("2000-01-01", "2017-02-22", "")
tradeday=days.Data
for item in result:
    i=0;
    code = item[0][0:6]
    codename=item[1]
    strs = code+'_ts'
    print strs
    cursorsx=conn.cursor()
    sqlquery="select * from "+strs
    print sqlquery
    cursorsx.execute(sqlquery) 
    resultsx = cursorsx.fetchall()
    
    for items in resultsx:
        coll.insert({"code":code,"name":codename,"date":tradeday[i],"pre_close":items[1],"open":items[2],"high":items[3],"low":items[4],"close":items[5],"volume":items[6],"amt":items[7],"chg":items[8],"pct_chg":items[9],"swing":items[10],"vwap":items[11],"turn":items[12],"rel_ipo_chg":items[13],"rel_ipo_pct_chg":items[14]})
        i=i+1
        print i
conn.commit()
cursor.close()
conn.close()
