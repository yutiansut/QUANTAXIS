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
import time

import pymongo
import tornado
from tornado import gen
from tornado.concurrent import Future
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_stock_day, QA_fetch_stock_min,
                                       QA_fetch_stock_to_market_date)
from QUANTAXIS.QAFetch.QAQuery_Advance import (QA_fetch_stock_day_adv,
                                               QA_fetch_stock_min_adv)
from QUANTAXIS.QAUtil.QADict import QA_util_dict_remove_key
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas
from QUANTAXIS.QAWeb.basehandles import QABaseHandler
from QUANTAXIS.QAWeb.fetch_block import get_block, get_name


class StockdayHandler(QABaseHandler):
    # @gen.coroutine
    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 end-->today

        """
        code = self.get_argument('code', default='000001')
        start = self.get_argument('start', default='2017-01-01')
        end = self.get_argument('end', default=str(datetime.date.today()))
        if_fq = self.get_argument('if_fq', default=False)
        return self.get_data(code, start, end, if_fq)

    def get_data(self, code, start, end, if_fq):

        if if_fq:
            data = QA_util_to_json_from_pandas(
                QA_fetch_stock_day_adv(code, start, end).to_qfq().data)

            self.write({'result': data})
        else:
            data = QA_util_to_json_from_pandas(
                QA_fetch_stock_day(code, start, end, format='pd'))

            self.write({'result': data})


class StockminHandler(QABaseHandler):
    """stock_min

    Arguments:
        QABaseHandler {[type]} -- [description]
    """

    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 09:00:00 end-->now

        """
        code = self.get_argument('code', default='000001')
        start = self.get_argument('start', default='2017-01-01 09:00:00')
        end = self.get_argument('end', default=str(datetime.datetime.now()))
        frequence = self.get_argument('frequence', default='1min')
        if_fq = self.get_argument('if_fq', default=False)

        if if_fq:
            data = QA_util_to_json_from_pandas(
                QA_fetch_stock_min_adv(code, start, end, frequence).to_qfq().data)

            self.write({'result': data})
        else:
            data = QA_util_to_json_from_pandas(
                QA_fetch_stock_min(code, start, end, format='pd', frequence=frequence))

            self.write({'result': data})

        self.write({'result': data})


class StockBlockHandler(QABaseHandler):
    """return BLOCK

    Arguments:
        QABaseHandler {[type]} -- [description]
    """

    def get(self):
        block_name = self.get_argument('block', default=[])
        monitor_list = get_name(get_block(block_name))
        self.write({'result': monitor_list})


class StockPriceHandler(QABaseHandler):
    """return REALTIME handler

    Arguments:
        QABaseHandler {[type]} -- [description]
    """

    def get(self):
        try:
            code = self.get_argument('code', default='000001')[0:6]
            database = DATABASE.get_collection(
                'realtime_{}'.format(datetime.date.today()))

            current = [QA_util_dict_remove_key(item, '_id') for item in database.find({'code': code}, limit=1, sort=[
                ('datetime', pymongo.DESCENDING)])]

            self.write(current[0])
        except:
            self.write('wrong')


class StockCodeHandler(QABaseHandler):
    """return STOCK LIST/NAME

    Arguments:
        QABaseHandler {[type]} -- [description]
    """

    def get(self):
        try:
            code = self.get_argument('code', default='000001')[0:6]
            res = DATABASE.stock_list.find_one({'code': code})

            if res is None:
                self.write('wrong')

            else:
                self.write(res['name'].encode('gbk'))
        except:
            self.write('wrong')


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
