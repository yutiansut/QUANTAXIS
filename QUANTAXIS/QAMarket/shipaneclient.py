# -*- coding: utf-8 -*-

import copy
import datetime
import re
from enum import Enum
from urllib.parse import urlencode

import lxml.html
import pandas as pd
import requests
import six
import tushare as ts
from lxml import etree
from pandas.compat import StringIO
from requests import Request
from requests.auth import HTTPBasicAuth


class MediaType(Enum):
    DEFAULT = 'application/json'
    JOIN_QUANT = 'application/vnd.joinquant+json'


class ConnectionMethod(Enum):
    DIRECT = 'DIRECT'
    PROXY = 'PROXY'


class Client(object):
    KEY_REGEX = r'key=([^&]*)'

    def __init__(self, logger=None, **kwargs):
        if logger is not None:
            self._logger = logger
        else:
            import logging
            self._logger = logging.getLogger(__name__)
        self._connection_method = ConnectionMethod[kwargs.pop('connection_method', 'DIRECT')]
        if self._connection_method is ConnectionMethod.DIRECT:
            self._host = kwargs.pop('host', 'localhost')
            self._port = kwargs.pop('port', 8888)
        else:
            self._proxy_base_url = kwargs.pop('proxy_base_url')
            self._proxy_username = kwargs.pop('proxy_username')
            self._proxy_password = kwargs.pop('proxy_password')
            self._instance_id = kwargs.pop('instance_id')
        self._base_url = self.__create_base_url()
        self._key = kwargs.pop('key', '')
        self._client = kwargs.pop('client', '')
        self._timeout = kwargs.pop('timeout', (5.0, 10.0))

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        self._port = value

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def get_statuses(self, timeout=None):
        request = Request('GET', self.__create_url(None, 'statuses'))
        self.__send_request(request, timeout)

    def get_account(self, client=None, timeout=None):
        request = Request('GET', self.__create_url(client, 'accounts'))
        response = self.__send_request(request, timeout)
        return response.json()

    def get_positions(self, client=None, media_type=MediaType.DEFAULT, timeout=None):
        request = Request('GET', self.__create_url(client, 'positions'))
        request.headers['Accept'] = media_type.value
        response = self.__send_request(request, timeout)
        json = response.json()
        if media_type == MediaType.DEFAULT:
            sub_accounts = pd.DataFrame(json['subAccounts']).T
            positions = pd.DataFrame(json['dataTable']['rows'], columns=json['dataTable']['columns'])
            portfolio = {'sub_accounts': sub_accounts, 'positions': positions}
            return portfolio
        return json

    def get_orders(self, client=None, status="", timeout=None):
        request = Request('GET', self.__create_url(client, 'orders', status=status))
        response = self.__send_request(request, timeout)
        json = response.json()
        df = pd.DataFrame(json['dataTable']['rows'], columns=json['dataTable']['columns'])
        return df

    def buy(self, client=None, timeout=None, **kwargs):
        kwargs['action'] = 'BUY'
        return self.__execute(client, timeout, **kwargs)

    def sell(self, client=None, timeout=None, **kwargs):
        kwargs['action'] = 'SELL'
        return self.__execute(client, timeout, **kwargs)

    def ipo(self, client=None, timeout=None, **kwargs):
        kwargs['action'] = 'IPO'
        return self.__execute(client, timeout, **kwargs)

    def execute(self, client=None, timeout=None, **kwargs):
        return self.__execute(client, timeout, **kwargs)

    def cancel(self, client=None, order_id=None, timeout=None):
        request = Request('DELETE', self.__create_order_url(client, order_id))
        self.__send_request(request, timeout)

    def cancel_all(self, client=None, timeout=None):
        request = Request('DELETE', self.__create_order_url(client))
        self.__send_request(request, timeout)

    def query(self, client=None, navigation=None, timeout=None):
        request = Request('GET', self.__create_url(client, '', navigation=navigation))
        response = self.__send_request(request, timeout)
        json = response.json()
        df = pd.DataFrame(json['dataTable']['rows'], columns=json['dataTable']['columns'])
        return df

    def query_new_stocks(self):
        return self.__query_new_stocks()

    def query_convertible_bonds(self):
        return self.__query_convertible_bonds()

    def purchase_new_stocks(self, client=None, timeout=None):
        today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        df = self.query_new_stocks()
        df = df[(df.ipo_date == today)]
        self._logger.info('今日有[{}]支可申购新股'.format(len(df)))
        for index, row in df.iterrows():
            try:
                order = {
                    'symbol': row['xcode'],
                    'price': row['price'],
                    'amountProportion': 'ALL'
                }
                self._logger.info('申购新股：{}'.format(order))
                self.ipo(client, timeout, **order)
            except Exception as e:
                self._logger.error(
                    '客户端[{}]申购新股[{}({})]失败\n{}'.format((client or self._client), row['name'], row['code'], e))

    def purchase_convertible_bonds(self, client=None, timeout=None):
        today = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        df = self.query_convertible_bonds()
        df = df[(df.ipo_date == today)]
        self._logger.info('今日有[{}]支可申购转债'.format(len(df)))
        for index, row in df.iterrows():
            try:
                order = {
                    'symbol': row['xcode'],
                    'price': 100,
                    'amountProportion': 'ALL'
                }
                self._logger.info('申购转债：{}'.format(order))
                self.buy(client, timeout, **order)
            except Exception as e:
                self._logger.error(
                    '客户端[{}]申购转债[{}({})]失败\n{}'.format((client or self._client), row['bname'], row['xcode'], e))

    def create_adjustment(self, client=None, request_json=None, timeout=None):
        request = Request('POST', self.__create_url(client, 'adjustments'), json=request_json)
        request.headers['Content-Type'] = MediaType.JOIN_QUANT.value
        response = self.__send_request(request, timeout)
        json = response.json()
        return json

    def start_clients(self, timeout=None):
        request = Request('PUT', self.__create_url(None, 'clients'))
        self.__send_request(request, timeout)

    def shutdown_clients(self, timeout=None):
        request = Request('DELETE', self.__create_url(None, 'clients'))
        self.__send_request(request, timeout)

    def __execute(self, client=None, timeout=None, **kwargs):
        if not kwargs.get('type'):
            kwargs['type'] = 'LIMIT'
        request = Request('POST', self.__create_order_url(client), json=kwargs)
        response = self.__send_request(request)
        return response.json()

    def __query_new_stocks(self):
        DATA_URL = 'http://vip.stock.finance.sina.com.cn/corp/view/vRPD_NewStockIssue.php?page=1&cngem=0&orderBy=NetDate&orderType=desc'
        html = lxml.html.parse(DATA_URL)
        res = html.xpath('//table[@id=\"NewStockTable\"]/tr')
        if six.PY2:
            sarr = [etree.tostring(node) for node in res]
        else:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        sarr = ''.join(sarr)
        sarr = sarr.replace('<font color="red">*</font>', '')
        sarr = '<table>%s</table>' % sarr
        df = pd.read_html(StringIO(sarr), skiprows=[0, 1])[0]
        df = df.select(lambda x: x in [0, 1, 2, 3, 7], axis=1)
        df.columns = ['code', 'xcode', 'name', 'ipo_date', 'price']
        df['code'] = df['code'].map(lambda x: str(x).zfill(6))
        df['xcode'] = df['xcode'].map(lambda x: str(x).zfill(6))
        return df

    def __query_convertible_bonds(self):
        df = ts.new_cbonds()
        return df

    def __create_order_url(self, client=None, order_id=None, **params):
        return self.__create_url(client, 'orders', order_id, **params)

    def __create_url(self, client, resource, resource_id=None, **params):
        all_params = copy.deepcopy(params)
        all_params.update(client=(client or self._client))
        all_params.update(key=(self._key or ''))
        if resource_id is None:
            path = '/{}'.format(resource)
        else:
            path = '/{}/{}'.format(resource, resource_id)
        url = '{}{}?{}'.format(self._base_url, path, urlencode(all_params))
        return url

    def __create_base_url(self):
        if self._connection_method is ConnectionMethod.DIRECT:
            return 'http://{}:{}'.format(self._host, self._port)
        else:
            return self._proxy_base_url

    def __send_request(self, request, timeout=None):
        if self._connection_method is ConnectionMethod.PROXY:
            request.auth = HTTPBasicAuth(self._proxy_username, self._proxy_password)
            request.headers['X-Instance-ID'] = self._instance_id
        prepared_request = request.prepare()
        self.__log_request(prepared_request)
        with requests.sessions.Session() as session:
            response = session.send(prepared_request, timeout=(timeout or self._timeout))
        self.__log_response(response)
        response.raise_for_status()
        return response

    def __log_request(self, prepared_request):
        url = self.__eliminate_privacy(prepared_request.path_url)
        if prepared_request.body is None:
            self._logger.info('Request:\n{} {}'.format(prepared_request.method, url))
        else:
            self._logger.info('Request:\n{} {}\n{}'.format(prepared_request.method, url, prepared_request.body))

    def __log_response(self, response):
        message = u'Response:\n{} {}\n{}'.format(response.status_code, response.reason, response.text)
        if response.status_code == 200:
            self._logger.info(message)
        else:
            self._logger.error(message)

    @classmethod
    def __eliminate_privacy(cls, url):
        match = re.search(cls.KEY_REGEX, url)
        if match is None:
            return url
        key = match.group(1)
        masked_key = '*' * len(key)
        url = re.sub(cls.KEY_REGEX, "key={}".format(masked_key), url)
        return url
