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
DEFAULT_SHIPANE_KEY = ''


class SPE_CONFIG():
    def __init__(self, uri=DEFAULT_SHIPANE_URL, key=DEFAULT_SHIPANE_KEY):
        self.key = key
        self.uri = uri


def get_config_SPE():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIGFILE_PATH):
        config.read(CONFIGFILE_PATH)
        try:

            return SPE_CONFIG(config.get('SPE', 'uri'), config.get('SPE', 'key'))

        except configparser.NoSectionError:
            config.add_section('SPE')
            config.set('SPE', 'uri', DEFAULT_SHIPANE_URL)
            config.set('SPE', 'key', DEFAULT_SHIPANE_KEY)
            return SPE_CONFIG()
        except configparser.NoOptionError:
            config.set('SPE', 'uri', DEFAULT_SHIPANE_URL)
            config.set('SPE', 'key', DEFAULT_SHIPANE_KEY)
            return SPE_CONFIG()
        finally:

            with open(CONFIGFILE_PATH, 'w') as f:
                config.write(f)

    else:
        f = open(CONFIGFILE_PATH, 'w')
        config.add_section('SPE')
        config.set('SPE', 'uri', DEFAULT_SHIPANE_URL)
        config.set('SPE', 'key', DEFAULT_SHIPANE_KEY)
        config.write(f)
        f.close()
        return DEFAULT_SHIPANE_URL


class QA_SPEBroker(QA_Broker):
    def __init__(self):

        self.setting = get_config_SPE()
        self._session = requests
        self._endpoint = self.setting.uri
        self.key = self.setting.key

        self.fillorder_headers = ['name', 'datetime', 'towards', 'price',
                                  'amount', 'money', 'trade_id', 'order_id', 'code', 'shareholder', 'other']
        self.holding_headers = ['code', 'name', 'hoding_price', 'price', 'pnl', 'amount',
                                'sell_available', 'pnl_money', 'holdings', 'total_amount', 'lastest_amounts', 'shareholder']
        self.askorder_headers = ['code', 'towards', 'price', 'amount', 'transaction_price',
                                 'transaction_amount', 'status', 'order_time', 'order_id', 'id', 'code', 'shareholders']

    def call(self, func, params=''):
        try:
            if self.key == '':
                uri = '{}/api/v1.0/{}?client={}'.format(
                    self._endpoint, func, params.pop('client'))
            else:
                uri = '{}/api/v1.0/{}?key={}&client={}'.format(
                    self._endpoint, func, self.key, params.pop('client'))
            print(uri)
            response = self._session.get(uri, params)
            text = response.text

            return json.loads(text)
        except Exception as e:
            print(e)
            return None

    def call_post(self, func, params={}):
        if self.key == '':
            uri = '{}/api/v1.0/{}?client={}'.format(
                self._endpoint, func, params.pop('client'))
        else:
            uri = '{}/api/v1.0/{}?key={}&client={}'.format(
                self._endpoint, func, self.key, params.pop('client'))
        response = self._session.post(uri, json=params)
        text = response.text
        return json.loads(text)

    def call_delete(self, func, params=''):

        if self.key == '':
            uri = '{}/api/v1.0/{}?client={}'.format(
                self._endpoint, func, params.pop('client'))
        else:
            uri = '{}/api/v1.0/{}?key={}&client={}'.format(
                self._endpoint, func, self.key, params.pop('client'))

        response = self._session.delete(uri)

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
        try:
            return self.call_post('orders', {
                'client': accounts,
                "action": 'BUY' if order_direction == 1 else 'SELL',
                "symbol": code,
                "type": order_model,
                "priceType": 0 if order_model == ORDER_MODEL.LIMIT else 4,
                "price": price,
                "amount": amount
            })
        except json.decoder.JSONDecodeError:
            print(RuntimeError('TRADE ERROR'))
            return None

    def cancel_order(self, accounts, orderid):
        return self.call_delete('orders/{}'.format(orderid), {
            'client': accounts
        })

    def cancel_all(self, accounts):
        return self.call_delete('orders', {
            'client': accounts
        })


if __name__ == '__main__':
    a = QA_SPEBroker()
    print(a.query_accounts('account:1391'))
    print(a.query_orders('account:1391'))
    print(a.query_orders('account:1391', 'open'))
    """多账户同时下单测试
    """

    print(a.send_order('account:1391', price=8.5))
    print(a.query_orders('account:1391', 'open'))
    print(a.query_orders('account:1391', 'filled'))
    # print(a.send_order('account:141',price=8.95))
    print(a.cancel_all('account:1391'))

    print(a.cancel_order('account:1391', '910954549'))
