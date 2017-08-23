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

from .QAMarket_advance import QA_Market


class stock_market(QA_Market):
    # 设置交易细节

    #
    # self.init()

    # 手续费 Commission
    # 买卖规则  双向市场 平仓优先、时间优先（closing out position and time priority）
    # 返回code
    # 保证金（Margin） 初始保证金（Initial Margin）维持保证金(Maintenance Margin)
    # 结算价
    # 数据级别
    # 最小变动价位（Minimum Price Movement）
    # 每日价格最大波动限制(Daily Price Limit) 10%

    def init(self):
        pass


class future_market():
    def init(self):
        pass


class HK_stock_market():
    pass


class US_stock_market():
    pass
