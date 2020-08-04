#
# The MIT License (MIT)
#
# Copyright (c) 2016-2020 yutiansut/QUANTAXIS
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
from QUANTAXIS.QAIndicator.indicators import *
from QUANTAXIS.QAIndicator.base import *
try:
    from QUANTAXIS.QAIndicator.talib_series import *
    from QUANTAXIS.QAIndicator.talib_numpy import *
    from QUANTAXIS.QAIndicator import talib_indicators as talib_qa
except:
    print('PLEASE install TALIB to call these methods')
"""
这个模块是对了对应QA_DataStruct

可以被add_func来添加,所以 这个模块的函数必须有一个DataFrame的输入


例如

import QUANTAXIS as QA
data=QA.QA_fetch_stock_day_adv('000001','2017-01-01','2017-01-31')
data.add_func(QA.)
"""
