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

import datetime
import os
import time

import pandas as pd
import pymongo
import tornado
from tornado.web import Application, RequestHandler, authenticated

import QUANTAXIS as QA
from QUANTAXIS.QAWeb.basehandles import QABaseHandler,QAWebSocketHandler
from tornado.websocket import WebSocketClosedError
from tornado.iostream import StreamClosedError

"""
要实现2个api

1. SIMULATED WEBSOCKET

2. REALTIME WEBSOCKET

"""
client = set() 

class INDEX(QABaseHandler):
    def get(self):
        self.render("./index.html")


class RealtimeSocketHandler(QAWebSocketHandler):
    client = set() 
    def open(self):
        self.client.add(self)
        self.write_message('realtime socket start')

    
    def on_message(self, message):
        #assert isinstance(message,str)

        try:
            
            database = QA.DATABASE.get_collection(
                'realtime_{}'.format(datetime.date.today()))
            current = [QA.QA_util_dict_remove_key(item, '_id') for item in database.find({'code': message}, limit=1, sort=[
                ('datetime', pymongo.DESCENDING)])]
            
            self.write_message(current[0])

        except Exception as e:
            print(e)

    def on_close(self):
        print('connection close')


class SimulateSocketHandler(QAWebSocketHandler):
    def open(self):
        self.write_message('start')

    def on_message(self, message):
        if len(str(message)) == 6:
            data = QA.QA_util_to_json_from_pandas(
                QA.QA_fetch_stock_day(message, '2017-01-01', '2017-02-05', 'pd'))
            for item in data:
                self.write_message(item)
                time.sleep(0.1)

    def on_close(self):
        print('connection close')


class MonitorSocketHandler(QAWebSocketHandler):
    def open(self):
        self.write_message('start')

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print('connection close')


if __name__ == '__main__':
    app = Application(
        handlers=[
            (r"/", INDEX),
            (r"/realtime", RealtimeSocketHandler),
            (r"/simulate", SimulateSocketHandler)
        ],
        debug=True
    )
    app.listen(8010)
    tornado.ioloop.IOLoop.instance().start()
