import cmd
import configparser
from pprint import pprint
import time
from Event import ActionType, DirectionType
from CTPTraderSpi import CTPTraderSpi
import logging

logging.basicConfig(level=logging.INFO)

account=bytes(input('account'),encoding='UTF-8')
password=bytes(input('password'),encoding='UTF-8')


trader=CTPTraderSpi(b'./co',b'tcp://180.168.146.187:10000',b'9999',account,password)
trader.Connect()
trader.ReqUserLogin()
def buy_open(instrument):


    instrument=bytes(instrument, encoding = "utf8")
    market_data=trader.ReqQryDepthMarketData(instrument)   
    #time.sleep(1)
    if market_data :
        trader.ReqOrderInsert(
                    instrument, DirectionType.BUY, ActionType.OPEN,
                    1, market_data['AskPrice']
                )
    else:
        pass



def sell_close(instrument):

    instrument=bytes(instrument, encoding = "utf8")
    market_data=trader.ReqQryDepthMarketData(instrument)   
    #time.sleep(1)
    if market_data :
        trader.ReqOrderInsert(
                    instrument, DirectionType.SELL, ActionType.CLOSE,
                    1, market_data['BidPrice'],True)



def query_trade():

    data=trader.ReqQryTrade()
    trader.Release()
    return data

def query_order():

    data=trader.ReqQryOrder()
    trader.Release()
    return data

if __name__=="__main__":
    for i in range(1000):
        buy_open('rb1810')
        time.sleep(1)
        sell_close('rb1810')
        time.sleep(1)
    time.sleep(100)
    print(query_order())
    print(query_trade())
