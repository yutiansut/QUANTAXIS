# coding:utf-8
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
#
#
import datetime
import threading
import time
import calendar
import math

from QUANTAXIS.QAUtil.QALogs import QA_util_log_info

# 🛠todo 时间函数 建议使用这些
#  字符串 和 datetime date time 类型之间的转换
#  QA_util__str_to_dateime
#
#  QA_util__datetime_to_str19
#  QA_util__datetime_to_str10

#  QA_util__str10_to_datetime
#  QA_util__str19_to_datetime

#  QA_util__int10_to_datetime
#  QA_util__int19_to_datetime

#  QA_util__date_to_str10
#  QA_util__date_to_str19

#  QA_util__time_to_str10
#  QA_util__time_to_str19

#  QA_util__str10_to_date
#  QA_util__str10_to_time

#  QA_util__str19_to_time
#  QA_util__str19_to_date

# 或者有更好的方案


def QA_util_time_now():
    """
    返回当前时间
    :return: 类型datetime.datetime
    """
    return datetime.datetime.now()


def QA_util_date_today():
    """
    返回当前日期
    :return: 类型datetime.date
    """
    return datetime.date.today()


def QA_util_today_str():
    """
    返回今天的日期字符串
    :return: 类型字符串 2011-11-11
    """
    dt = QA_util_date_today()
    str = QA_util_datetime_to_strdate(dt)
    return str


def QA_util_date_str2int(date):
    """
    日期字符串 '2011-09-11' 变换成 整数 20110911
    日期字符串 '2018-12-01' 变换成 整数 20181201
    :param date: str日期字符串
    :return: 类型int
    """
    # return int(str(date)[0:4] + str(date)[5:7] + str(date)[8:10])
    if isinstance(date, str):
        return int(str().join(date.split('-')))
    elif isinstance(date, int):
        return date


def QA_util_date_int2str(int_date):
    """
    类型datetime.datatime
    :param date: int 8位整数
    :return: 类型str
    """
    if isinstance(int_date, int):
        return str(str(int_date)[0:4] + '-' + str(int_date)[4:6] + '-' + str(int_date)[6:8])
    elif isinstance(int_date, str):
        return int_date


def QA_util_to_datetime(time):
    """
    字符串 '2018-01-01'  转变成 datatime 类型
    :param time: 字符串str -- 格式必须是 2018-01-01 ，长度10
    :return: 类型datetime.datatime
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
    :param dt:  pythone datetime.datetime
    :return:  1999-02-01 string type
    """
    strdate = "%04d-%02d-%02d" % (dt.year, dt.month, dt.day)
    return strdate


def QA_util_datetime_to_strdatetime(dt):
    """
    :param dt:  pythone datetime.datetime
    :return:  1999-02-01 09:30:91 string type
    """
    strdatetime = "%04d-%02d-%02d %02d:%02d:%02d" % (
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    return strdatetime


def QA_util_date_stamp(date):
    """
    字符串 '2018-01-01'  转变成 float 类型时间 类似 time.time() 返回的类型
    :param date: 字符串str -- 格式必须是 2018-01-01 ，长度10
    :return: 类型float
    """
    datestr = str(date)[0:10]
    date = time.mktime(time.strptime(datestr, '%Y-%m-%d'))
    return date


def QA_util_time_stamp(time_):
    """
    字符串 '2018-01-01 00:00:00'  转变成 float 类型时间 类似 time.time() 返回的类型
    :param time_: 字符串str -- 数据格式 最好是%Y-%m-%d %H:%M:%S 中间要有空格
    :return: 类型float
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


def QA_util_pands_timestamp_to_date(pandsTimestamp):
    """
    转换 pandas 的时间戳 到 datetime.date类型
    :param pandsTimestamp: 类型 pandas._libs.tslib.Timestamp
    :return: datetime.datetime类型
    """
    return pandsTimestamp.to_pydatetime().date()


def QA_util_pands_timestamp_to_datetime(pandsTimestamp):
    """
    转换 pandas 的时间戳 到 datetime.datetime类型
    :param pandsTimestamp: 类型 pandas._libs.tslib.Timestamp
    :return: datetime.datetime类型
    """
    return pandsTimestamp.to_pydatetime()


def QA_util_stamp2datetime(timestamp):
    """
    datestamp转datetime
    pandas转出来的timestamp是13位整数 要/1000
    It’s common for this to be restricted to years from 1970 through 2038.
    从1970年开始的纳秒到当前的计数 转变成 float 类型时间 类似 time.time() 返回的类型
    :param timestamp: long类型
    :return: 类型float
    """
    try:
        return datetime.datetime.fromtimestamp(timestamp)
    except Exception as e:
        # it won't work ??
        return datetime.datetime.fromtimestamp(timestamp / 1000)
    #


def QA_util_ms_stamp(ms):
    """
    直接返回不做处理
    :param ms:  long类型 -- tick count
    :return: 返回ms
    """
    return ms


def QA_util_date_valid(date):
    """
    判断字符串是否是 1982-05-11 这种格式
    :param date: date 字符串str -- 格式 字符串长度10
    :return: boolean -- 格式是否正确
    """
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def QA_util_realtime(strtime, client):
    """
    查询数据库中的数据
    :param strtime: strtime  str字符串                 -- 1999-12-11 这种格式
    :param client: client  pymongo.MongoClient类型    -- mongodb 数据库 从 QA_util_sql_mongo_setting 中 QA_util_sql_mongo_setting 获取
    :return: Dictionary  -- {'time_real': 时间,'id': id}
    """
    time_stamp = QA_util_date_stamp(strtime)
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'date_stamp': {"$gte": time_stamp}})
    time_real = temp_str['date']
    time_id = temp_str['num']
    return {'time_real': time_real, 'id': time_id}


def QA_util_id2date(idx, client):
    """
    从数据库中查询 通达信时间
    :param idx: 字符串 -- 数据库index
    :param client: pymongo.MongoClient类型    -- mongodb 数据库 从 QA_util_sql_mongo_setting 中 QA_util_sql_mongo_setting 获取
    :return:         Str -- 通达信数据库时间
    """
    coll = client.quantaxis.trade_date
    temp_str = coll.find_one({'num': idx})
    return temp_str['date']


def QA_util_is_trade(date, code, client):
    """
    判断是否是交易日
    从数据库中查询
    :param date: str类型 -- 1999-12-11 这种格式    10位字符串
    :param code: str类型 -- 股票代码 例如 603658 ， 6位字符串
    :param client: pymongo.MongoClient类型    -- mongodb 数据库 从 QA_util_sql_mongo_setting 中 QA_util_sql_mongo_setting 获取
    :return:  Boolean -- 是否是交易时间
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
    返回在trade_list中的index位置
    :param date: str类型 -- 1999-12-11 这种格式    10位字符串
    :param trade_list: ？？
    :return: ？？
    """
    return trade_list.index(date)


def QA_util_get_index_date(id, trade_list):
    """
    :param id:  ：？？
    :param trade_list:  ？？
    :return: ？？
    """
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
    """
    'quantaxis的时间选择函数,约定时间的范围,比如30分到59分'
    :param time:
    :param gt:
    :param lt:
    :param gte:
    :param lte:
    :return:
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
    '这是一个用于复用/比如说@装饰器的延时函数\
    使用threading里面的延时,为了是不阻塞进程\
    有时候,同时发进去两个函数,第一个函数需要延时\
    第二个不需要的话,用sleep就会阻塞掉第二个进程'
    :param time_:
    :return:
    """
    def _exec(func):
        threading.Timer(time_, func)
    return _exec


def QA_util_calc_time(func, *args, **kwargs):
    """
    '耗时长度的装饰器'
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    _time = datetime.datetime.now()
    func(*args, **kwargs)
    print(datetime.datetime.now() - _time)
    # return datetime.datetime.now() - _time

def QA_util_getBetweenMonth(from_date, to_date):
    """
    #返回所有月份，以及每月的起始日期、结束日期，字典格式
    """
    date_list = {}
    begin_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m")
        date_list[date_str] = ['%d-%d-01'%(begin_date.year, begin_date.month),
                               '%d-%d-%d'%(begin_date.year, begin_date.month,
                                           calendar.monthrange(begin_date.year, begin_date.month)[1])]
        begin_date = QA_util_get_1st_of_next_month(begin_date)
    return(date_list)

def QA_util_add_months(dt,months):
    """
    #返回dt隔months个月后的日期，months相当于步长
    """
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d")
    month = dt.month - 1 + months
    year = dt.year + math.ceil(month / 12)
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, int(month))[1])
    return(dt.replace(year=year, month=month, day=day))

def QA_util_get_1st_of_next_month(dt):
    """
    获取下个月第一天的日期
    :return: 返回日期
    """
    year=dt.year
    month=dt.month
    if month==12:
        month=1
        year+=1
    else:
        month+=1
    res=datetime.datetime(year,month,1)
    return(res)

def QA_util_getBetweenQuarter(begin_date, end_date):
    """
    #加上每季度的起始日期、结束日期
    """
    quarter_list = {}
    month_list = QA_util_getBetweenMonth(begin_date, end_date)
    for value in month_list:
        tempvalue = value.split("-")
        year = tempvalue[0]
        if tempvalue[1] in ['01', '02', '03']:
            quarter_list[year + "Q1"] = ['%s-01-01' % year, '%s-03-31' % year]
        elif tempvalue[1] in ['04','05','06']:
            quarter_list[year + "Q2"] = ['%s-04-01' % year, '%s-06-30' % year]
        elif tempvalue[1] in ['07', '08', '09']:
            quarter_list[year + "Q3"] = ['%s-07-31' % year, '%s-09-30' % year]
        elif tempvalue[1] in ['10', '11', '12']:
            quarter_list[year + "Q4"] = ['%s-10-01' % year, '%s-12-31' % year]
    # quarter_set = set(quarter_list)
    # quarter_list = list(quarter_set)
    # quarter_list.sort()
    return(quarter_list)

month_data = ['1996-03-31',
              '1996-06-30',
              '1996-09-30',
              '1996-12-31',
              '1997-03-31',
              '1997-06-30',
              '1997-09-30',
              '1997-12-31',
              '1998-03-31',
              '1998-06-30',
              '1998-09-30',
              '1998-12-31',
              '1999-03-31',
              '1999-06-30',
              '1999-09-30',
              '1999-12-31',
              '2000-03-31',
              '2000-06-30',
              '2000-09-30',
              '2000-12-31',
              '2001-03-31',
              '2001-06-30',
              '2001-09-30',
              '2001-12-31',
              '2002-03-31',
              '2002-06-30',
              '2002-09-30',
              '2002-12-31',
              '2003-03-31',
              '2003-06-30',
              '2003-09-30',
              '2003-12-31',
              '2004-03-31',
              '2004-06-30',
              '2004-09-30',
              '2004-12-31',
              '2005-03-31',
              '2005-06-30',
              '2005-09-30',
              '2005-12-31',
              '2006-03-31',
              '2006-06-30',
              '2006-09-30',
              '2006-12-31',
              '2007-03-31',
              '2007-06-30',
              '2007-09-30',
              '2007-12-31',
              '2008-03-31',
              '2008-06-30',
              '2008-09-30',
              '2008-12-31',
              '2009-03-31',
              '2009-06-30',
              '2009-09-30',
              '2009-12-31',
              '2010-03-31',
              '2010-06-30',
              '2010-09-30',
              '2010-12-31',
              '2011-03-31',
              '2011-06-30',
              '2011-09-30',
              '2011-12-31',
              '2012-03-31',
              '2012-06-30',
              '2012-09-30',
              '2012-12-31',
              '2013-03-31',
              '2013-06-30',
              '2013-09-30',
              '2013-12-31',
              '2014-03-31',
              '2014-06-30',
              '2014-09-30',
              '2014-12-31',
              '2015-03-31',
              '2015-06-30',
              '2015-09-30',
              '2015-12-31',
              '2016-03-31',
              '2016-06-30',
              '2016-09-30',
              '2016-12-31',
              '2017-03-31',
              '2017-06-30',
              '2017-09-30',
              '2017-12-31',
              '2018-03-31',
              '2018-06-30',
              '2018-09-30',
              '2018-12-31']


if __name__ == '__main__':
    print(QA_util_time_stamp('2017-01-01 10:25:08'))
