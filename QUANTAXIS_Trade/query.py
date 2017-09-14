# coding=utf-8
from QA_trade_stock import QA_Trade_stock_api,QA_Trade_stock_util

import pymongo
import csv
import time
import datetime






st = QA_Trade_stock_api.QA_Stock()
st.get_config()
client = st.QA_trade_stock_login()

st.QA_trade_stock_get_orders(client)
holder = st.QA_trade_stock_get_holder(client)

account = QA_Trade_stock_util.QA_get_account_assest(st, client)
# print(account)

db = pymongo.MongoClient().quantaxis
QA_Trade_stock_util.QA_save_account(st, client, db)
