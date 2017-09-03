# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import QUANTAXIS as QA


"""
data=QA.QA_fetch_stocklist_day_adv(['000001','000006','000004','600010','601801'],'2017-07-01','2017-07-31')
#print(data.to_qfq().data)

print(data.to_qfq().data.query('date=="2017-07-04"'))

print(data.to_qfq().splits())

x=data.to_qfq().splits()[0]

print([item.data for item in data.to_qfq().splits()])
print(x)
print(x.data)
#y=QA.QA_DataStruct_Stock_day(x)
#print(y.data)
#print(y.code)
print(x.to_qfq().data)
#print(y.to_hfq().data)
#print(data.to_hfq().splits()[0].if_fq)

print(x.to_hfq().to_qfq().data)
"""
#data=QA.QA_fetch_stock_min_adv('000001','2017-07-26','2017-07-27')


#data=QA.QA_fetch_stocklist_min(['000001','000006','000004','600010','601801'],['2017-07-26','2017-07-27'],'1min')
#print(data)
#=QA.QA_fetch_stock_min('000001','2017-07-26','2017-07-27','pd','1min')
#print(data)
data=QA.QA_fetch_stocklist_min_adv(['000001','000006','000004','600010','601801'],'2017-07-26','2017-07-27')
print(data.to_qfq().data)
dax=data.to_qfq().data
print(dax[dax['datetime']=='2017-07-26 14:45:00'])

print(data.to_qfq().splits())
#print([item.data for item in data.to_qfq().splits()])
#data=QA.QA_fetch_stock_day_adv('000001','2017-07-26','2017-07-27')

#data=QA.QA_fetch_stocklist_min_adv(['000001','000006','000004','600010','601801'],'2017-07-26','2017-07-27')
#print(data.to_qfq().data)