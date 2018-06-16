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
import tornado
from tornado.web import Application, RequestHandler, authenticated

from QUANTAXIS.QAWeb.datahandles import StockdayHandler, StockminHandler,StockBlockHandler
from QUANTAXIS.QAWeb.quotationhandles import (RealtimeSocketHandler,
                               SimulateSocketHandler,MonitorSocketHandler)
from QUANTAXIS.QAWeb.userhandles import SigninHandler, SignupHandler, PersonBlockHandler
from QUANTAXIS.QAWeb.basehandles import QABaseHandler
from QUANTAXIS.QAWeb.arphandles import AccountHandler

class INDEX(QABaseHandler):
    def get(self):
        self.render(".\index.html")


def main():
    apps = Application(
        handlers=[
            (r"/", INDEX),
            (r"/marketdata/stock/day", StockdayHandler),
            (r"/marketdata/stock/min", StockminHandler),
            (r"/marketdata/stock/block", StockBlockHandler),
            (r"/user/signin", SigninHandler),
            (r"/user/signup", SignupHandler),
            (r"/user/blocksetting", PersonBlockHandler),
            (r"/realtime", RealtimeSocketHandler),
            (r"/simulate", SimulateSocketHandler),
            (r"/monitor", MonitorSocketHandler),
            (r"/accounts",AccountHandler)
        ],
        debug=True
    )
    apps.listen(8010)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    app = Application(
        handlers=[
            (r"/", INDEX),
            (r"/marketdata/stock/day", StockdayHandler),
            (r"/marketdata/stock/min", StockminHandler),
            (r"/marketdata/stock/block", StockBlockHandler),
            (r"/user/signin", SigninHandler),
            (r"/user/signup", SignupHandler),
            (r"/user/blocksetting", PersonBlockHandler),
            (r"/realtime", RealtimeSocketHandler),
            (r"/simulate", SimulateSocketHandler),
            (r"/monitor", MonitorSocketHandler),
            (r"/accounts",AccountHandler)
        ],
        debug=True
    )
    app.listen(8010)
    tornado.ioloop.IOLoop.instance().start()
