import json
import requests
import sys
import pymongo
import talib
from factor import *

initFund=100000
fund=[]
# firstly, try something of bid price
trade=requests.get("http://localhost:3000/backtest/ts?bidCode=000001&bidTime=2001-01-04&bidPrice=4.08")
#firstLine = trade.readline() 
assert trade.text == "success"

class account():
    def _init_(self):
        fund[0]=initFund
    def fund(self):
        return






#urllib.urlopen("http://localhost:3000/backtest/save?")