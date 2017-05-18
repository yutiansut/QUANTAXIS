#coding:utf-8
import easyquotation
import redis
import datetime

quotation = easyquotation.use('sina')  
r = redis.Redis(host='localhost', port=6379, db=0)
code=['000002','600538','601801']

for i in range(1,100000):
    
    
    print (quotation.stocks(['000001', code]))  
   # r.save(quotation.stocks(code))


"""
result=eval(r.get(code))[code]
print(result['high'])
"""
