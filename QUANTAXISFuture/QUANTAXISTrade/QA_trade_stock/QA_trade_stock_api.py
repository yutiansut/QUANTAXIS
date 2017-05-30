#!/usr/bin/env python
# -*- coding: utf-8 -*-

import msvcrt
import sys
import TradeX
import ConfigParser
TradeX.OpenTdx()



class QA_Trade_stock():
    def get_config(self):
        config=ConfigParser.ConfigParser()
        try:
            with open("setting.cfg","rw") as cfgfile: 
                config.readfp(cfgfile)
                self.sHost =config.get("trade","host")
                self.nPort =config.get("trade","port")
                self.sVersion =config.get("trade","version")
                self.sBranchID =config.get("trade","branchID")
                self.sAccountNo =config.get("trade","accountNo")
                self.sTradeAccountNo =config.get("trade","tradeAccountNo")
                self.sPassword=config.get("trade","password")
                self.sTxPassword =config.get("trade","txPassword")
        except:
            print('error with read setting files')
    def QA_trade_stock_login(self):
        try:
            client = TradeX.Logon(self.sHost, self.nPort, self.sVersion, self.sBranchID, self.sAccountNo,self.sTradeAccountNo, self.sPassword, self.sTxPassword)
            return client
        except TradeX.error as e:
            print ("error: " + e.message)
            sys.exit(-1)
    def QA_trade_stock_get_account(self):
        pass