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
from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAUtil import (DATABASE, QA_util_log_info,
                              QA_util_random_with_topic)


class QA_Portfolio():

    """
    QUANTAXIS 多账户
    以及组合管理

    # 适用 回测/实盘


    在portfolio中,我们希望通过cookie来控制account_unit
    对于account的指标,要进行风险控制,组合成最优的投资组合的量

    用account的cookie来管理控制account

    portfolio里面的资产主要考虑的是 资金的分配
    """

    def __init__(self, user_cookie=None, strategy_name=None, init_assets=1000000, cash=None, sell_available=None, history=None):
        self.accounts = {}
        self.portfolio_cookie = QA_util_random_with_topic('Portfolio')
        self.user_cookie = user_cookie
        self.strategy_name = strategy_name
        # 和account一样的资产类
        self.init_assets = 1000000 if init_assets is None else init_assets
        self.cash = [self.init_assets] if cash is None else cash
        self.cash_available = self.cash[-1]  # 可用资金
        self.sell_available = sell_available
        self.history = [] if history is None else history
        self.time_index = []

        for cookie in self.accounts.keys():
            self.accounts[cookie] = QA_Account(account_cookie=cookie)

    def __repr__(self):
        return '< QA_Portfolio {} with {} Accounts >'.format(self.portfolio_cookie, len(self.accounts.keys()))

    @property
    def cash(self):
        pass

    @property
    def history(self):
        pass

    def get_portfolio(self):
        'return the accounts dict'
        return self.accounts

    def add_account(self, account):
        'portfolio add a account/stratetgy'
        if account.account_cookie not in self.accounts.keys():
            account.portfolio_cookie = self.portfolio_cookie
            account.user_cookie = self.user_cookie
            self.accounts[account.account_cookie] = account
        else:
            pass

    def new_account(self, account_cookie=None):
        'portfolio create a account/strategy'
        if account_cookie is None:
            temp = QA_Account(portfolio_cookie=self.portfolio_cookie,
                              user_cookie=self.user_cookie)
            if temp.account_cookie not in self.accounts.keys():
                self.accounts[temp.account_cookie] = temp
                return temp

            else:
                return self.new_account()
        else:
            if account_cookie not in self.accounts.keys():
                self.accounts[account_cookie] = QA_Account(portfolio_cookie=self.portfolio_cookie,
                                                           user_cookie=self.user_cookie, account_cookie=account_cookie)
                return self.accounts[account_cookie]
            else:
                return self.new_account(account_cookie)

    def get_account(self, cookie):
        'give the account_cookie and return the account/strategy back'
        try:
            return self.accounts[cookie]
        except:
            QA_util_log_info('Can not find this account')
            return None

    def cookie_mangement(self):
        pass

    @property
    def table(self):
        return pd.concat([acc.table for acc in self.accounts.values()], axis=1)

    def get_cash(self):
        """拿到整个portfolio的可用资金

        统计每一个时间点的时候的cash总和
        """

        pass

    def pull(self, account_cookie=None, collection=DATABASE.account):
        'pull from the databases'
        if account_cookie is None:
            for item in self.accounts.keys():
                try:
                    message = collection.find_one({'account_cookie': item})
                    QA_util_log_info('{} sync successfully'.format(item))
                except Exception as e:
                    QA_util_log_info(
                        '{} sync wrong \\\n wrong info {}'.format(item, e))
                self.accounts[item].from_message(message)

        else:
            try:
                message = collection.find_one(
                    {'account_cookie': account_cookie})
                QA_util_log_info('{} sync successfully'.format(item))
            except Exception as e:
                QA_util_log_info(
                    '{} sync wrong \\\n wrong info {}'.format(account_cookie, e))
            self.accounts[account_cookie].from_message(message)

    def push(self, account_cookie=None, collection=DATABASE.account):
        'push to databases'
        message = self.accounts[account_cookie].message
        if account_cookie is None:
            for item in self.accounts.keys():
                try:
                    message = collection.find_one_and_update(
                        {'account_cookie': item})
                    QA_util_log_info('{} sync successfully'.format(item))
                except Exception as e:
                    QA_util_log_info(
                        '{} sync wrong \\\n wrong info {}'.format(item, e))
                self.accounts[item].from_message(message)

        else:
            try:
                message = collection.find_one(
                    {'account_cookie': account_cookie})
                QA_util_log_info('{} sync successfully'.format(item))
            except Exception as e:
                QA_util_log_info(
                    '{} sync wrong \\\n wrong info {}'.format(account_cookie, e))
            self.accounts[account_cookie].from_message(message)
