# coding :utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64
import configparser
import json
import os
import urllib
import future
import asyncio
import pandas as pd
import requests
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from QUANTAXIS.QAEngine.QAEvent import QA_Event
from QUANTAXIS.QAMarket.common import cn_en_compare, trade_towards_cn_en, order_status_cn_en
from QUANTAXIS.QAMarket.QABroker import QA_Broker
from QUANTAXIS.QAMarket.QAOrderHandler import QA_OrderHandler
from QUANTAXIS.QAUtil.QAParameter import (
    BROKER_EVENT,
    ORDER_DIRECTION,
    BROKER_TYPE,
    ORDER_MODEL,
    ORDER_STATUS
)
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_order_datetime
from QUANTAXIS.QAUtil.QADate import QA_util_date_int2str
from QUANTAXIS.QAUtil.QASetting import setting_path

CONFIGFILE_PATH = '{}{}{}'.format(setting_path, os.sep, 'config.ini')


class QA_ATBroker(QA_Broker):

    def __init__(self):
        pass

    def get_market(self, order):
        pass

    def query_orders(self, account_cookie, order_id):
        raise NotImplementedError

    def query_deal(self, account_cookie, order_id):
        raise NotImplementedError

    def query_positions(self, account_cookie):
        raise NotImplementedError
