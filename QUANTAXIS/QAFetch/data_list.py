# encoding: UTF-8
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

"""
0201e20000000000 RZRQ (融资融券标的) 1000009226000000 RQ (转融券标的) a001050100000000 ST(ST股)

a001050200000000 SST (*ST)  1000023325000000 YJ(预警 SZSE) a001050d00000000 小盘股

a001050e00000000 大盘蓝筹 0201240000000000 cixin(次新股)
"""
wind_stock_list_special_id = {'rzrq': '0201e20000000000',
                              'rq': '1000009226000000',
                              'st': 'a001050100000000',
                              'sst': 'a001050200000000',
                              'yj': '1000023325000000',
                              'small': 'a001050d00000000',
                              'big': 'a001050e00000000',
                              'cixin': '0201240000000000'
                              }
