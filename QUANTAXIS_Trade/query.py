# coding=utf-8
import csv
import datetime
import time

import pymongo

from QUANTAXIS_Trade.QA_tradex import QA_Trade_stock_api, QA_Trade_stock_util

st = QA_Trade_stock_api.QA_Stock()
st.get_config()
client = st.QA_trade_stock_login()

st.QA_trade_stock_get_orders(client)
holder = st.QA_trade_stock_get_holder(client)

account = QA_Trade_stock_util.QA_get_account_assest(st, client)
# print(account)

db = pymongo.MongoClient().quantaxis
QA_Trade_stock_util.QA_save_account(st, client, db)
