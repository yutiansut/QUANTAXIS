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
                              QA_util_log_info)

from QUANTAXIS.QAARP.QAAccount import QA_Account
from QUANTAXIS.QAARP.QARisk import QA_Risk


class QA_Portfolio():

    """
    在portfolio中,我们希望通过cookie来控制account_unit
    对于account的指标,要进行风险控制,组合成最优的投资组合的量

    用account的cookie来管理控制account


    """

    def init(self):
        self.portfolio_account = []
        self.portfolio_cookies=[]
        for i in range(0, len(self.portfolio_cookies) - 1, 1):
            self.portfolio_account[i] = QA_Account(coo)

    def QA_portfolio_get_portfolio(self):
        return self.portfolio_account

    def new_accouts(self,account_cookie=None):
        if account_cookie is None:
            temp=QA_Account()
            if temp.account_cookie is not in self.portfolio_cookies:


    def cookie_mangement(self):
        pass

    def QA_portfolio_get_free_cash(self):
        pass
