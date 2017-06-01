#coding:utf-8
"""
这里是实盘的时候可能用到的一些函数

- 历史数据和实盘数据的合并
- 账户信息的监控
- 风险监控
- 消息的传递
"""

import zmq
import requests
import json,sys,os,datetime,time
import pymongo
import tushare as ts
from QA_Trade_stock_api import QA_Stock
import QUANTAXIS as QA


def QA_get_hist_data(code,date):
    return QA.QA_fetch_get_stock_day('ts',code,date[0],date[1])
def QA_get_realtime_data():
    return QA.QA_fetch_get_stock_realtime('ts')
def QA_get_now_data(client,st,code):

    data=st.QA_trade_stock_get_quote(client,code)
    print(data.split('\n')[1].split('\t')[5])
def QA_combind_data(code,gap):
    data1=QA_get_hist_data('603999',[str(datetime.date.today()-datetime.timedelta(days=20)),str(datetime.date.today())])
    data2=QA_get_realtime_data()
    for item in data2:
        if item['code']=='603999':
            print(item)
def QA_get_account_assest(st,client):
    account={
        'cash':{},
        'stock':[],
        'time':{
            'time_stamp':datetime.datetime.now().timestamp(),
            'date':str(datetime.date.today()),
            'date_stamp':QA.QA_util_date_stamp(str(datetime.date.today())),
            }}
    cash=st.QA_trade_stock_get_cash(client)
    stock=st.QA_trade_stock_get_stock(client)
    stocks=stock.split('\n')
    """
    资金帐号        币种    资金余额        可用资金        冻结资金        在途资金        可取资金        可转资金        保留信息
    """
    accounts=cash.split('\n')[1].split('\t')
    account['cash']['account_id']=accounts[0]
    account['cash']['available']=accounts[3]
    account['cash']['freeze']=accounts[4]
    account['cash']['on_way']=accounts[5]
    account['cash']['withdraw']=accounts[6]

    for i in range(1,len(stocks)):
        """
        证券代码        证券名称        证券数量        持仓量  可卖数量        当前价  最新市值        成本价  浮动盈亏        盈亏比例(%)     帐号类别
        资金帐号        股东代码        交易所名称      买卖标志        买卖标志        投保标志        投保标志        今买数量        今卖数量        买持
        仓      卖持仓  昨日结算价      保证金  保留信息

        """
        temp={}
        temp['code']=stocks[i].split('\t')[0]
        temp['name']=stocks[i].split('\t')[1]
        temp['number']=stocks[i].split('\t')[2]
        temp['hold']=stocks[i].split('\t')[3]
        temp['sell_available']=stocks[i].split('\t')[4]
        temp['price_now']=stocks[i].split('\t')[5]
        temp['value_now']=stocks[i].split('\t')[6]
        temp['price_buy']=stocks[i].split('\t')[7]
        temp['pnl_float']=stocks[i].split('\t')[8]
        temp['pnl_ratio']=stocks[i].split('\t')[9]
        temp['account_type']=stocks[i].split('\t')[10]
        temp['account_id']=stocks[i].split('\t')[11]
        temp['shareholder']=stocks[i].split('\t')[12]
        temp['exchange']=stocks[i].split('\t')[13]
        temp['trade_mark']=stocks[i].split('\t')[14]
        temp['insure_mark']=stocks[i].split('\t')[15]
        temp['buy_today']=stocks[i].split('\t')[16]
        temp['sell_today']=stocks[i].split('\t')[17]
        temp['position_buy']=stocks[i].split('\t')[18]
        temp['position_sell']=stocks[i].split('\t')[19]
        temp['price_yesterday']=stocks[i].split('\t')[20]
        temp['margin']=stocks[i].split('\t')[21]
        account['stock'].append(temp)




    return account
    
def QA_risk_analysis():
    pass

def QA_save_account(st,client,db):
    db.trade_stock.insert(QA_get_account_assest(st,client))
if __name__=='__main__':
    st=QA_Stock()
    st.get_config()
    client = st.QA_trade_stock_login()
    #print(QA_get_hist_data('603999',[str(datetime.date.today()-datetime.timedelta(days=20)),str(datetime.date.today())]))
    #data=QA_get_realtime_data()

    print(QA_get_account_assest(st,client))

    
    #print(ts.get_today_all())