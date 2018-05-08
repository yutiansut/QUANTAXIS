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
import pandas as pd
from QUANTAXIS.QAARP.QAPortfolio import QA_Portfolio
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
from QUANTAXIS.QAUtil.QARandom import QA_util_random_with_topic
from QUANTAXIS.QAUtil.QASetting import QA_Setting


class QA_User():
    """QA_User 
    User--Portfolio--Account/Strategy

    :: 需要增加对于QA_USER的支持

    USER作为一个单位实体,可以自由创建组合(需要被记录),修改组合
    


    @yutiansut 
    2018/05/08
    """

    def __init__(self):
        self.setting = QA_Setting()
        self.portfolio_list = {}
        self.user_cookie = QA_util_random_with_topic('USER')

    def __repr__(self):
        return '< QA_USER {} with {} portfolio >'.format(self.user_cookie, len(self.portfolio_list.keys()))

    @property
    def table(self):
        return pd.concat([po.table for po in self.portfolio_list.values()], axis=1)

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
        _portfolio = QA_Portfolio(user_cookie=self.user_cookie)
        if _portfolio.portfolio_cookie not in self.portfolio_list.keys():
            self.portfolio_list[_portfolio.portfolio_cookie] = _portfolio
            return _portfolio

    def get_portfolio(self, portfolio):
        'get a portfolio'
        return self.portfolio_list[portfolio]

    def generate_simpleaccount(self):
        """make a simple account with a easier way
        如果当前user中没有创建portfolio, 则创建一个portfolio,并用此portfolio创建一个account
        如果已有一个或多个portfolio,则使用第一个portfolio来创建一个account
        """
        if len(self.portfolio_list.keys()) < 1:
            po = self.new_portfolio()
        else:
            po = list(self.portfolio_list.values())[0]
        ac = po.new_account()
        return ac, po

    def register_account(self, account):
        if len(self.portfolio_list.keys()) < 1:
            po = self.new_portfolio()
        else:
            po = list(self.portfolio_list.values())[0]
        po.add_account(account)
        return (po, account)


    def save(self):
        """
        将QA_USER的信息存入数据库
        """
        pass


if __name__ == '__main__':
    user = QA_User()
    portfolio1 = user.new_portfolio()
    ac1 = user.get_portfolio(portfolio1).new_account()

    print(user)
    print(user.get_portfolio(portfolio1))
    print(user.get_portfolio(portfolio1).get_account(ac1))
