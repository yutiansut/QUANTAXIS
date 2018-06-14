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
import json

import tornado
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day, QA_fetch_stock_min
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_day_adv
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
from QUANTAXIS.QAWeb.fetch_block import get_block, get_name
from QUANTAXIS.QAWeb.basehandles import QABaseHandler


class StockdayHandler(QABaseHandler):
    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 end-->today

        """
        code = self.get_argument('code', default='000001')
        start = self.get_argument('start', default='2017-01-01')
        end = self.get_argument('end', default=str(datetime.date.today()))
        data = QA_util_to_json_from_pandas(
            QA_fetch_stock_day(code, start, end, format='pd'))

        self.write({'result': data})


class StockminHandler(QABaseHandler):
    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 09:00:00 end-->now

        """
        code = self.get_argument('code', default='000001')
        start = self.get_argument('start', default='2017-01-01 09:00:00')
        end = self.get_argument('end', default=str(datetime.datetime.now()))
        frequence = self.get_argument('frequence', default='1min')
        data = QA_util_to_json_from_pandas(
            QA_fetch_stock_min(code, start, end, format='pd', frequence=frequence))

        self.write({'result': data})


class StockBlockHandler(QABaseHandler):
    def get(self):
        block_name = self.get_argument('block', default=[])
        print(block_name)
        monitor_list = get_name(get_block(block_name))
        self.write({'result': monitor_list})


if __name__ == "__main__":

    app = Application(
        handlers=[
            (r"/stock/day", StockdayHandler),
            (r"/stock/min", StockminHandler)
        ],
        debug=True
    )
    app.listen(8010)
    tornado.ioloop.IOLoop.current().start()
