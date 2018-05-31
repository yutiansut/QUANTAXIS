# coding:utf-8

import os
import base64
import configparser
import json
import urllib

import pandas as pd
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS.QAUtil.QASetting import setting_path

try:
    from pytdx.log import log
except ImportError:
    def log(x):
        return None

CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')
DEFAULT_SHIPANE_URL = 'http://127.0.0.1:8888'


def get_config_SPE():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIGFILE_PATH):
        config.read(CONFIGFILE_PATH)
        try:
            return config.get('SPE', 'uri')
        except configparser.NoSectionError:
            config.add_section('SPE')
            config.set('SPE', 'uri', DEFAULT_SHIPANE_URL)
            return DEFAULT_SHIPANE_URL
        except configparser.NoOptionError:
            config.set('SPE', 'uri', DEFAULT_SHIPANE_URL)
            return DEFAULT_SHIPANE_URL
        finally:

            with open(CONFIGFILE_PATH, 'w') as f:
                config.write(f)

    else:
        f = open(CONFIGFILE_PATH, 'w')
        config.add_section('SPE')
        config.set('SPE', 'uri', DEFAULT_SHIPANE_URL)
        config.write(f)
        f.close()
        return DEFAULT_SHIPANE_URL


class SPETradeApi(QA_Broker):
    def __init__(self, endpoint=get_config_SPE()):

        self._endpoint = endpoint
        self._session = requests.Session()

    def call(self, func, params=''):

        response = self._session.post(
            '{}/api/v1.0/{}'.format(self._endpoint, func), params)

        text = response.text

        return json.loads(text)

    def data_to_df(self, result):
        return pd.DataFrame(data=result)

    #------ functions

    def ping(self):
        return self.call("ping", {})

    def query_accounts(self, accounts):
        return self.call("accounts", {
        })

    def query_holdings(self):
        return self.call('positions', {})

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
        return self.send_order(event.client_id, event.category, event.price_type, event.gddm, event.zqdm, event.price, event.quantity)
        #client_id, category, price_type, gddm, zqdm, price, quantity

    def run(self, event):
        pass


if __name__ == "__main__":
    import os
    api = SPETradeApi(endpoint="http://10.11.5.175:10092/api")
    #api = SPETradeApi(endpoint="http://10.11.5.175:10092/api")
    print("---Ping---")
    result = api.ping()

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
