import json
import urllib
import sys
import pymongo


fund=100000;




trade=urllib.urlopen("http://localhost:3000/backtest/ts?bidCode=000001&bidTime=2001-01-04&bidPrice=4.08")
firstLine = trade.readline() 
print firstLine