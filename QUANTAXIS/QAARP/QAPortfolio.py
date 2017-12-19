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

import threading

from QUANTAXIS.QAUtil import (QA_util_date_stamp, QA_util_date_valid,
                              QA_util_log_info, QA_Setting)

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QARisk import QA_Risk


class QA_Portfolio():

    """
    QUANTAXIS 多账户
    以及组合管理

    # 状态 未完成
    # 适用 回测/实盘


    在portfolio中,我们希望通过cookie来控制account_unit
    对于account的指标,要进行风险控制,组合成最优的投资组合的量

    用account的cookie来管理控制account
    """

    def __init__(self, portfolio_cookies=[]):
        self.portfolio_accounts = {}
        self.portfolio_cookies = portfolio_cookies
        for cookie in self.portfolio_cookies:
            self.portfolio_accounts[cookie] = QA_Account(account_cookie=cookie)

    def __repr__(self):
        return '<QA_Portfolio with {} Accounts>'.format(len(self.portfolio_cookies))

    def QA_portfolio_get_portfolio(self):
        return self.portfolio_accounts

    def add_account(self, account_cookie):
        temp=QA_Account(account_cookie=account_cookie)
        if account_cookie not in self.portfolio_cookies:
            self.portfolio_cookies.append(temp.account_cookie)
            self.portfolio_accounts[temp.account_cookie] = temp

        else:
            pass        

    def new_account(self, account_cookie=None):
        if account_cookie is None:
            temp = QA_Account()
            if temp.account_cookie not in self.portfolio_cookies:
                self.portfolio_cookies.append(temp.account_cookie)
                self.portfolio_accounts[temp.account_cookie] = temp

            else:
                pass

    def get_account(self, cookie):
        try:
            return self.portfolio_accounts[cookie]
        except:
            QA_util_log_info('Can not find this account')
            return None

    def cookie_mangement(self):
        pass

    def get_cash(self):
        """拿到整个portfolio的可用资金
        
        统计每一个时间点的时候的cash总和
        """
        
        pass

    def pull(self,account_cookie=None,collection=QA_Setting.client.quantaxis.account):
        if account_cookie is None:
            for item in self.portfolio_cookies:
                try:
                    message=collection.find_one({'cookie':item})['message']
                    QA_util_log_info('{} sync successfully'.format(item))
                except Exception as e:
                    QA_util_log_info('{} sync wrong \\\n wrong info {}'.format(item,e))
                self.portfolio_accounts[item].from_message(message)

        else:
            try:
                message=collection.find_one({'cookie':account_cookie})['message']
                QA_util_log_info('{} sync successfully'.format(item))
            except Exception as e:
                QA_util_log_info('{} sync wrong \\\n wrong info {}'.format(account_cookie,e))
            self.portfolio_accounts[account_cookie].from_message(message)          

    def push(self,account_cookie=None,collection=QA_Setting.client.quantaxis.account):
        message=self.portfolio_accounts[account_cookie].message
        if account_cookie is None:
            for item in self.portfolio_cookies:
                try:
                    message=collection.find_one_and_update({'cookie':item})
                    QA_util_log_info('{} sync successfully'.format(item))
                except Exception as e:
                    QA_util_log_info('{} sync wrong \\\n wrong info {}'.format(item,e))
                self.portfolio_accounts[item].from_message(message)

        else:
            try:
                message=collection.find_one({'cookie':account_cookie})['message']
                QA_util_log_info('{} sync successfully'.format(item))
            except Exception as e:
                QA_util_log_info('{} sync wrong \\\n wrong info {}'.format(account_cookie,e))
            self.portfolio_accounts[account_cookie].from_message(message)  