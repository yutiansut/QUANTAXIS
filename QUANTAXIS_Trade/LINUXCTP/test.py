import cmd
import configparser
from pprint import pprint
import time
from Event import ActionType, DirectionType
from CTPTraderSpi import CTPTraderSpi
import logging

logging.basicConfig(level=logging.INFO)

account=input('account')
password=input('password')


trader=CTPTraderSpi(b'./co',b'tcp://180.168.146.187:10000',b'9999',b'{}'.format(account),b'{}'.format(password))
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
                    1, market_data['BidPrice'])



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
        
        buy_open('IF1711')
        time.sleep(1)
        sell_close('IF1711')
        time.sleep(1)
    time.sleep(100)
    print(query_order())
    print(query_trade())
