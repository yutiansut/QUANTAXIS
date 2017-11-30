# coding:utf-8
from QUANTAXIS_Trade.util import base_trade
import requests
import urllib
import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class TdxTradeApiParams:
    
    """
    参见 https://github.com/yutiansut/pytdx/blob/master/pytdx/trade/trade.py
    0 资金
    1 股份
    2 当日委托
    3 当日成交
    4 可撤单
    5 股东代码
    6 融资余额
    7 融券余额
    8 可融证券
    9
    10
    11
    12 可申购新股查询
    13 新股申购额度查询
    14 配号查询
    15 中签查询
    """
    QUERY_CATEGORY_CASH     = 0
    QUERY_CATEGORY_STOCKS   = 1
    QUERY_CATEGORY_ORDER_OF_TODAY       = 2
    QUERY_CATEGORY_DEAL_OF_TODAY        = 3
    QUERY_CATEGORY_CANCELABLE_ORDER     = 4
    QUERY_CATEGORY_SHAREHOLDERS_CODE    = 5
    QUERY_CATEGORY_BALANCE_OF_MARGIN_LOAN   = 6
    QUERY_CATEGORY_BALANCE_OF_STOCK_LOAN    = 7
    QUERY_CATEGORY_OPERABLE_MARGIN_SOTCK    = 8

    QUERY_CATEGORY_NEW_STOCKS       = 12
    QUERY_CATEGORY_NEW_STOCKS_QUOTA = 13
    QUERY_CATEGORY_NEW_STOCK_NUMBER = 14
    QUERY_CATEGORY_NEW_STOCK_HIT    = 15


class QATrade_TdxTradeServer(base_trade.QA_Trade_Api):
    def __init__(self, endpoint="http://127.0.0.1:10920/api", encoding="utf-8", enc_key=None, enc_iv=None):
        super.__init__()
        
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
            self._cipher = Cipher(algorithms.AES(enc_key), modes.CBC(enc_iv), backend=backend)

        self._session = requests.Session()


    def spi_job(self, func, params=None):
        while self._queue.empty is False:
            job=self._queue.get()
            
             

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
            log.debug(decoded_text)
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
            return pd.DataFrame(data=data)
    def ping(self):
    
        return self.call("ping", {})


    def login(self, ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password):
        return self.call("logon",{
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