#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msvcrt
import sys
import configparser
import os
sys.path.append(os.path.realpath('.'))

import TradeX

TradeX.OpenTdx()


class QA_Stock():
    
    def get_config(self):
        config = configparser.ConfigParser()
        try:
            config.read('setting.ini')
            self.sHost = config['trade']['host']
            self.nPort = config['trade']['port']
            self.sVersion = config['trade']['version']
            self.sBranchID = config['trade']['branchID']
            self.sAccountNo = config['trade']['accountNo']
            self.sTradeAccountNo =config['trade']['tradeAccountNo']
            self.sPassword = int(config['trade']['password'])
            self.sTxPassword = int(config['trade']['txPassword'])

            
        except:
            print('error with read setting files')

    def QA_trade_stock_login(self):
        try:
            TradeX.OpenTdx()
            client = TradeX.Logon(str(self.sHost), int(self.nPort), str(self.sVersion), int(self.sBranchID),
                                  str(self.sAccountNo), str(self.sTradeAccountNo),
                                  str(self.sPassword), str(self.sTxPassword))
            return client
        except TradeX.error as e:
            print("error: " + e.message)
            sys.exit(-1)

    def QA_trade_stock_get_account(self, client):
        self.nCategory = 0

        errinfo, self.result = client.QueryData(self.nCategory)
        if errinfo != "":
            print(errinfo)
        else:
            print(self.result)
            return self.result


if __name__ == "__main__":
    st = QA_Stock()
    st.get_config()
    client = st.QA_trade_stock_login()
    st.QA_trade_stock_get_account(client)
