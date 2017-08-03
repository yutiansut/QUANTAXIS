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

import datetime
import re
import time
import threading


def QA_util_time_now():
    return datetime.datetime.now()


def QA_util_date_stamp(date):
    # date function
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date

 
def QA_util_time_stamp(time_):
    '''
    数据格式需要是%Y-%m-%d %H:%M:%S 中间要有空格
    '''

    try:
        timestr = str(time_)[0:19]
        time__ = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))
        return time__

    except:
        return QA_util_date_stamp('1900-01-01')


def QA_util_ms_stamp(ms):
    return ms


def QA_util_date_valid(date):
    try:

        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def QA_util_realtime(strtime, client):
    time_stamp = QA_util_date_stamp(strtime)
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'date_stamp': {"$gte": time_stamp}})
    time_real = temp_str['date']
    time_id = temp_str['num']
    return {'time_real': time_real, 'id': time_id}


def QA_util_id2date(id, client):
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'num': id})
    return temp_str['date']


def QA_util_is_trade(date, code, client):
    coll = client.quantaxis.stock_day
    date = str(date)[0:10]
    is_trade = coll.find_one({'code': code, 'date': date})
    try:
        len(is_trade)
        return True
    except:
        return False


def QA_util_get_real_date(date, trade_list, towards):
    """
    获取真实的交易日期,其中,第三个参数towards是表示向前/向后推
    towards=1 日期向后迭代
    towards=-1 日期向前迭代
    @ yutiansut
    
    """
    if towards == 1:
        while date not in trade_list:
            date = str(datetime.datetime.strptime(
                date, '%Y-%m-%d') + datetime.timedelta(days=1))[0:10]
        else:
            return date
    elif towards == -1:
        while date not in trade_list:
            date = str(datetime.datetime.strptime(
                date, '%Y-%m-%d') - datetime.timedelta(days=1))[0:10]
        else:
            return date


def QA_util_get_date_index(date, trade_list):
    return trade_list.index(date)


def QA_util_get_index_date(id, trade_list):
    return trade_list[id]


def QA_util_select_hours(time=None, gt=None, lt=None, gte=None, lte=None):
    'quantaxis的时间选择函数,约定时间的范围,比如早上9点到11点'
    if time is None:
        __realtime = datetime.datetime.now()
    else:
        __realtime = time

    fun_list = []
    if gt != None:
        fun_list.append('>')
    if lt != None:
        fun_list.append('<')
    if gte != None:
        fun_list.append('>=')
    if lte != None:
        fun_list.append('<=')

    assert len(fun_list) > 0
    true_list = []
    try:
        for item in fun_list:
            if item == '>':
                if __realtime.strftime('%H') > gt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<':
                if __realtime.strftime('%H') < lt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '>=':
                if __realtime.strftime('%H') >= gte:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<=':
                if __realtime.strftime('%H') <= lte:
                    true_list.append(0)
                else:
                    true_list.append(1)

    except:
        return Exception
    if sum(true_list) > 0:
        return False
    else:
        return True


def QA_util_select_min(time=None, gt=None, lt=None, gte=None, lte=None):
    'quantaxis的时间选择函数,约定时间的范围,比如30分到59分'
    if time is None:
        __realtime = datetime.datetime.now()
    else:
        __realtime = time

    fun_list = []
    if gt != None:
        fun_list.append('>')
    if lt != None:
        fun_list.append('<')
    if gte != None:
        fun_list.append('>=')
    if lte != None:
        fun_list.append('<=')

    assert len(fun_list) > 0
    true_list = []
    try:
        for item in fun_list:
            if item == '>':
                if __realtime.strftime('%M') > gt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<':
                if __realtime.strftime('%M') < lt:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '>=':
                if __realtime.strftime('%M') >= gte:
                    true_list.append(0)
                else:
                    true_list.append(1)
            elif item == '<=':
                if __realtime.strftime('%M') <= lte:
                    true_list.append(0)
                else:
                    true_list.append(1)

    except:
        return Exception
    if sum(true_list) > 0:
        return False
    else:
        return True



def QA_util_time_delay(time_=0):
    '这是一个用于复用/比如说@装饰器的延时函数\
    使用threading里面的延时,为了是不阻塞进程\
    有时候,同时发进去两个函数,第一个函数需要延时\
    第二个不需要的话,用sleep就会阻塞掉第二个进程'
    def _exec(func):
        threading.Timer(time_,func)
    return _exec


if __name__=='__main__':
    print(QA_util_time_stamp('2017-01-01 10:25:08'))