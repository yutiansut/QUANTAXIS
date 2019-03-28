# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
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

from QUANTAXIS.QAEngine.QAThreadEngine import QA_Engine

# 交易封装


class QA_Trade():
    "多线程+generator模式"

    def __init__(self, *args, **kwargs):
        self.trade_engine = QA_Engine()
        self.event_queue = self.trade_engine.queue
        
        # self.spi_thread.start()

    def connect(self, *args, **kwargs):

        pass

    def on_connect(self, *args, **kwargs):
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

    def get_account_cookie(self, *args, **kwargs):
        pass

    def subscribe_public_topic(self, *args, **kwargs):
        pass

    def login(self, *args, **kwargs):
        pass

    def logout(self, *args, **kwargs):
        pass

    def insert_order(self, *args, **kwargs):
        pass

    def on_insert_order(self, *args, **kwargs):
        pass

    def cancel_order(self, *args, **kwargs):
        pass

    def on_cancel_order(self, *args, **kwargs):
        pass

    def query_order(self, *args, **kwargs):
        pass

    def on_query_order(self, *args, **kwargs):
        pass

    def query_trade(self, *args, **kwargs):
        pass

    def on_query_trade(self, *args, **kwargs):
        pass

    def query_position(self, *args, **kwargs):
        pass

    def on_query_position(self, *args, **kwargs):
        pass

    def query_assets(self, *args, **kwargs):
        pass

    def on_query_assets(self, *args, **kwargs):
        pass

    def query_data(self, *args, **kwargs):
        pass

    def on_query_data(self, *args, **kwargs):
        pass

    def on_error(self, *args, **kwargs):
        pass

    def on_order_event(self, *args, **kwargs):
        pass

    def on_trade_event(self, *args, **kwargs):
        pass

    def on_cancel_order_event(self, *args, **kwargs):
        pass
