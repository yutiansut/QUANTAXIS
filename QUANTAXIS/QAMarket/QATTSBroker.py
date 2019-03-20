# coding:utf-8


import requests
import json
import urllib
import base64
import datetime
import pandas as pd
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from QUANTAXIS.QAMarket.QAOrderHandler import QA_OrderHandler
from QUANTAXIS.QAFetch.QATdx import (QA_fetch_get_future_day,
                                     QA_fetch_get_future_min,
                                     QA_fetch_get_index_day,
                                     QA_fetch_get_index_min,
                                     QA_fetch_get_stock_day,
                                     QA_fetch_get_stock_min)
from QUANTAXIS.QAMarket.common import (
    cn_en_compare,
    order_status_cn_en,
    trade_towards_cn_en
)
from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS import QAFetch
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION, MARKET_TYPE, ORDER_MODEL, TRADE_STATUS, FREQUENCE, BROKER_EVENT, BROKER_TYPE, MARKET_EVENT


class QA_TTSBroker(QA_Broker):
    def __init__(self, endpoint="http://127.0.0.1:10092/api", encoding="utf-8", enc_key=None, enc_iv=None):
        super().__init__()
        self.name = BROKER_TYPE.TTS
        self.order_handler =  QA_OrderHandler()
        self._endpoint = endpoint
        self._encoding = "utf-8"
        if enc_key == None or enc_iv == None:
            self._transport_enc = False
            self._transport_enc_key = None
            self._transport_enc_iv = None
            self._cipher = None
        else:
            self._transport_enc = True
            self._transport_enc_key = enc_key
            self._transport_enc_iv = enc_iv
            backend = default_backend()
            self._cipher = Cipher(algorithms.AES(
                enc_key), modes.CBC(enc_iv), backend=backend)

        self._session = requests.Session()
        self.client_id = 0
        self.gddm_sh = 0 #上海股东代码
        self.gddm_sz = 0 #深圳股东代码

        self.fetcher = {(MARKET_TYPE.STOCK_CN, FREQUENCE.DAY): QA_fetch_get_stock_day,
                       (MARKET_TYPE.STOCK_CN, FREQUENCE.FIFTEEN_MIN): QA_fetch_get_stock_min,
                       (MARKET_TYPE.STOCK_CN, FREQUENCE.ONE_MIN): QA_fetch_get_stock_min,
                       (MARKET_TYPE.STOCK_CN, FREQUENCE.FIVE_MIN): QA_fetch_get_stock_min,
                       (MARKET_TYPE.STOCK_CN, FREQUENCE.THIRTY_MIN): QA_fetch_get_stock_min,
                       (MARKET_TYPE.STOCK_CN, FREQUENCE.SIXTY_MIN): QA_fetch_get_stock_min,
                       (MARKET_TYPE.INDEX_CN, FREQUENCE.DAY): QA_fetch_get_index_day,
                       (MARKET_TYPE.INDEX_CN, FREQUENCE.FIFTEEN_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.INDEX_CN, FREQUENCE.ONE_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.INDEX_CN, FREQUENCE.FIVE_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.INDEX_CN, FREQUENCE.THIRTY_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.INDEX_CN, FREQUENCE.SIXTY_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.FUND_CN, FREQUENCE.DAY): QA_fetch_get_index_day,
                       (MARKET_TYPE.FUND_CN, FREQUENCE.FIFTEEN_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.FUND_CN, FREQUENCE.ONE_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.FUND_CN, FREQUENCE.FIVE_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.FUND_CN, FREQUENCE.THIRTY_MIN): QA_fetch_get_index_min,
                       (MARKET_TYPE.FUND_CN, FREQUENCE.SIXTY_MIN): QA_fetch_get_index_min}

    def call(self, func, params=None):

        json_obj = {
            "func": func
        }

        if params is not None:
            json_obj["params"] = params

        if self._transport_enc:
            data_to_send = self.encrypt(json_obj)
            response = self._session.post(self._endpoint, data=data_to_send)
        else:
            response = self._session.post(self._endpoint, json=json_obj)
        response.encoding = self._encoding
        text = response.text

        if self._transport_enc:
            decoded_text = self.decrypt(text)
            #print(decoded_text)
            return json.loads(decoded_text)
        else:
            return json.loads(text)

    def encrypt(self, source_obj):
        encrypter = self._cipher.encryptor()
        source = json.dumps(source_obj)
        source = source.encode(self._encoding)
        need_to_padding = 16 - (len(source) % 16)
        if need_to_padding > 0:
            source = source + b'\x00' * need_to_padding
        enc_data = encrypter.update(source) + encrypter.finalize()
        b64_enc_data = base64.encodebytes(enc_data)
        return urllib.parse.quote(b64_enc_data)

    def decrypt(self, source):
        decrypter = self._cipher.decryptor()
        source = urllib.parse.unquote(source)
        source = base64.decodebytes(source.encode("utf-8"))
        data_bytes = decrypter.update(source) + decrypter.finalize()
        return data_bytes.rstrip(b"\x00").decode(self._encoding)

    def data_to_df(self, result):
        if 'data' in result:
            data = result['data']
            df = pd.DataFrame(data=data)
            df.rename(columns=lambda x: cn_en_compare[x] if x in cn_en_compare else x, inplace=True)
            if hasattr(df, 'towards'):
                df.towards = df.towards.apply(lambda x: trade_towards_cn_en[x] if x in trade_towards_cn_en else x)
            if hasattr(df, 'status'):
                df.status = df.status.apply(lambda x: order_status_cn_en[x] if x in order_status_cn_en else x)
            if hasattr(df, 'order_time'):
                df.order_time = df.order_time.apply(
                    lambda x: '{} {}'.format(
                        datetime.date.today().strftime('%Y-%m-%d'),
                        datetime.datetime.strptime(x, '%H%M%S').strftime('%H:%M:%S')))
            if hasattr(df, 'trade_time'):
                df.trade_time = df.trade_time.apply(
                    lambda x: '{} {}'.format(
                        datetime.date.today().strftime('%Y-%m-%d'),
                        datetime.datetime.strptime(x, '%H%M%S').strftime('%H:%M:%S')))
            if hasattr(df, 'amount'):
                df.amount = df.amount.apply(pd.to_numeric)
            if hasattr(df, 'price'):
                df.price = df.price.apply(pd.to_numeric)
            if hasattr(df, 'money'):
                df.money = df.money.apply(pd.to_numeric)
            if hasattr(df, 'trade_amount'):
                df.trade_amount = df.trade_amount.apply(pd.to_numeric)
            if hasattr(df, 'trade_price'):
                df.trade_price = df.trade_price.apply(pd.to_numeric)
            if hasattr(df, 'trade_money'):
                df.trade_money = df.trade_money.apply(pd.to_numeric)
            if hasattr(df, 'order_price'):
                df.order_price = df.order_price.apply(pd.to_numeric)
            if hasattr(df, 'order_amount'):
                df.order_amount = df.order_amount.apply(pd.to_numeric)
            if hasattr(df, 'order_money'):
                df.order_money = df.order_money.apply(pd.to_numeric)
            if hasattr(df, 'cancel_amount'):
                df.cancel_amount = df.cancel_amount.apply(pd.to_numeric)
            return df
        else:
            return pd.DataFrame()

    #------ functions

    def ping(self):

        return self.call("ping", {})

    def logon(self, ip, port, version, yyb_id, account_cookie, trade_account, jy_passwrod, tx_password):
        data = self.call("logon", {
            "ip": ip,
            "port": port,
            "version": version,
            "yyb_id": yyb_id,
            "account_no": account_cookie,
            "trade_account": trade_account,
            "jy_password": jy_passwrod,
            "tx_password": tx_password
        })
        if data['success']:
            self.client_id = data["data"]["client_id"]
            self.gddm_sh = self.query_data(5)['data'][0]['股东代码']
            self.gddm_sz = self.query_data(5)['data'][1]['股东代码']
            print('上海股东代码:%s,深圳股东代码:%s',self.gddm_sh,self.gddm_sz)
        return data

    def logoff(self):
        return self.call("logoff", {
            "client_id": self.client_id
        })

    def query_data(self,  category):
        return self.call("query_data", {
            "client_id": self.client_id,
            "category": category
        })

    def send_order(self,  code, price, amount, towards, order_model, market=None):
        """下单

        Arguments:
            code {[type]} -- [description]
            price {[type]} -- [description]
            amount {[type]} -- [description]
            towards {[type]} -- [description]
            order_model {[type]} -- [description]
            market:市场，SZ 深交所，SH 上交所

        Returns:
            [type] -- [description]
        """

        towards = 0 if towards == ORDER_DIRECTION.BUY else 1
        if order_model == ORDER_MODEL.MARKET:
            order_model = 4
        elif order_model == ORDER_MODEL.LIMIT:
            order_model = 0

        if market is None:
            market = QAFetch.base.get_stock_market(code)
        if not isinstance(market, str):
            raise Exception('%s不正确，请检查code和market参数' % market)
        market = market.lower()
        if market not in ['sh', 'sz']:
            raise Exception('%s不支持，请检查code和market参数' % market)

        return self.call("send_order", {
            'client_id': self.client_id,
            'category': towards,
            'price_type': order_model,
            'gddm': self.gddm_sh if market == 'sh' else self.gddm_sz,
            'zqdm': code,
            'price': price,
            'quantity': amount
        })

    def cancel_order(self, exchange_id, order_id):
        """

        Arguments:
            exchange_id {[type]} -- 交易所  0 深圳 1上海 (偶尔2是深圳)
            order_id {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        return self.call("cancel_order", {
            'client_id': self.client_id,
            'exchange_id': exchange_id,
            'hth': order_id
        })

    def get_quote(self, code):
        return self.call("get_quote", {
            'client_id': self.client_id,
            'code': code,
        })

    def repay(self,  amount):
        return self.call("repay", {
            'client_id': self.client_id,
            'amount': amount
        })

    def receive_order(self, event):
        res = self.send_order(code=event.order.code, price=event.order.price, amount=event.order.amount, towards=event.order.towards, order_model=event.order.order_model)
        try:
            event.order.queued(realorder_id=res.realorder_id[0])
            print('success receive order {}'.format(event.order.realorder_id))
        except:
            event.order.failed()

            print(
                'FAILED FOR CREATE ORDER {} {}'.format(
                    event.order.account_cookie,
                    event.order.status
                )
            )
        return event.order

    def run(self, event):
        #if event.event_type is MARKET_EVENT.QUERY_DATA:
        #    self.order_handler.run(event)
        #    try:
        #        data = self.fetcher[(event.market_type, event.frequence)](
        #            code=event.code, start=event.start, end=event.end).values[0]
        #        if 'vol' in data.keys() and 'volume' not in data.keys():
        #            data['volume'] = data['vol']
        #        elif 'vol' not in data.keys() and 'volume' in data.keys():
        #            data['vol'] = data['volume']
        #        return data
        #    except Exception as e:
        #        QA_util_log_info('MARKET_ENGING ERROR: {}'.format(e))
        #        return None
        #elif event.event_type is BROKER_EVENT.RECEIVE_ORDER:
        #    self.order_handler.run(event)
        #elif event.event_type is BROKER_EVENT.TRADE:
        #    event = self.order_handler.run(event)
        #    event.message = 'trade'
        #    if event.callback:
        #        event.callback(event)
        #el
        if event.event_type is MARKET_EVENT.QUERY_ORDER:
            self.order_handler.run(event)
        elif event.event_type is BROKER_EVENT.SETTLE:
            self.order_handler.run(event)
            if event.callback:
                event.callback('settle')

    def get_market(self, order):
        try:
            data = self.fetcher[(order.market_type, order.frequence)](
                code=order.code, start=order.datetime, end=order.datetime).values[0]
            if 'vol' in data.keys() and 'volume' not in data.keys():
                data['volume'] = data['vol']
            elif 'vol' not in data.keys() and 'volume' in data.keys():
                data['vol'] = data['volume']
            return data
        except Exception as e:
            QA_util_log_info('MARKET_ENGING ERROR: {}'.format(e))
            return None

    def query_orders(self, account_cookie, status='filled'):
        df = self.data_to_df(self.query_data(3 if status is 'filled' else 2))
        df['account_cookie'] = account_cookie
        if status is 'filled':
            df = df[self.dealstatus_headers] if len(df) > 0 else pd.DataFrame(columns=self.dealstatus_headers)
        else:
            df['cancel_amount'] = 0
            df = df[self.orderstatus_headers] if len(df) > 0 else pd.DataFrame(columns=self.orderstatus_headers)
        return df.set_index(['account_cookie',  'realorder_id']).sort_index()

    def query_positions(self, account_cookie):
        data = {
            'cash_available': 0.00,
            'hold_available': {},
        }
        try:
            result = self.query_data(0)
            if 'data' in result and len(result['data']) > 0:
                # 使用减法避免因为账户日内现金理财导致可用金额错误
                data['cash_available'] = round(
                    float(result['data'][0]['总资产']) - float(result['data'][0]['最新市值']) - float(
                        result['data'][0]['冻结资金']), 2)

            result = self.data_to_df(self.query_data(1))
            if len(result) > 0:
                result.index = result.code
                if hasattr(result, 'amount'):
                    data['hold_available'] = result.amount
            return data
        except:
            print(e)
            return data


if __name__ == "__main__":
    import os
    import QUANTAXIS as QA
    print('在运行前 请先运行tdxtradeserver的 exe文件, 目录是你直接get_tts指定的 一般是 C:\tdxTradeServer')
    print('这是测试代码, 下面需要输入的 key/iv在ini中自己查找, account 和password是自己的账户密码 ')
    api = QA_TTSBroker(endpoint="http://127.0.0.1:19820/api",
                       enc_key=bytes(input('env_key:   '), encoding='utf-8'), enc_iv=bytes(input('env_iv:    '), encoding='utf-8'))

    print("---Ping---")
    result = api.ping()
    print(result)

    print("---登入---")
    acc = input('account:    ')
    password = input('password:   ')
    result = api.logon("60.191.116.36", 7708,
                       "6.44", 1,
                       acc, acc, password, "")

    if result["success"]:
        for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15):
            print("---查询信息 cate=%d--" % i)
            print(api.data_to_df(api.query_data(i)))


        print('==============================下面是下单部分========================')
        print('即将演示的是  下单000001  数量100股  价格9.8 的限价单模式')
        
        if str(input('我已知晓, 并下单 按y继续 n 退出'))[0] == 'y':
        
            print(api.send_order(code='000001', price=9.8, amount=100,
                                towards=QA.ORDER_DIRECTION.BUY, order_model=QA.ORDER_DIRECTION.BUY))
        print("---登出---")
        print(api.logoff())
