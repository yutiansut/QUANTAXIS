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
from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION, ORDER_MODEL

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
        self.fillorder_headers = ['name', 'datetime', 'towards', 'price',
                                  'amount', 'money', 'trade_id', 'order_id', 'code', 'shareholder', 'other']
        self.holding_headers = ['code', 'name', 'hoding_price', 'price', 'pnl', 'amount',
                                'sell_available', 'pnl_money', 'holdings', 'total_amount', 'lastest_amounts', 'shareholder']
        self.askorder_headers = ['code', 'towards', 'price', 'amount', 'transaction_price',
                                 'transaction_amount', 'status', 'order_time', 'order_id', 'id', 'code', 'shareholders']

    def call(self, func, params=''):
        response = self._session.get(
            '{}/api/v1.0/{}'.format(self._endpoint, func), params)

        text = response.text

        return json.loads(text)

    def call_post(self, func, params={}):
        uri = '{}/api/v1.0/{}?client={}'.format(
            self._endpoint, func, params.pop('client'))
        response = self._session.post(uri, json=params)
        text = response.text
        return json.loads(text)

    def call_delete(self, func, params=''):
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
            'client': accounts
        })

    def query_positions(self, accounts):
        return self.call("positions", {
            'client': accounts
        })

    def query_clients(self):
        return self.call("clients")

    def query_orders(self, accounts, status='filled'):
        """查询订单
        
        Arguments:
            accounts {[type]} -- [description]
        
        Keyword Arguments:
            status {str} -- [description] (default: {'filled'})
        
        Returns:
            [type] -- [description]
        """

        return self.call("orders", {
            'client': accounts,
            'status': status
        })

    def send_order(self, accounts, code='000001', price=9, amount=100, order_direction=ORDER_DIRECTION.BUY, order_model=ORDER_MODEL.LIMIT):
        """[summary]

        Arguments:
            accounts {[type]} -- [description]
            code {[type]} -- [description]
            price {[type]} -- [description]
            amount {[type]} -- [description]

        Keyword Arguments:
            order_direction {[type]} -- [description] (default: {ORDER_DIRECTION.BUY})
            order_model {[type]} -- [description] (default: {ORDER_MODEL.LIMIT})



        priceType 可选择： 上海交易所：

            0 - 限价委托
            4 - 五档即时成交剩余撤销
            6 - 五档即时成交剩余转限

        深圳交易所：

            0 - 限价委托
            1 - 对手方最优价格委托
            2 - 本方最优价格委托
            3 - 即时成交剩余撤销委托
            4 - 五档即时成交剩余撤销
            5 - 全额成交或撤销委托

        Returns:
            [type] -- [description]
        """

        return self.call_post('orders', {
            'client': accounts,
            "action": 'BUY' if order_direction == 1 else 'SELL',
            "symbol": code,
            "type": order_model,
            "priceType": 0 if order_model == ORDER_MODEL.LIMIT else 4,
            "price": price,
            "amount": amount

        })

    def cancel_order(self, accounts, orderid):
        return self.call_delete('orders/{}'.format(orderid), json.dumps({
            'client': accounts
        }))

    def cancel_all(self):
        return self.call_delete('orders')


if __name__ == '__main__':
    a = SPETradeApi()
    a.query_accounts('account:1391')
    a.query_orders('account:1391')
    a.query_orders('account:1391', 'open')
    #a.send_order('account:141')

    #a.cancel_all()

    # a.cancel_order('account:141','919')
