import datetime
import calendar
from dateutil.relativedelta import relativedelta


def QA_util_getBetweenMonth(from_date, to_date):
    """
    #返回所有月份，以及每月的起始日期、结束日期，字典格式
    """
    date_list = {}
    begin_date = datetime.datetime.strptime(from_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(to_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m")
        date_list[date_str] = ['%d-%d-01' % (begin_date.year, begin_date.month),
                               '%d-%d-%d' % (begin_date.year, begin_date.month,
                                             calendar.monthrange(begin_date.year, begin_date.month)[1])]
        begin_date = QA_util_get_1st_of_next_month(begin_date)
    return(date_list)


def QA_util_add_months(dt, months):
    """
    #返回dt隔months个月后的日期，months相当于步长
    """
    dt = datetime.datetime.strptime(
        dt, "%Y-%m-%d") + relativedelta(months=months)
    return(dt)


def QA_util_get_1st_of_next_month(dt):
    """
    获取下个月第一天的日期
    :return: 返回日期
    """
    year = dt.year
    month = dt.month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    res = datetime.datetime(year, month, 1)
    return res


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
        elif tempvalue[1] in ['04', '05', '06']:
            quarter_list[year + "Q2"] = ['%s-04-01' % year, '%s-06-30' % year]
        elif tempvalue[1] in ['07', '08', '09']:
            quarter_list[year + "Q3"] = ['%s-07-31' % year, '%s-09-30' % year]
        elif tempvalue[1] in ['10', '11', '12']:
            quarter_list[year + "Q4"] = ['%s-10-01' % year, '%s-12-31' % year]
    return(quarter_list)
