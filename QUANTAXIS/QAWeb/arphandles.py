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

import json
import tornado
import datetime
from tornado.web import Application, RequestHandler, authenticated
from tornado.websocket import WebSocketHandler

from QUANTAXIS.QAFetch.QAQuery import QA_fetch_account, QA_fetch_risk
from QUANTAXIS.QASU.save_account import save_account
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QARisk import QA_Performance, QA_Risk
from QUANTAXIS.QASU.user import QA_user_sign_in, QA_user_sign_up
from QUANTAXIS.QAUtil.QASetting import DATABASE
from QUANTAXIS.QAUtil.QASql import QA_util_sql_mongo_setting
from QUANTAXIS.QAWeb.basehandles import QABaseHandler
from QUANTAXIS.QAWeb.util import CJsonEncoder


class MemberHandler(QABaseHandler):
    """
    获得所有的回测member
    """
    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 09:00:00 end-->now
        accounts?account_cookie=xxx
        """
        #account_cookie= self.get_argument('account_cookie', default='admin')

        query_account = QA_fetch_account()
        # data = [res for res in query_account]
        if len(query_account) > 0:
            #data = [QA.QA_Account().from_message(x) for x in query_account]
            warpper=lambda x: str(x) if isinstance(x,datetime.datetime) else x
            for item in query_account:
                item['trade_index']=list(map(str,item['trade_index']))
                item['history']=[list(map(warpper,itemd)) for itemd in item['history']]

            self.write({'result': query_account})
        else:
            self.write('WRONG')


class AccountHandler(QABaseHandler):
    """
    对于某个回测账户
    """
    def get(self):
        """
        采用了get_arguents来获取参数
        默认参数: code-->000001 start-->2017-01-01 09:00:00 end-->now
        accounts?account_cookie=xxx
        """
        account_cookie = self.get_argument('account_cookie', default='admin')

        query_account = QA_fetch_account({'account_cookie': account_cookie})
        #data = [QA_Account().from_message(x) for x in query_account]

        if len(query_account) > 0:
            #data = [QA.QA_Account().from_message(x) for x in query_account]
            warpper=lambda x: str(x) if isinstance(x,datetime.datetime) else x
            for item in query_account:
                item['trade_index']=list(map(str,item['trade_index']))
                item['history']=[list(map(warpper,itemd)) for itemd in item['history']]


            self.write({'result': query_account})
        else:
            self.write('WRONG')


class RiskHandler(QABaseHandler):
    """
    回测账户的风险评价
    """
    def get(self):
        account_cookie = self.get_argument('account_cookie', default='admin')

        query_account = QA_fetch_risk({'account_cookie': account_cookie})
        #data = [QA_Account().from_message(x) for x in query_account]
        if len(query_account) > 0:
            #data = [QA.QA_Account().from_message(x) for x in query_account]

            self.write({'result': query_account})
        else:
            self.write('WRONG')
