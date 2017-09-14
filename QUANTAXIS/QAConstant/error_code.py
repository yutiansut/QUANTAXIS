# coding=utf-8
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


class QUANTAXIS_Error():
    QUANTAXIS_Error_framework_error = 0100

# QUANTAXIS 框架错误代码 0000-0999
QUANTAXIS_error = {}
# 数据获取/数据库读取错误代码 1000-1999
QA_fetch_error = {}
# 数据错误代码 保存部分 2000-2499
QA_save_error = {}

# 数据错误代码  更新部分 2500-2599
QA_update_error = {}
# 交易错误代码(模拟market返回) 3000-3999
QA_market_error = {}

# 回测错误代码 4000-4999
QA_backtest_error = {
    # 通用错误代码
    'total': {

    },
    # 特定错误代码
    'QA_backtest_stock_day': {

    },
    'QA_backtest_stock_min': {},
    'QA_backtest_stock_tick': {},
    'QA_backtest_future_day': {},
    'QA_backtest_future_min': {},
    'QA_backtest_future_tick': {}

}
