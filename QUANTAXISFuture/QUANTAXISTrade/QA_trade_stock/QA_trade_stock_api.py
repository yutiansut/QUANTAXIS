#coding:utf-8

import msvcrt
import sys
import TradeX

TradeX.OpenTdx()
class QA_Trade_stock():
    def __init__(self):
        sHost = ""
        nPort = 7708
        sVersion = ""
        sBranchID =	1
        sAccountNo = ""
        sTradeAccountNo = ""
        sPassword = ""
        sTxPassword = ""
    def QA_trade_stock_login(self):
        try:
            self.client = TradeX.Logon(self.sHost, self.nPort, self.sVersion, self.sBranchID, self.sAccountNo,self.sTradeAccountNo, self.sPassword, self.sTxPassword)
            return self.client
        except TradeX.error as e:
            print ("error: " + e.message)
            sys.exit(-1)
    def QA_trade_stock_get_account(self):
        pass