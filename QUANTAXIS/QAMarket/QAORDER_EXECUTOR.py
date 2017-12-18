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
import pandas as pd
import numpy as np
import datetime
import queue
from QUANTAXIS.QAMarket.QAOrder import QA_Order, QA_Order_list
from QUANTAXIS.QAMarket.QAMarket import QA_Market
from QUANTAXIS.QAUtil.QAParameter import RUNNING_ENVIRONMENT


class ORDER_EXECUTOR():
    """ORDER执行器

    仅负责一个无状态的执行层

    用于接受订单 发送给相应的marker_broker

    可用的market_broker:
    1.回测盘
    2.实时模拟盘
    3.实盘

    """

    def __init__(self, order_queue=queue.Queue(), market, environment=RUNNING_ENVIRONMENT.BACKETEST, *args, **kwargs):
        self.order_queue() = order
        self.market = market
        self.environment_engine = {'backtest':QA_Market,'simulation':}
        self.environment = environment

    def switch_environment(self, environment):
        self.environment = environment
