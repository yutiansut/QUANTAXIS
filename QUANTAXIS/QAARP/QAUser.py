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

from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QASetting import QA_Setting


class QA_User():
    """QA_User 
    User--Portfolio--Account/Strategy
    """
    def __init__(self):
        self.setting = QA_Setting()
        self.portfolio_list = {}
        self.user_cookie = QA_util_random_with_topic('USER')

    def __repr__(self):
        return '< QA_USER {} with {} portfolio >'.format(self.user_cookie, len(self.portfolio_list.keys()))

    def client(self):
        'user.client to connect database'
        return self.setting.client

    def connect_database(self, ip='127.0.0.1', port=27017):
        'connect is also a way to change database from IP_A to IP_B'
        self.setting.change(ip, port)

    def login(self, user_name, password):
        'login to a database'
        if self.setting.login(user_name, password):
            QA_util_log_info('SUCCESS')
        else:
            QA_util_log_info('FAILD')

    def new_portfolio(self):
        'create a portfolio'
        _portfolio = QA_Portfolio()
        if _portfolio.portfolio_cookie not in self.portfolio_list.keys():
            self.portfolio_list[_portfolio.portfolio_cookie] = _portfolio
            return _portfolio.portfolio_cookie

    def get_portfolio(self, portfolio):
        'get a portfolio'
        return self.portfolio_list[portfolio]

    def generate_simpleaccount(self):
        'make a simple account with a easier way'
        if len(self.portfolio_list.keys()) < 1:
            po = self.new_portfolio()
            ac = self.get_portfolio(po).new_account()
            return ac, po


if __name__ == '__main__':
    user = QA_User()
    portfolio1 = user.new_portfolio()
    ac1 = user.get_portfolio(portfolio1).new_account()

    print(user)
    print(user.get_portfolio(portfolio1))
    print(user.get_portfolio(portfolio1).get_account(ac1))
