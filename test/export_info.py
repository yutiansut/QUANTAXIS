#coding:utf-8
import sys
import pymongo
import csv
coll=pymongo.MongoClient().quantaxis.backtest_info
coll2=pymongo.MongoClient().quantaxis.stock_info
with open('info.csv','w',newline='') as f:
    csvwriter=csv.writer(f)
    csvwriter.writerow(['strategy','stock_list','start_time','end_time','account_cookie','total_returns','annualized_returns','benchmark_annualized_returns','win_rate','alpha','beta','sharpe','vol','benchmark_vol','max_drop','exist','outstanding','totals'])
    for item in  coll.find():
        code=item['stock_list'][0]
        try:
            data=coll2.find_one({'code':code})
            outstanding=data['outstanding']
            totals=data['totals']
            csvwriter.writerow([item['strategy'],'c'+str(item['stock_list'][0]),item['start_time'],item['end_time'],item['account_cookie'],item['total_returns'],item['annualized_returns'],item['benchmark_annualized_returns'],item['win_rate'],item['alpha'],item['beta'],item['sharpe'],item['vol'],item['benchmark_vol'],item['max_drop'],item['exist'],outstanding,totals])
        except:
            info=sys.exc_info()  
            print(info[0],":",info[1])
            print(code)

            