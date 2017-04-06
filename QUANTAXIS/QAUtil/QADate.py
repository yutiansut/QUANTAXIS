import datetime
import time
import re

def QA_util_date_stamp(date):
    #封装的日期函数
    datestr=str(date)[0:10]
    date=time.mktime(time.strptime(datestr,'%Y-%m-%d'))
    return date
def QA_util_time_stamp(time):
    time=str(time)[0:10]
    
    return time
def QA_util_ms_stamp(ms):
    return ms

def QA_util_date_valid(date):
    try:
        
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False