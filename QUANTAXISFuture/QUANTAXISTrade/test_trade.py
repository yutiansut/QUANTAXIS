#coding:utf-8
from QA_trade_stock.QA_trade_stock_api import QA_Trade_stock


trade=QA_Trade_stock()
trade.get_config()
client=trade.QA_trade_stock_login()
