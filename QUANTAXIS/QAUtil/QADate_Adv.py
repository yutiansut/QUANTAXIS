# coding:utf-8
# Author:阿财（11652964@qq.com）
# Created date: 2018-06-03
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
from datetime import datetime, timezone, timedelta
import threading
import time
import numpy as np

from QUANTAXIS.QAUtil.QALogs import QA_util_log_info


def QA_util_datetime_to_Unix_timestamp(ts_epoch = None):  
    """
    返回当前UTC时间戳，默认时区为北京时间
    :return: 类型 int
    """
    if (ts_epoch is None):
        ts_epoch = datetime.now(timezone(timedelta(hours=8)))

    return (ts_epoch - datetime(1970,1,1, tzinfo=timezone.utc)).total_seconds()


def QA_util_timestamp_to_str(ts_epoch = None, local_tz = timezone(timedelta(hours=8))):
    """
    返回字符串格式时间
    :return: 类型string
    """
    if (ts_epoch is None):
        ts_epoch = datetime.now(timezone(timedelta(hours=8)))

    if isinstance(ts_epoch, datetime):
        try:
            return ts_epoch.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ts_epoch.tz_localize(local_tz).strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(ts_epoch, int) or isinstance(ts_epoch, np.int32) or isinstance(ts_epoch, np.int64) or isinstance(ts_epoch, float):
        return (datetime(1970,1,1, tzinfo=timezone.utc) + timedelta(seconds = int(ts_epoch))).astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise Exception('No support type %s.' % type(ts_epoch))


def QA_util_str_to_Unix_timestamp(time_, tz_str= ' +0800'):
    """
    默认时区为 北京时间
    字符串 '2018-01-01 00:00:00'  转变成 int 类型时间 类似 time.time() 返回的类型
    :param time_: 字符串str -- 数据格式 最好是%Y-%m-%d %H:%M:%S 中间要有空格
    :return: 类型 int
    """
    if len(str(time_)) == 10:
        # yyyy-mm-dd格式
        return QA_util_datetime_to_Unix_timestamp(datetime.strptime(time_ + tz_str, '%Y-%m-%d %z'))
    elif len(str(time_)) == 16:
        # yyyy-mm-dd hh:mm格式
        return QA_util_datetime_to_Unix_timestamp(datetime.strptime(time_ + tz_str, '%Y-%m-%d %H:%M %z'))
    else:
        timestr = str(time_)[0:19]
        return QA_util_datetime_to_Unix_timestamp(datetime.strptime(time_ + tz_str, '%Y-%m-%d %H:%M:%S %z'))

    
def QA_util_str_to_datetime(time, tz_str= ' +0800'):
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
    return datetime.strptime(_time + tz_str, '%Y-%m-%d %H:%M:%S %z')


#def QA_util_str_to_Unix_timestamp(dtStr = '2018-01-01 00:00:00'):
#    """
#    返回字符串格式时间
#    :return: 类型long
#    """
#    if isinstance(dtStr, str):
#        dtDateTime = QA_util_to_datetime(dtStr)
#    elif isinstance(dtStr, datetime):
#        dtDateTime = dtStr
#    else:
#        raise Exception('Invailed datetime.')

#    epoch_datetime = datetime(1970,1,1, 0, 0, 0)
#    return (dtDateTime - epoch_datetime).total_seconds()


#def QA_util_datetime_to_Unix_timestamp(dtDatetime = datetime.now()):
#    """
#    返回当前UTC时间戳
#    :return: 类型datetime
#    """

#    return QA_util_str_to_Unix_timestamp(dtDatetime)

def QA_util_print_timestamp(ts_epoch):
    """
    打印合适阅读的时间格式
    """
    return '{:s}({:d})'.format(
        QA_util_timestamp_to_str(ts_epoch)[2:16],
        int(ts_epoch)
    )


if __name__ == '__main__':
    print(QA_util_time_stamp('2017-01-01 10:25:08'))
