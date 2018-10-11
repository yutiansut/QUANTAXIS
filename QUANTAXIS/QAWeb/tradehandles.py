#coding :utf-8
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

import datetime
import json

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler
from QUANTAXIS.QAARP import QA_Account, QA_Portfolio, QA_User
from QUANTAXIS.QAWeb.basehandles import QABaseHandler, QAWebSocketHandler
"""
GET http://localhost:8888/accounts
GET http://localhost:8888/positions
GET http://localhost:8888/orders
POST http://localhost:8888/orders
DELETE http://localhost:8888/orders/O1234
GET http://localhost:8888/clients
"""


class AccModelHandler(QAWebSocketHandler):
    port=QA_Portfolio()

    def open(self):
        self.client.add(self)
        self.write_message('realtime socket start')

    def on_message(self, message):
        #assert isinstance(message,str)

        try:
            if message =='create_account':

                account=self.port.new_account()
                #account = self.port.add_account()
                self.write_message('CREATE ACCOUNT: {}'.format(account.account_cookie))

        except Exception as e:
            print(e)

    def on_close(self):
        print('connection close')
