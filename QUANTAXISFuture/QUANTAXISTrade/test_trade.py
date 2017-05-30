#coding:utf-8
from QA_trade_stock.QA_trade_stock_api import QA_Stock


trade=QA_Stock()
trade.get_config()
client=trade.QA_trade_stock_login()

trade.QA_trade_stock_get_account(client)
