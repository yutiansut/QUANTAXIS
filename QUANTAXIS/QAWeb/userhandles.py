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

from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting
from QUANTAXIS.QAWeb.basehandles import QABaseHandler


class SignupHandler(QABaseHandler):
    def get(self):
        """注册接口
        
        Arguments:
            QABaseHandler {[type]} -- [description]

            user/signin?user=xxx&password=xx
        Return 
            'SUCCESS' if success
            'WRONG' if wrong
        """

        username = self.get_argument('user', default='admin')
        password = self.get_argument('password', default='admin')
        if QA_user_sign_up(username, password, client=QA_util_sql_mongo_setting()):
            self.write('SUCCESS')
        else:
            self.write('WRONG')


class SigninHandler(QABaseHandler):
    def get(self):
        """登陆接口
        
        Arguments:
            QABaseHandler {[type]} -- [description]

            user/signup?user=xxx&password=xx
        Return 
            'SUCCESS' if success
            'WRONG' if wrong
        """

        username = self.get_argument('user', default='admin')
        password = self.get_argument('password', default='admin')
        res = QA_user_sign_in(username, password,
                              client=QA_util_sql_mongo_setting())
        if res is not None:
            self.write('SUCCESS')
        else:
            self.write('WRONG')


class PersonBlockHandler(QABaseHandler):
    def get(self):
        """
        make table for user: user

        send in ==> {'block',[{'block':xxxx,'code':code}}
        """
        table = DATABASE.user_block
        data = table.find_one()
        print(data)
        data.pop('_id')
        self.write(data)
        # table.find_one_and_update('')

    def post(self):
        """
        make table for user: user

        send in ==> {'block',[{'block':xxxx,'code':code}}
        """
        param = eval(self.get_argument('block'))
        print(param)
        table = DATABASE.user_block
        table.insert({'block': param})
        # table.find_one_and_update('')


if __name__ == '__main__':
    app = Application(
        handlers=[

            (r"/user/signin", SigninHandler),
            (r"/user/signup", SignupHandler)
        ],
        debug=True
    )
    app.listen(8010)
    tornado.ioloop.IOLoop.instance().start()
