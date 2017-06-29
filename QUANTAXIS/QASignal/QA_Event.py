# coding:utf-8
import datetime
import json
import threading
import time

import numpy as np
import pandas as pd

from six.moves import queue
from QUANTAXIS.QAUtil import QA_util_log_info


class event_type():
    QA_Bid = '1x00'
    QA_Market = '2x00'
    QA_Fetch = '3x00'
    QA_Account = '4x00'
    QA_Risk = '5x00'
    QA_Portfolio = '6x00'
    QA_Trade = '7x00'
    QA_Strategy = '8x00'
    QA_Other = '9x00'
    QUANTAXIS = '0x00'

    def __dispatch(self, __type):
        if __type == self.QA_Bid:
            return 'QA.QA_Bid_event'
        elif __type == self.QA_Market:
            return 'QA.QAMarket'
        elif __type == self.QA_Fetch:
            return 'QA.QAFetch'
        elif __type == self.QA_Account:
            return 'QA.QAARP.QAAccout'
        elif __type == self.QA_Risk:
            return 'QA.QAARP.QARisk'
        elif __type == self.QA_Portfolio:
            return 'QA.QAARP.QAPortfolio'
        elif __type == self.QA_Trade:
            return 'QA.QA_Trade'
        elif __type == self.QA_Strategy:
            return 'QA.QA_Strategy'
        elif __type == self.QA_Other:
            return ''
        elif __type == self.QUANTAXIS:
            return 'QUANTAXIS'


class QA_Bid_event():
    stock_day = '1x01'
    stock_min = '1x02'
    stock_tick = '1x03'
    future_day = '1x04'
    future_min = '1x05'
    future_tick = '1x06'
    stock_future = '1x10'

    def __tran_(self, sub_type):
        if sub_type == self.stock_day:
            return 'stock_day'
        elif sub_type == self.stock_min:
            return 'stock_min'
        elif sub_type == self.stock_tick:
            return 'stock_tick'
        elif sub_type == self.future_day:
            return 'future_day'
        elif sub_type == self.future_min:
            return 'future_min'
        elif sub_type == self.future_tick:
            return 'future_tick'
        elif sub_type == self.stock_future:
            return 'stock_future'

    def check_(self, __event):
        pass


class QA_Market_event():
    market_engine = '2x01'

    market_exec = '2x11'

    market_status = '2x21'

    market_engine_type = {}

    def __tran_(self, __event):
        if __event.sub_type == self.market_engine:
            return 'market_engine'
        elif __event.sub_type == self.market_exec:
            return 'market_exec'
        elif __event.sub_type == self.market_status:
            return 'market_exec'

    def check_(self, __event):
        pass


class event_proto:
    """
    a least-feature-event_msg should only have type message and args, where we can give the function to them
    """

    def __init__(self,
                 __type_: str,
                 __sub_type: str,
                 __args: list,
                 __fn: str):
        
        pass

    def repackage(self, event):
        pass


class event_engine():
    def __init__(self):
        self.__queue = queue.Queue()
        self.thread = threading.Thread()
        self.timer = threading.Timer

    def __insert(self, __event):

        self.__queue.put_nowait(__event)

    def __exec(self):
        while self.__queue.empty():
            __exec_event = self.__queue.get_nowait()
            eval(__exec_event['fn'])(__exec_event['args'])
