# coding:utf-8


import requests
import json
import urllib
import base64
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from QUANTAXIS.QAMarket.QABroker import QA_Broker
try:
    from pytdx.log import log
except ImportError:
    def log(x): 
        return None


class SPETradeApi(QA_Broker):
    def __init__(self, endpoint="http://127.0.0.1:8888"):

        self._endpoint = endpoint
        self._session = requests.Session()

    def call(self, func, params=None):

        json_obj = {
            "func": func
        }

        if params is not None:
            json_obj["params"] = params

        response = self._session.post(self._endpoint, json=json_obj)

        text = response.text

        return json.loads(text)

    def data_to_df(self, result):
        if 'data' in result:
            data = result['data']
            return pd.DataFrame(data=data)

    #------ functions

    def ping(self):

        return self.call("ping", {})

    def logon(self, ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password):
        return self.call("logon", {
            "ip": ip,
            "port": port,
            "version": version,
            "yyb_id": yyb_id,
            "account_no": account_id,
            "trade_account": trade_account,
            "jy_password": jy_passwrod,
            "tx_password": tx_password
        })

    def logoff(self, client_id):
        return self.call("logoff", {
            "client_id": client_id
        })

    def query_data(self, client_id, category):
        return self.call("query_data", {
            "client_id": client_id,
            "category": category
        })

    def send_order(self, client_id, category, price_type, gddm, zqdm, price, quantity):
        return self.call("send_order", {
            'client_id': client_id,
            'category': category,
            'price_type': price_type,
            'gddm': gddm,
            'zqdm': zqdm,
            'price': price,
            'quantity': quantity
        })

    def cancel_order(self, client_id, exchange_id, hth):
        return self.call("cancel_order", {
            'client_id': client_id,
            'exchange_id': exchange_id,
            'hth': hth
        })

    def get_quote(self, client_id, code):
        return self.call("get_quote", {
            'client_id': client_id,
            'code': code,
        })

    def repay(self, client_id, amount):
        return self.call("repay", {
            'client_id': client_id,
            'amount': amount
        })

    def receive_order(self, event):
        """
        0 限价委托； 上海限价委托 / 深圳限价委托
        1 市价委托(深圳对方最优价格)
        2 市价委托(深圳本方最优价格)    
        3 市价委托(深圳即时成交剩余撤销)
        4 市价委托(上海五档即成剩撤 / 深圳五档即成剩撤)
        5 市价委托(深圳全额成交或撤销)
        6 市价委托(上海五档即成转限价)
        """
        return self.send_order(event.client_id, event.category, event.price_type,event.gddm,event.zqdm,event.price,event.quantity)
        #client_id, category, price_type, gddm, zqdm, price, quantity

    def run(self,event):
        pass

    
if __name__ == "__main__":
    import os
    api = TdxTradeApi(endpoint="http://10.11.5.175:10092/api",
                      enc_key=b"4f1cf3fec4c84c84", enc_iv=b"0c78abc083b011e7")
    #api = TdxTradeApi(endpoint="http://10.11.5.175:10092/api")
    print("---Ping---")
    result = api.ping()
    print(result)

    print("---登入---")
    acc = os.getenv("TDX_ACCOUNT", "")
    password = os.getenv("TDX_PASS", "")
    result = api.logon("202.108.253.186", 7708,
                       "8.23", 32,
                       acc, acc, password, "")

    print(result)

    if result["success"]:
        client_id = result["data"]["client_id"]

        for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15):
            print("---查询信息 cate=%d--" % i)
            print(api.data_to_df(api.query_data(client_id, i)))

        print("---查询报价---")
        print(api.data_to_df(api.get_quote(client_id, '600315')))

        print("---登出---")
        print(api.logoff(client_id))
