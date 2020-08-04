# coding:utf-8
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
#
#
import datetime
import threading
import time
import pandas as pd

from QUANTAXIS.QAUtil.QALogs import QA_util_log_info

QATZInfo_CN = 'Asia/Shanghai'


def QA_util_time_now():
    """
    explanation:
       获取当前日期时间
    
    return:
        datetime
    """
    return datetime.datetime.now()


def QA_util_date_today():
    """
    explanation:
       获取当前日期

    return:
        date
    """
    return datetime.date.today()


def QA_util_today_str():
    """
    explanation:
        返回今天的日期字符串
    
    return:
        str
    """
    dt = QA_util_date_today()
    return QA_util_datetime_to_strdate(dt)


def QA_util_date_str2int(date):
    """
    explanation:
        转换日期字符串为整数
    
    params:
        * date->
            含义: 日期字符串
            类型: date
            参数支持: []
    
    demonstrate:
        print(QA_util_date_str2int("2011-09-11"))

    return:
        int

    output:
        >>20110911
    """
    # return int(str(date)[0:4] + str(date)[5:7] + str(date)[8:10])
    if isinstance(date, str):
        return int(str().join(date.split('-')))
    elif isinstance(date, int):
        return date


def QA_util_date_int2str(int_date):
    """
    explanation:
        转换日期整数为字符串
    
    params:
        * int_date->
            含义: 日期转换得
            类型: int
            参数支持: []
    
    return:
        str
    """
    date = str(int_date)
    if len(date) == 8:
        return str(date[0:4] + '-' + date[4:6] + '-' + date[6:8])
    elif len(date) == 10:
        return date


def QA_util_to_datetime(time):
    """
    explanation:
        转换字符串格式的日期为datetime
    
    params:
        * time->
            含义: 日期
            类型: str
            参数支持: []
    
    return:
        datetime
    """
    if len(str(time)) == 10:
        _time = '{} 00:00:00'.format(time)
    elif len(str(time)) == 19:
        _time = str(time)
    else:
        QA_util_log_info('WRONG DATETIME FORMAT {}'.format(time))
    return datetime.datetime.strptime(_time, '%Y-%m-%d %H:%M:%S')


def QA_util_datetime_to_strdate(dt):
    """
    explanation:
        转换字符串格式的日期为datetime
    
    params:
        * dt->
            含义: 日期时间
            类型: datetime
            参数支持: []

    return:
        str
    """
    strdate = "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)
    return strdate


def QA_util_datetime_to_strdatetime(dt):
    """
    explanation:
        转换日期时间为字符串格式
    
    params:
        * dt->
            含义: 日期时间
            类型: datetime
            参数支持: []

    return:
        datetime
        
    """
    strdatetime = "%04d-%02d-%02d %02d:%02d:%02d" % (
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second
    )
    return strdatetime


def QA_util_date_stamp(date):
    """
    explanation:
        转换日期时间字符串为浮点数的时间戳
    
    params:
        * date->
            含义: 日期时间
            类型: str
            参数支持: []
    
    return:
        time
    """
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date


def QA_util_time_stamp(time_):
    """
    explanation:
       转换日期时间的字符串为浮点数的时间戳
    
    params:
        * time_->
            含义: 日期时间
            类型: str
            参数支持: ['2018-01-01 00:00:00']

    return:
        time
    """
    if len(str(time_)) == 10:
        # yyyy-mm-dd格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d'))
    elif len(str(time_)) == 16:
        # yyyy-mm-dd hh:mm格式
        return time.mktime(time.strptime(time_, '%Y-%m-%d %H:%M'))
    else:
        timestr = str(time_)[0:19]
        return time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M:%S'))


def QA_util_tdxtimestamp(time_stamp):

    """
    explanation:
       转换tdx的realtimeQuote数据, [相关地址](https://github.com/rainx/pytdx/issues/187#issuecomment-441270487)
    
    params:
        * time_stamp->
            含义: 时间
            类型: str
            参数支持: []

    return:
        int

    """
    if time_stamp is not None:
        time_stamp = str(time_stamp)
        time = time_stamp[:-6] + ':'
        if int(time_stamp[-6:-4]) < 60:
            time += '%s:' % time_stamp[-6:-4]
            time += '%06.3f' % (
                int(time_stamp[-4:]) * 60 / 10000.0
            )
        else:
            time += '%02d:' % (
                int(time_stamp[-6:]) * 60 / 1000000
            )
            time += '%06.3f' % (
                (int(time_stamp[-6:]) * 60 % 1000000) * 60 / 1000000.0
            )
        return time


def QA_util_pands_timestamp_to_date(pandsTimestamp):
    """
    explanation:
        转换 pandas 的时间戳 到 datetime.date类型
    
    params:
        * pandsTimestamp->
            含义: pandas的时间戳
            类型:  pandas._libs.tslib.Timestamp
            参数支持: []
    return:
        date
    """
    return pandsTimestamp.to_pydatetime().date()


def QA_util_pands_timestamp_to_datetime(pandsTimestamp):
    """
    explanation:
        转换 pandas时间戳 到 datetime.datetime类型
    
    params:
        * pandsTimestamp->
            含义: pandas时间戳
            类型:  pandas._libs.tslib.Timestamp
            参数支持: []
    return:
        datetime
    """
    return pandsTimestamp.to_pydatetime()


def QA_util_stamp2datetime(timestamp):
    """
    explanation:
        datestamp转datetime,pandas转出来的timestamp是13位整数 要/1000,
        It’s common for this to be restricted to years from 1970 through 2038.
        从1970年开始的纳秒到当前的计数 转变成 float 类型时间 类似 time.time() 返回的类型
    
    params:
        * timestamp->
            含义: 时间戳
            类型: float
            参数支持: []
    
    return:
        datetime
    """
    try:
        return datetime.datetime.fromtimestamp(timestamp)
    except Exception as e:
        # it won't work ??
        try:
            return datetime.datetime.fromtimestamp(timestamp / 1000)
        except:
            try:
                return datetime.datetime.fromtimestamp(timestamp / 1000000)
            except:
                return datetime.datetime.fromtimestamp(timestamp / 1000000000)

    #


def QA_util_ms_stamp(ms):
    """
    explanation:
        直接返回不做处理

    params:
        * ms->
            含义: 时间戳
            类型: float
            参数支持: []
    return:
        float
    """
    
    return ms


def QA_util_date_valid(date):
    """
    explanation:
        判断字符串格式(1982-05-11)

    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
    
    return:
        bool
    """
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def QA_util_realtime(strtime, client):
    """
    explanation:
        查询数据库中的数据

    params:
        * strtime->
            含义: 日期
            类型: str
            参数支持: []
        * client->
            含义: 源
            类型: pymongo.MongoClient
            参数支持: []

    return:
        dict
    """
    time_stamp = QA_util_date_stamp(strtime)
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'date_stamp': {"$gte": time_stamp}})
    time_real = temp_str['date']
    time_id = temp_str['num']
    return {'time_real': time_real, 'id': time_id}


def QA_util_id2date(idx, client):
    """
    explanation:
         从数据库中查询通达信时间

    params:
        * idx->
            含义: 数据库index
            类型: str
            参数支持: []
        * client->
            含义: 源
            类型: pymongo.MongoClient
            参数支持: []

    return:
        str
    """
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'num': idx})
    return temp_str['date']


def QA_util_is_trade(date, code, client):
    """
    explanation:
        从数据库中查询判断是否是交易日

    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
        * code->
            含义: 代码
            类型: str
            参数支持: []
        * client->
            含义: 源
            类型: pymongo.MongoClient
            参数支持: []

    return:
        bool
    """
    coll = client.quantaxis.stock_day
    date = str(date)[0:10]
    is_trade = coll.find_one({'code': code, 'date': date})
    try:
        len(is_trade)
        return True
    except:
        return False


def QA_util_get_date_index(date, trade_list):
    """
    explanation:
        返回在trade_list中的index位置

    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
        * trade_list->
            含义: 代码
            类型: ??
            参数支持: []
        
    return:
        ??
    """
    return trade_list.index(date)


def QA_util_get_index_date(id, trade_list):
    """
    explanation:
        根据id索引值

    params:
        * id->
            含义: 日期
            类型: str
            参数支持: []
        * trade_list->
            含义: 代码
            类型: dict
            参数支持: []
        
    return:
        ??
    """
    return trade_list[id]


def QA_util_select_hours(time=None, gt=None, lt=None, gte=None, lte=None):
    """
    explanation:
        quantaxis的时间选择函数,约定时间的范围,比如早上9点到11点

    params:
        * time->
            含义: 时间
            类型: str
            参数支持: []
        * gt->
            含义: 大于
            类型: Any
            参数支持: []
        * lt->
            含义: 小于
            类型: Any
            参数支持: []
        * gte->
            含义: 大于等于
            类型: Any
            参数支持: []
        * lte->
            含义: 小于等于
            类型: Any
            参数支持: []

    return:
        bool
    """
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
    """
    explanation:
        择分钟

    params:
        * time->
            含义: 时间
            类型: str
            参数支持: []
        * gt->
            含义: 大于等于
            类型: Any
            参数支持: []
        * lt->
            含义: 小于
            类型: Any
            参数支持: []
        * gte->
            含义: 大于等于
            类型: Any
            参数支持: []
        * lte->
            含义: 小于等于
            类型: Any
            参数支持: []

    return:
        bool
    """
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
    """
    explanation:
        这是一个用于复用/比如说@装饰器的延时函数,使用threading里面的延时,为了是不阻塞进程,
        有时候,同时发进去两个函数,第一个函数需要延时,第二个不需要的话,用sleep就会阻塞掉第二个进程

    params:
        * time_->
            含义: 时间
            类型: time
            参数支持: []
        
    return:
        func
    """

    def _exec(func):
        threading.Timer(time_, func)

    return _exec


def QA_util_calc_time(func, *args, **kwargs):
    """
    explanation:
        耗时长度的装饰器

    params:
        * func ->
            含义: 被装饰的函数
            类型: func
            参数支持: []
        * args ->
            含义: 函数接受的任意元组参数
            类型: tuple
            参数支持: []
        * kwargs ->
            含义: 函数接受的任意字典参数
            类型: dict
            参数支持: []

    return:
        None
    """
    _time = datetime.datetime.now()
    func(*args, **kwargs)
    print(datetime.datetime.now() - _time)
    # return datetime.datetime.now() - _time


month_data = pd.date_range(
    '1/1/1996',
    '12/31/2023',
    freq='Q-MAR'
).astype(str).tolist()

if __name__ == '__main__':
    print(QA_util_time_stamp('2017-01-01 10:25:08'))
