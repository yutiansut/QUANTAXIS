#coding:utf-8

import msvcrt
import sys
import TradeX

TradeX.OpenTdx()
class QA_Trade_stock():
    def __init__(self):
        self.sHost = ""
        self.nPort = 7708
        self.sVersion = ""
        self.sBranchID =	1
        self.sAccountNo = ""
        self.sTradeAccountNo = ""
        self.sPassword = ""
        self.sTxPassword = ""
    def QA_trade_stock_login(self):
        try:
            client = TradeX.Logon(self.sHost, self.nPort, self.sVersion, self.sBranchID, self.sAccountNo,self.sTradeAccountNo, self.sPassword, self.sTxPassword)
            return client
        except TradeX.error as e:
            print ("error: " + e.message)
            sys.exit(-1)
    def QA_trade_stock_get_account(self):
        pass