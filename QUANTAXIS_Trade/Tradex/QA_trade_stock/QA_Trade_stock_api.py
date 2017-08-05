#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msvcrt
import sys
import configparser
import os
#print (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
# input()
import TradeX

TradeX.OpenTdx()


class QA_Stock():

    def set_config(self, configs):
        try:
            # print(str(os.path.dirname(os.path.realpath(__file__)))+'setting.ini')

            self.sHost = configs['host']
            self.nPort = configs['port']
            self.sVersion = configs['version']
            self.sBranchID = configs['branchID']
            self.sAccountNo = configs['accountNo']
            self.sTradeAccountNo = configs['tradeAccountNo']
            self.sPassword = int(configs['password'])
            self.sTxPassword = int(configs['txPassword'])

            print(self.sAccountNo)
        except:
            return ('error with read setting files')

    def get_config(self):
        config = configparser.ConfigParser()
        try:
            # print(str(os.path.dirname(os.path.realpath(__file__)))+'setting.ini')
            config.read(
                str(os.path.dirname(os.path.realpath(__file__))) + '\setting.ini')
            self.sHost = config['trade-mock']['host']
            self.nPort = config['trade-mock']['port']
            self.sVersion = config['trade-mock']['version']
            self.sBranchID = config['trade-mock']['branchID']
            self.sAccountNo = config['trade-mock']['accountNo']
            self.sTradeAccountNo = config['trade-mock']['tradeAccountNo']
            self.sPassword = int(config['trade-mock']['password'])
            self.sTxPassword = int(config['trade-mock']['txPassword'])
            config_setting = {
                "host": config['trade-mock']['host'],
                "port": config['trade-mock']['port'],
                "version": config['trade-mock']['version'],
                "branchID": config['trade-mock']['branchID'],
                "accountNo": config['trade-mock']['accountNo'],
                "tradeAccountNo": config['trade-mock']['tradeAccountNo'],
                "password": int(config['trade-mock']['password']),
                "txPassword": int(config['trade-mock']['txPassword'])
            }
            return config_setting

        except:
            return ('error with read setting files')

    def QA_trade_stock_login(self):
        try:
            TradeX.OpenTdx()
            client = TradeX.Logon(str(self.sHost), int(self.nPort), str(self.sVersion), int(self.sBranchID),
                                  str(self.sAccountNo), str(
                                      self.sTradeAccountNo),
                                  str(self.sPassword), str(self.sTxPassword))
            return client
        except TradeX.error as e:
            return ("error: " + e.message)

    def QA_trade_stock_login_with_config(self,config):
        try:
            TradeX.OpenTdx()
            client = TradeX.Logon(str(config[0]), int(config[1]), str(config[2]), int(self.sBranchID),
                                  str(self.sAccountNo), str(
                                      self.sTradeAccountNo),
                                  str(self.sPassword), str(self.sTxPassword))
            return client
        except TradeX.error as e:
            return ("error: " + e.message)

        """
        nCategory
        0 资金
        1 股份
        2 当日委托
        3 当日成交
        4 可撤单
        5 股东代码
        6 融资余额
        7 融券余额
        8 可融证券
        9
        10
        11
        12 可申购新股查询
        13 新股申购额度查询
        14 配号查询
        15 中签查询 
        """

    def QA_trade_stock_get_cash(self, _client):
        # 资金
        self.nCategory = 0

        _errinfo, self.result = _client.QueryData(self.nCategory)
        if _errinfo != "":
            return (errinfo)
        else:
            # print(self.result)
            accounts = self.result.split('\n')[1].split('\t')
            account={}
            account['account_id'] = accounts[0]
            account['available'] = accounts[3]
            account['freeze'] = accounts[4]
            account['on_way'] = accounts[5]
            account['withdraw'] = accounts[6]
            return account

    def QA_trade_stock_get_stock(self, client):
        # 股份
        self.nCategory = 1

        _errinfo, self.result = client.QueryData(self.nCategory)
        if _errinfo != "":
            return (errinfo)
        else:
            stocks=self.result.split('\n')
            stock=[]
            for i in range(1,len(stocks)):
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
                stock.append(temp)
            return stock

    def QA_trade_stock_get_orders(self, client):
        # 当日委托
        self.nCategory = 2

        _errinfo, self.result = client.QueryData(self.nCategory)
        if _errinfo != "":
            return (errinfo)
        else:

            return self.result

    def QA_trade_stock_get_deals(self, client):
        # 当日成交
        self.nCategory = 2

        _errinfo, self.result = client.QueryData(self.nCategory)
        if errinfo != "":
            return (_errinfo)
        else:
            print(self.result)
            return self.result

    def QA_trade_stock_get_holder(self, client):
        # 股东代码
        self.nCategory = 5

        errinfo, self.result = client.QueryData(self.nCategory)
        if errinfo != "":
            print(errinfo)
        else:
            # print(self.result.split('\n')[1].split('\t')[0])
            # print(self.result.split('\n')[2].split('\t')[0])

            return [self.result.split('\n')[1].split('\t')[0], self.result.split('\n')[2].split('\t')[0]]

            """
            nCategory - 委托业务的种类
                0 买入
                1 卖出
                2 融资买入
                3 融券卖出
                4 买券还券
                5 卖券还款
                6 现券还券
            nOrderType - 委托报价方式
                0 限价委托； 上海限价委托/ 深圳限价委托
                1 市价委托(深圳对方最优价格)
                2 市价委托(深圳本方最优价格)
                3 市价委托(深圳即时成交剩余撤销)
                4 市价委托(上海五档即成剩撤/ 深圳五档即成剩撤)
                5 市价委托(深圳全额成交或撤销)
                6 市价委托(上海五档即成转限价)
            sAccount - 股东代码
            sStockCode - 证券代码
            sPrice - 价格
            sVolume - 委托证券的股数
            返回值：
            errinfo - 出错时函数抛出的异常信息；
            result - 查询到的数据。


            nCategory = 0
            nOrderType = 4
            sInvestorAccount = "p001001001005793"
            sStockCode = "601988"
            sPrice = 0
            sVolume = 100
            """

    def QA_trade_stock_post_order(self, client, order):
        
        if len(order)==6:
            
            errinfo, self.result = client.SendOrder(order[0],order[1],order[2],order[3],order[4],order[5])
            if errinfo != "":
                print(errinfo)
            else:
                print(self.result)

    def QA_trade_stock_post_orders(self, orderLists):

        orderLists = [{
            "nCategory": 0,
            "nOrderType": 4,
            "sInvestorAccount": "p001001001005793",
            "sStockCode": "601988",
            "sPrice": 0,
            "sVolume": 100
        }, {
            "nCategory": 0,
            "nOrderType": 4,
            "sInvestorAccount": "p001001001005793",
            "sStockCode": "601988",
            "sPrice": 0,
            "sVolume": 100
        }]
        pass

    def QA_trade_stock_delete_order(self, client, order_list):
        """
        参数：
        nMarket - 市场代码0:深圳，1:上海
        Orderid - 可撤销的委托单号
        返回值：
        errinfo - 出错时函数抛出的异常信息；
        result - 查询到的数据。

        """

        errinfo, result = client.CancelOrder(
            int(order_list[0]), str(order_list[1]))
        if errinfo != "":
            print(errinfo)
        else:
            print(result)
            return (result)

    def QA_trade_stock_delete_order(self, client, order_list):
        """
        参数：
        nMarket - 市场代码0:深圳，1:上海
        Orderid - 可撤销的委托单号
        返回值：
        errinfo - 出错时函数抛出的异常信息；
        result - 查询到的数据。

        """

        errinfo, result = client.CancelOrders(
            int(order_list[0]), str(order_list[1]))
        if errinfo != "":
            print(errinfo)
        else:
            print(result)
            return (result)

    def QA_trade_stock_get_quote(self, client, stock):
        errinfo, self.result = client.GetQuote(str(stock),)
        if errinfo != "":
            print(errinfo)
        else:
            #print (self.result)
            return self.result

    def QA_trade_stock_get_quotes(self, client, stock_list):
        res = client.GetQuotes(tuple(stock_list))
        for elem in res:
            errinfo, result = elem
            if errinfo != "":
                print (errinfo)
            else:
                print (result)

    def QA_trade_stock_get_stockbars(self, client):
        pass


        #GetSecurityBars(nCategory, nMarket, sStockCode, nStart, nCount)
if __name__ == "__main__":
    st = QA_Stock()
    st.get_config()
    client = st.QA_trade_stock_login()
    st.QA_trade_stock_get_cash(client)
    st.QA_trade_stock_get_stock(client)
    st.QA_trade_stock_get_orders(client)
    holder = st.QA_trade_stock_get_holder(client)
    st.QA_trade_stock_get_quotes(client, ['000001', '601988'])
    #st.QA_trade_stock_delete_order(client,[0,'2 '])
    #st.QA_trade_stock_post_order(client,[0, 4, holder[0], "601988", 0, 100])
