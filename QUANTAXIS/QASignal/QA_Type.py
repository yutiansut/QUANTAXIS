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

import datetime
import json
import threading
import time

import numpy as np
import pandas as pd

from six.moves import queue
from QUANTAXIS.QAUtil import QA_util_log_info


class QA_Type_standard():
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

class error_code():
    market_err={
        '203':'limited',
        '400':'fail',
        '500':'no market data'
    }