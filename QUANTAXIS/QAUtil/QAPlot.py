import pyecharts
from pyecharts import Kline
import os
from QUANTAXIS.QAData.QADataStruct import __stock_hq_base
from QUANTAXIS.QAUtil.QALogs import QA_util_log_info
import webbrowser

"""
0.5.1预计新增内容:


维护一个画图方法,之后可能会做成抽象基类


主要是画DataStruct的k线图, DataStruct加指标的图,以及回测框架的回测结果的图
"""
def plot_datastruct(__stock_hq_base, code=None):
    if code is None:
        path_name = '.' + os.sep + 'QA_' + __stock_hq_base.type + \
            '_codepackage_' + __stock_hq_base.if_fq + '.html'
        kline = Kline('CodePackage_' + __stock_hq_base.if_fq + '_' + __stock_hq_base.type,
                      width=1360, height=700, page_title='QUANTAXIS')

        data_splits = __stock_hq_base.splits()

        for i_ in range(len(data_splits)):
            data = []
            axis = []
            for dates, row in data_splits[i_].data.iterrows():
                open, high, low, close = row[1:5]
                datas = [open, close, low, high]
                axis.append(dates[0])
                data.append(datas)

            kline.add(__stock_hq_base.code[i_], axis, data, mark_point=[
                      "max", "min"], is_datazoom_show=True, datazoom_orient='horizontal')
        kline.render(path_name)
        webbrowser.open(path_name)
        QA_util_log_info('The Pic has been saved to your path: %s' % path_name)
    else:
        data = []
        axis = []
        for dates, row in __stock_hq_base.select_code(code).data.iterrows():
            open, high, low, close = row[1:5]
            datas = [open, close, low, high]
            axis.append(dates[0])
            data.append(datas)

        path_name = '.' + os.sep + 'QA_' + __stock_hq_base.type + \
            '_' + code + '_' + __stock_hq_base.if_fq + '.html'
        kline = Kline(code + '__' + __stock_hq_base.if_fq + '__' + __stock_hq_base.type,
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
