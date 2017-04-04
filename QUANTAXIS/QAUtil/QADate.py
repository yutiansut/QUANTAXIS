import datetime
import time
import re



def util_date_stamp(date):
    #封装的日期函数
    datestr=str(date)[0:10]
    date=time.mktime(time.strptime(datestr,'%Y-%m-%d'))
    return date
def util_time_stamp(time):
    time=str(time)[0:10]
    
    return time
def util_ms_stamp(ms):
    return ms