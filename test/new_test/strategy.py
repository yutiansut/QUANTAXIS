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
import random

import QUANTAXIS as QA


class strategy:
    """
    携带一个函数句柄
    """
    @classmethod
    def setting(self):
        pass

    @classmethod
    def predict(self, market, account, hold, info):
        """
        一个极其简单的示例策略,随机 随机真的随机
        """

        if hold == 0:
            __dat = random.random()
            if __dat > 0.5:
                return {'if_buy': 1, 'if_sell': 0, 'amount': 'mean'}
            else:
                return {'if_buy': 0, 'if_sell': 1, 'amount': 'mean'}
        else:
            __dat = random.random()
            if __dat > 0.5:
                return {'if_buy': 1, 'if_sell': 0, 'amount': 'mean'}
            else:

                return {'if_buy': 0, 'if_sell': 1, 'amount': 'all'}


d = QA.QA_Backtest()
# d.QA_backtest_import_setting()
d.QA_backtest_init()
d.QA_backtest_start(strategy())
