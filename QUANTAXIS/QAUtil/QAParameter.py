# -* coding: utf-8 -*-
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


"""
这里定义的是一些常用常量
"""


class Order_DIRECTION:
    @property
    def BUY(self):
        return 1

    @property
    def SELL(self):
        return -1

    @property
    def BUY_OPEN(self):
        return 2

    @property
    def BUY_CLOSE(self):
        return 3

    @property
    def SELL_OPEN(self):
        return -2

    @property
    def SELL_CLOSE(self):
        return -3


class MARKET_TYPE():
    @property
    def stock_day(self):
        return '0x01'

    @property
    def stock_min(self):
        return '0x02'

    @property
    def index_day(self):
        return '0x03'

    @property
    def index_min(self):
        return '0x04'

    @property
    def stock_transaction(self):

        return '0x05'

    @property
    def index_transaction(self):
        return '0x07'

    @property
    def future_day(self):
        return '1x01'