# coding=utf-8
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
import os
import webbrowser

from pyecharts import Kline

from QUANTAXIS.QAUtil.QALogs import QA_util_log_info


"""
0.5.1预计新增内容:


维护一个画图方法,之后可能会做成抽象基类


主要是画DataStruct的k线图, DataStruct加指标的图,以及回测框架的回测结果的图
"""


def plot_datastruct(_quotation_base, code=None):
    if code is None:
        path_name = '.' + os.sep + 'QA_' + _quotation_base.type + \
            '_codepackage_' + _quotation_base.if_fq + '.html'
        kline = Kline('CodePackage_' + _quotation_base.if_fq + '_' + _quotation_base.type,
                      width=1360, height=700, page_title='QUANTAXIS')

        data_splits = _quotation_base.splits()

        for i_ in range(len(data_splits)):
            data = []
            axis = []
            for dates, row in data_splits[i_].data.iterrows():
                open, high, low, close = row[1:5]
                datas = [open, close, low, high]
                axis.append(dates[0])
                data.append(datas)

            kline.add(_quotation_base.code[i_], axis, data, mark_point=[
                      "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
        kline.render(path_name)
        webbrowser.open(path_name)
        QA_util_log_info('The Pic has been saved to your path: %s' % path_name)
    else:
        data = []
        axis = []
        for dates, row in _quotation_base.select_code(code).data.iterrows():
            open, high, low, close = row[1:5]
            datas = [open, close, low, high]
            axis.append(dates[0])
            data.append(datas)

        path_name = '.' + os.sep + 'QA_' + _quotation_base.type + \
            '_' + code + '_' + _quotation_base.if_fq + '.html'
        kline = Kline(code + '__' + _quotation_base.if_fq + '__' + _quotation_base.type,
                      width=1360, height=700, page_title='QUANTAXIS')
        kline.add(code, axis, data, mark_point=[
                  "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
        kline.render(path_name)
        webbrowser.open(path_name)
        QA_util_log_info('The Pic has been saved to your path: %s' % path_name)


def QA_plot_save_html(pic_handle, path, if_open_web):
    pic_handle.render(path)
    if if_open_web:
        webbrowser.open(path)
    else:
        pass
    QA_util_log_info('The Pic has been saved to your path: %s' % path)
