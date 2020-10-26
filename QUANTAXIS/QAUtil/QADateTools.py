import datetime
import calendar
from dateutil.relativedelta import relativedelta
from QUANTAXIS.QAUtil.QASetting import (DATABASE)
import pymongo
import pandas as pd
def QA_util_getBetweenMonth(from_date, to_date):

    """
    explanation:
        返回所有月份，以及每月的起始日期、结束日期，字典格式		

    params:
        * from_date ->:
            meaning: 起始日期
            type: null
            optional: [null]
        * to_date ->:
            meaning: 结束日期
            type: null
            optional: [null]

    return:
        dict
	
    demonstrate:
        Not described
	
    output:
        Not described
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
    explanation:
        返回dt隔months个月后的日期，months相当于步长

    params:
        * dt ->:
            meaning:日期
            type: null
            optional: [null]
        * months ->:
            meaning:步长
            type: null
            optional: [null]

    return:
        datetime
	
    demonstrate:
        Not described
	
    output:
        Not described
    """

    """
  
    """
    dt = datetime.datetime.strptime(
        dt, "%Y-%m-%d") + relativedelta(months=months)
    return(dt)


def QA_util_get_1st_of_next_month(dt):
    """
    explanation:
         获取下个月第一天的日期

    params:
        * dt ->:
            meaning:当天日期
            type: datetime
            optional: [null]

    return:
        datetime
	
    demonstrate:
        Not described
	
    output:
        Not described
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
    explanation:
        加上每季度的起始日期、结束日期	

    params:
        * begin_date ->:
            meaning: 起始日期
            type: null
            optional: [null]
        * end_date ->:
            meaning: 结束日期
            type: null
            optional: [null]

    return:
        dict
	
    demonstrate:
        Not described
	
    output:
        Not described
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


def QA_util_firstDayTrading(codelist: list):
    """
    explanation:
        获取交易品种的第一个上市日期，或第一个交易日。支持混合股票,index,etf		

    params:
        * codelist ->:
            meaning: stcok/index/etf 代码列表
            type: list
            optional: [null]

    return:
        pandas.DataFrame: the code with its first trading date
	
    demonstrate:
        QA_util_firstDayTrading(['600066','510050','000300'])
	
    output:
        Not described
    """

    coll_stock_day = DATABASE.stock_day
    coll_index_day = DATABASE.index_day
    coll_stock_day.create_index(
    [("code",
      pymongo.ASCENDING),
     ("date_stamp",
      pymongo.ASCENDING)]
    )
    coll_index_day.create_index(
    [("code",
      pymongo.ASCENDING),
     ("date_stamp",
      pymongo.ASCENDING)]
    )

    dates = []
    for code in codelist:
        ref = coll_stock_day.find({"code": code})
        ref2 = coll_index_day.find({'code': code})
        #print('{} is ref is {}, ref2 is {}'.format(code, ref.count(), ref2.count()))
        if ref.count() > 0:
            start_date = ref[0]['date']
            dates.append(start_date)
        elif ref2.count() > 0:
            start_date = ref2[0]['date']
            dates.append(start_date)
        else:
            raise ValueError('{} 没有数据'.format(code))

    return pd.DataFrame({'code':codelist, 'date': dates} )
