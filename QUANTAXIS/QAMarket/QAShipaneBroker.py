# coding:utf-8

import base64
import configparser
import json
import os
import urllib
import future
import asyncio
import pandas as pd
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAMarket.common import cn_en_compare
from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS.QAMarket.QAOrderHandler import QA_OrderHandler
from QUANTAXIS.QAUtil.QAParameter import (BROKER_EVENT, ORDER_DIRECTION,
                                          ORDER_MODEL, ORDER_STATUS)
from QUANTAXIS.QAUtil.QASetting import setting_path

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
    """
    1. 查询账户:

    如果有该账户, 返回可用资金和持仓

    如果当前market不存在或异常, 返回False

    2. 查询所有订单:

    如果成功 返回一个DataFrame
    如果失败 返回False

    3. 查询未成交订单

    如果成功 返回DataFrame
    如果失败 返回False

    4. 查询已成交订单

    如果成功 返回DataFramne
    如果失败 返回False


    5. 下单 receive_order/send_order


    receive_order(QAMARKET 用法):
    输入一个QA_ORDER类

    如果下单成功 返回带realorder_id, ORDER_STATUS.QUEUED状态值 的QA_Order
    如果下单失败 返回带 ORDER_STATUS.FAILED状态值的  QA_Order

    send_order(测试用法)



    6. 撤单 cancel_order

    如果撤单成功 返回 True

    如果撤单失败 返回 具体的原因 dict/json格式

    7. 全撤

    如果成功 返回True


    """

    def __init__(self):
        super().__init__()
        self.order_handler = QA_OrderHandler()
        self.setting = get_config_SPE()
        self._session = requests
        self._endpoint = self.setting.uri
        self.key = self.setting.key

        #self.account_headers = ['forzen_cash','balance_available','cash_available','pnl_money_today','total_assets','pnl_holding','market_value','money_available']

    def __repr__(self):
        return ' <QA_BROKER SHIPANE> '

    def run(self, event):
        if event.event_type is BROKER_EVENT.RECEIVE_ORDER:
            self.order_handler.run(event)
            #self.run(QA_Event(event_type=BROKER_EVENT.TRADE, broker=self))
        elif event.event_type is BROKER_EVENT.TRADE:
            """实盘交易部分!!!!! ATTENTION
            这里需要开一个子线程去查询是否成交

            ATTENTION
            """

            event = self.order_handler.run(event)
            event.message = 'trade'
            if event.callback:
                event.callback(event)

        elif event.event_type is BROKER_EVENT.SETTLE:
            self.order_handler.run(event)
            if event.callback:
                event.callback('settle')

    def call(self, func, params=''):
        try:
            if self.key == '':
                uri = '{}/api/v1.0/{}?client={}'.format(
                    self._endpoint, func, params.pop('client'))
            else:
                uri = '{}/api/v1.0/{}?key={}&client={}'.format(
                    self._endpoint, func, self.key, params.pop('client'))
            # print(uri)
            response = self._session.get(uri, params)
            text = response.text

            return json.loads(text)
        except Exception as e:
            print(e)
            # print(uri)
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
        # print(text)
        try:
            if text in ['', '获取提示对话框超时，因为：组件为空']:
                print('success')
                return True

            else:
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
        """查询现金和持仓

        Arguments:
            accounts {[type]} -- [description]

        Returns:
            dict-- {'cash':xxx,'position':xxx}
        """
        try:
            data = self.call("positions", {
                'client': accounts
            })

            if data is not None:
                cash_part = data.get('subAccounts', {}).get('人民币', False)
                if cash_part:
                    cash_available = cash_part.get('可用金额')
                position_part = data.get('dataTable', False)
                if position_part:
                    res = data.get('dataTable', False)
                    if res:
                        hold_headers = res['columns']
                        hold_headers = [cn_en_compare[item]
                                        for item in hold_headers]
                        hold_available = pd.DataFrame(
                            res['rows'], columns=hold_headers)

                return {'cash_available': cash_available, 'hold_available': hold_available.assign(amount=hold_available.amount.apply(float)).loc[:, ['code', 'amount']].set_index('code').amount}
            else:
                print(data)
                return False, 'None ACCOUNT'
        except:
            return False

    def query_clients(self):
        return self.call("clients")

    def query_orders(self, accounts, status='filled'):
        """查询订单

        Arguments:
            accounts {[type]} -- [description]

        Keyword Arguments:
            status {str} -- 'open' 待成交 'filled' 成交 (default: {'filled'})

        Returns:
            [type] -- [description]
        """
        try:
            data = self.call("orders", {
                'client': accounts,
                'status': status
            })

            if data is not None:
                orders = data.get('dataTable', False)

                order_headers = orders['columns']
                order_headers = [cn_en_compare[item] for item in order_headers]
                order_all = pd.DataFrame(
                    orders['rows'], columns=order_headers).assign(account_cookie=accounts)
                if status is 'filled':
                    return order_all.loc[:, self.dealstatus_headers].set_index(['account_cookie', 'realorder_id']).sort_index()
                else:
                    return order_all.loc[:, self.orderstatus_headers].set_index(['account_cookie', 'realorder_id']).sort_index()
            else:
                print('response is None')
                return False
        except Exception as e:
            print(e)
            return False

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

    def receive_order(self, event):
        order = event.order
        res = self.send_order(accounts=order.account_cookie, code=order.code,
                              amount=order.amount, order_direction=order.towards, order_model=order.order_model)
        try:
            if res is not None and 'id' in res.keys():

                order.realorder_id = res['id']
                order.status = ORDER_STATUS.QUEUED
                #order.text = 'SUCCESS'
                print('success receive order {}'.format(order.realorder_id))
                return order

        except:
            order.status = ORDER_STATUS.FAILED
            print('FAILED FOR CREATE ORDER {} {}'.format(
                order.account_cookie, order.status))
            print(res)

            return order
        #self.dealer.deal(order, self.market_data)


if __name__ == '__main__':
    a = QA_SPEBroker()

    print('查询账户')
    acc = 'account:141'
    print(a.query_positions(acc))
    print('查询所有订单')
    print(a.query_orders(acc, ''))
    print('查询未成交订单')
    print(a.query_orders(acc, 'open'))
    print('查询已成交订单')
    print(a.query_orders(acc, 'filled'))
    """多账户同时下单测试
    """
    print('下单测试')
    res = a.send_order(acc, price=9)
    #a.send_order(acc, price=9)
    #a.send_order(acc, price=9)
    # print(res)
    print('查询新的未成交订单')
    print(a.query_orders(acc, 'open'))

    print('撤单')

    print(a.cancel_order(acc, res['id']))
    print('查询已成交订单')
    print(a.query_orders(acc, 'filled'))
    # print(a.send_order('account:141',price=8.95))
    print('一键全部撤单')
    print(a.cancel_all(acc))

    #print(a.cancel_order('account:141', '1703'))
