#coding:utf-8
import json,datetime,time
import pymongo
import numpy as np
import pandas as pd
import csv

# settings
unit_strategy_name=''
# clients/collections
client=pymongo.MongoClient().quantaxis
coll_info=client.backtest_info
coll_history=client.backtest_history
#coll_stock_day=client.stock_day
#coll_stock_info=client.stock_info
coll_stock_list=client.stock_list



stock_list=[]

with open('da1.csv','r') as f:
    csvreader=csv.reader(f)
    for item in csvreader:
        stock_list.append(str(item[0][1:7]))

#stock_list=stock_list[0:20]
print(stock_list)




def make_portfolio(stock_list,unit_strategy_name):
    portfolio_data=[]
    for item in stock_list:
        try:
            data=coll_info.find_one({'stock_list':item,'strategy':unit_strategy_name})
            cookie=data['account_cookie']
            print(cookie)
            history=coll_history.find({'cookie':cookie})
            historys=history[history.count()-1]['history']
            print(len(historys))
            portfolio_data.append(historys)
        except:
            print('wrong')
    #print(portfolio_data)
    # 计算和合并交易队列
    # [date,code,price,amount,towards]
    l=[]
    for item in portfolio_data:
        for items in item[1::]:
            l.append(items)
    #按时间序列组合交易历史记录
    l.sort()

    #新增一列 计算资金占用
    l[0].append(float(l[0][2])*float(l[0][3])*int(l[0][4]))
    for i in range(1,len(l)-1,1):
        l[i].append(l[i-1][5]+float(l[i][2])*float(l[i][3])*int(l[i][4]))



    with open('choice1.csv','w',newline='') as f:
        csvwriter=csv.writer(f)
        csvwriter.writerow(['date','code','price','amount','towards','money_occupy'])
        for item in l:
            csvwriter.writerow(item)


make_portfolio(stock_list,unit_strategy_name)

