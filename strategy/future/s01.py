# -*- coding:utf-8 -*-

from WindPy import w
import pymongo

w.start()


# 拼接在市合约和退市合约
# 如果已经退市,直接存入mongodb

data=w.wset("SectorConstituent","date=20170124;sectorId=1000009644000000")
list=data.Data

for i in range(0,len(list[0])):
    date=list[0][i]
    code=list[1][i]
    
    print code
print date
