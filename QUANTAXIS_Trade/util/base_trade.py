# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2017 yutiansut/QUANTAXIS
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
import asyncio
import concurrent
import datetime
import logging
import queue
import threading
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Process
from threading import Event, Thread, Timer

import numpy as np
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient

from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API

from QUANTAXIS.QAUtil.QADate_trade import QA_util_if_tradetime
from QUANTAXIS.QAUtil.QASetting import QA_Setting, info_ip_list
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
from QUANTAXIS.QAMarket.QABid import QA_QAMarket_bid


class QA_Trade:
    def __init__(self, *args, **kwargs):
        pass

class Order(QA_QAMarket_bid):
    def __init__(self, *args, **kwargs):
        pass


class QA_Trade_Api():
    
    def __init__(self, *args, **kwargs):
        self.spi_thread=Thread(target=None,name='QATradeSpi',daemon=True)
        self._queue=queue.Queue()

    def spi_job(self, *args, **kwargs):
        # 任务应当在这里做
        pass


    def connect(self, *args, **kwargs):
        pass

    def release(self, *args, **kwargs):
        pass

    def get_trading_day(self, *args, **kwargs):
        pass

    def register_spi(self, *args, **kwargs):
        pass

    def get_api_last_error(self, *args, **kwargs):
        pass

    def get_api_version(self, *args, **kwargs):
        pass

    def get_client_id(self, *args, **kwargs):
        pass

    def get_account_id(self, *args, **kwargs):
        pass

    def subscribe_public_topic(self, *args, **kwargs):
        pass

    def login(self, *args, **kwargs):
        pass

    def logout(self, *args, **kwargs):
        pass

    def insert_order(self, *args, **kwargs):
        pass

    def cancel_order(self, *args, **kwargs):
        pass

    def query_order(self, *args, **kwargs):
        pass

    def query_trade(self, *args, **kwargs):
        pass

    def query_position(self, *args, **kwargs):
        pass

    def query_asset(self, *args, **kwargs):
        pass
    
    

class QA_Trade_Spi():
    def __init__(self, *args, **kwargs):
        pass

    def on_disconnected(self, *args, **kwargs):
        pass

    def on_error(self, *args, **kwargs):
        pass

    def on_order_event(self, *args, **kwargs):
        pass

    def on_trade_event(self, *args, **kwargs):
        pass

    def on_cancel_order_event(self, *args, **kwargs):
        pass

    def on_query_order(self, *args, **kwargs):
        pass

    def on_query_trade(self, *args, **kwargs):
        pass

    def on_query_position(self, *args, **kwargs):
        pass

    def on_query_asset(self, *args, **kwargs):
        pass