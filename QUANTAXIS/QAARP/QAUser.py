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

from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QASetting import QA_Setting
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QASU.user import QA_user_sign_in
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio

class QA_User():
    def __init__(self, *args, **kwargs):
        self.setting=QA_Setting()

        self.portfolio_list = {}
        self.user_cookie = QA_util_random_with_topic('USER')

    def client(self):
        return self.setting.client

    def connect_database(self,ip='127.0.0.1',port=27017):
        self.setting.change(ip,port)

    def login(self,user_name,password):
        if self.setting.login(user_name,password):
            QA_util_log_info('SUCCESS')
        else:
            QA_util_log_info('FAILD')
            

    def new_portfolio(self):
        _portfolio=QA_Portfolio()
        if _portfolio.portfolio_cookie not in self.portfolio_list.keys():
            self.portfolio_list[_portfolio.portfolio_cookie]=_portfolio
            
        
    def get_portfolio(self, portfolio):
        return self.portfolio_list[portfolio]
