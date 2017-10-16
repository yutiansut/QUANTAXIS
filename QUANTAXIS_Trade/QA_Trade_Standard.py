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

class QA_Trade:
    def __init__(self, *args, **kwargs):
        pass



class QATrade_Query:
    """
    一个查询类
    """
    def __init__(self, *args, **kwargs):
        pass
    @property
    def code(self):
        pass

    @code.setter
    def code(self):
        pass
class QA_Trade_Spi():
    "和中泰XTP一致的回调函数"
    def __init__(self, *args, **kwargs):
        pass
    def on_disconnected(self):
        pass
    def on_error(self):
        pass
    def on_order_event(self):
        pass
    def on_trade_event(self):
        pass
    def on_cancel_order_event(self):
        pass
    def on_query_order(self):
        pass
    def on_query_trade(self):
        pass
    def on_query_position(self):
        pass
    def on_query_asset(self):
        pass


class QA_Trade_Api():
    def __init__(self, *args, **kwargs):
        pass
    def release(self):
        pass
    def get_trading_day(self):
        pass
    def register_spi(self):
        pass
    def get_api_last_error(self):
        pass
    def get_api_version(self):
        pass
    def get_client_id(self):
        pass
    def get_account_id(self):
        pass
    def subscribe_public_topic(self):
        pass
    def login(self):
        pass
    def logout(self):
        pass
    def insert_order(self):
        pass
    def cancel_order(self):
        pass
    def query_order(self):
        pass
    def query_trade(self):
        pass
    def query_position(self):
        pass
    def query_asset(self):
        pass