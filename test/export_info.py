#coding:utf-8
import pymongo
import csv
coll=pymongo.MongoClient().quantaxis.backtest_info
with open('info.csv','w') as f:
    csvwriter=csv.writer(f)
    for item in  coll.find():
        csvwriter.writerow([item['strategy'],str(item['stock_list'][0]),item['start_time'],item['end_time'],item['account_cookie'],item['total_returns'],item['annualized_returns'],item['benchmark_annualized_returns'],item['win_rate'],item['alpha'],item['beta'],item['sharpe'],item['vol'],item['benchmark_vol'],item['max_drop'],item['exist']])