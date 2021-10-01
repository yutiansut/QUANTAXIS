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
import asyncio
import os
import sys

import tornado
from QUANTAXIS import __version__
from QUANTAXIS.QAUtil.QASetting import QASETTING
from QUANTAXIS.QAWebServer.basehandles import QABaseHandler
from QUANTAXIS.QAWebServer.commandhandler import (CommandHandler,
                                                  CommandHandlerWS,
                                                  RunnerHandler)
from QUANTAXIS.QAWebServer.schedulehandler import (QAScheduleQuery,
                                                   QASchedulerHandler,
                                                   init_scheduler)
from QUANTAXIS.QAWebServer.qifiserver import QAQIFI_Handler, QAQIFIS_Handler
from tornado.options import (define, options, parse_command_line,
                             parse_config_file)
from tornado.web import Application, RequestHandler, authenticated


class INDEX(QABaseHandler):

    def get(self):
        self.write(
            {
                'status': 200,
                'message': 'This is a welcome page for quantaxis backend',
                'url': [item[0] for item in handlers]
            }
        )


#term_manager = SingleTermManager(shell_command=['bash'])
handlers = [
    (r"/",
     INDEX),

    (r"/command/run",
     CommandHandler),
    (r"/command/runws",
     CommandHandlerWS),
    (r"/command/runbacktest",
     RunnerHandler),
    (r"/scheduler/map/?", QASchedulerHandler),
    (r"/scheduler/query", QAScheduleQuery),
    (r"/qifi", QAQIFI_Handler),
    (r"/qifis", QAQIFIS_Handler)

]


def main():
    asyncio.set_event_loop(asyncio.new_event_loop())
    define("port", default=8010, type=int, help="服务器监听端口号")

    define("address", default='0.0.0.0', type=str, help='服务器地址')
    define("content", default=[], type=str, multiple=True, help="控制台输出内容")

    parse_command_line()
    port = options.port
    address = options.address
    scheduler = init_scheduler()

    start_server(handlers, address, port)


def start_server(handlers, address='0.0.0.0', port=8010):
    apps = Application(
        handlers=handlers,
        debug=True,
        autoreload=True,
        compress_response=True
    )
    
    print('========WELCOME QUANTAXIS_WEBSERVER 2.0 ============')
    print('QUANTAXIS VERSION: {}'.format(__version__))
    print('QUANTAXIS WEBSERVER is Listening on: http://{}:{}'.format(address, port))
    print('请打开浏览器/使用JavaScript等来使用该后台, 并且不要关闭当前命令行窗口')
    apps.listen(port, address=address)

    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
