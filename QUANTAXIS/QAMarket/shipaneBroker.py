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
        self._session = requests

    def call(self, func, params=''):
        print('{}/api/v1.0/{}'.format(self._endpoint, func))
        print(params)
        response = self._session.get(
            '{}/api/v1.0/{}'.format(self._endpoint, func), params)

        text = response.text
        
        return json.loads(text)

    def call_post(self,func,params=''):
        print(params)
        response = self._session.post(
            '{}/api/v1.0/{}'.format(self._endpoint, func), params)

        text = response.text
        print(text)
        return json.loads(text)
    def call_delete(self,func,params=''):
        print(params)
        response = self._session.delete(
            '{}/api/v1.0/{}'.format(self._endpoint, func))

        text = response.text
        print(text)
        try:
            return json.loads(text)
        except:
            return text

    def data_to_df(self, result):
        return pd.DataFrame(data=result)

    #------ functions

    def ping(self):
        return self.call("ping", {})

    def query_accounts(self, accounts):
        return self.call("accounts", {
            'client':accounts
        })
    def query_positions(self, accounts):
        return self.call("positions", {
            'client':accounts
        })
    def query_orders(self,accounts,status='filled'):
        return self.call("orders", {
            'client':accounts,
            'status':status
        })
    def send_order(self,accounts):
        return self.call_post('orders',json.dumps({
            'client':accounts,
            "action": "BUY",
            "symbol" : "000001",
            "type": "LIMIT",
            "priceType" : 0,
            "price" : 9.26,
            "amount" : 100

        }))
    def cancel_order(self,accounts,orderid):
        return self.call_delete('orders/{}'.format(orderid),json.dumps({
            'client':accounts
        }))
    def cancel_all(self):
        return self.call_delete('orders')
        


if __name__=='__main__':
    a=SPETradeApi()
    a.query_accounts('account:1363350141')
    a.query_orders('account:141')
    a.query_orders('account:141','open')
    a.send_order('account:141')
    a.cancel_all()
    #a.cancel_order('account:141','919')