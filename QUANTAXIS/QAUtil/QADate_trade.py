# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2021 yutiansut/QUANTAXIS
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
from typing import List, Tuple, Union

import pandas as pd

from QUANTAXIS.QAUtil.QAParameter import FREQUENCE, MARKET_TYPE

#  只记录非交易日，其余的用程序迭代 生成交易日
# 非交易日期
trade_date_sse_exi = [
    "1991-01-01",
    "1991-02-15", "1991-02-18",
    "1991-05-01",
    "1991-10-01", "1991-10-02",

    "1992-01-01",
    "1992-02-04", "1992-02-05", "1992-02-06",
    "1992-05-01", "1992-10-01", "1992-10-02",

    "1993-01-01",
    "1993-01-25", "1993-01-26",
    "1993-10-01",

    "1994-02-07", "1994-02-08", "1994-02-09", "1994-02-10", "1994-02-11",
    "1994-05-02",
    "1994-10-03", "1994-10-04",

    "1995-01-02",
    "1995-01-30", "1995-01-31", "1995-02-01", "1995-02-02", "1995-02-03",
    "1995-05-01",
    "1995-10-02", "1995-10-03",

    "1996-01-01",
    "1996-02-19", "1996-02-20", "1996-02-21", "1996-02-22", "1996-02-23", "1996-02-26", "1996-02-27", "1996-02-28", "1996-02-29", "1996-03-01",
    "1996-05-01",
    "1996-09-30", "1996-10-01", "1996-10-02",

    "1997-01-01",
    "1997-02-03", "1997-02-04", "1997-02-05", "1997-02-06", "1997-02-07", "1997-02-10", "1997-02-11", "1997-02-12", "1997-02-13", "1997-02-14",
    "1997-05-01", "1997-05-02",
    "1997-06-30", "1997-07-01",
    "1997-10-01", "1997-10-02", "1997-10-03",

    "1998-01-01", "1998-01-02",
    "1998-01-26", "1998-01-27", "1998-01-28", "1998-01-29", "1998-01-30", "1998-02-02", "1998-02-03", "1998-02-04", "1998-02-05", "1998-02-06",
    "1998-05-01",
    "1998-10-01", "1998-10-02",

    "1999-01-01",
    "1999-02-10", "1999-02-11", "1999-02-12", "1999-02-15", "1999-02-16", "1999-02-17", "1999-02-18", "1999-02-19", "1999-02-22", "1999-02-23", "1999-02-24", "1999-02-25", "1999-02-26",
    "1999-05-03",
    "1999-10-01", "1999-10-04", "1999-10-05", "1999-10-06", "1999-10-07", "1999-12-20",
    "1999-12-31",

    "2000-01-03",
    "2000-01-31", "2000-02-01", "2000-02-02", "2000-02-03", "2000-02-04", "2000-02-07", "2000-02-08", "2000-02-09", "2000-02-10", "2000-02-11",
    "2000-05-01", "2000-05-02", "2000-05-03", "2000-05-04", "2000-05-05",
    "2000-10-02", "2000-10-03", "2000-10-04", "2000-10-05", "2000-10-06",

    "2001-01-01",
    "2001-01-22", "2001-01-23", "2001-01-24", "2001-01-25", "2001-01-26", "2001-01-29", "2001-01-30", "2001-01-31", "2001-02-01", "2001-02-02",
    "2001-05-01", "2001-05-02", "2001-05-03", "2001-05-04", "2001-05-07",
    "2001-10-01", "2001-10-02", "2001-10-03", "2001-10-04", "2001-10-05",

    "2002-01-01", "2002-01-02", "2002-01-03",
    "2002-02-11", "2002-02-12", "2002-02-13", "2002-02-14", "2002-02-15", "2002-02-18", "2002-02-19", "2002-02-20", "2002-02-21", "2002-02-22",
    "2002-05-01", "2002-05-02", "2002-05-03", "2002-05-06", "2002-05-07",
    "2002-09-30", "2002-10-01", "2002-10-02", "2002-10-03", "2002-10-04", "2002-10-07",

    "2003-01-01",
    "2003-01-30", "2003-01-31", "2003-02-03", "2003-02-04", "2003-02-05", "2003-02-06", "2003-02-07",
    "2003-05-01", "2003-05-02", "2003-05-05", "2003-05-06", "2003-05-07", "2003-05-08", "2003-05-09",
    "2003-10-01", "2003-10-02", "2003-10-03", "2003-10-06", "2003-10-07",

    "2004-01-01",
    "2004-01-19", "2004-01-20", "2004-01-21", "2004-01-22", "2004-01-23",
    "2004-01-26", "2004-01-27", "2004-01-28",
    "2004-05-03", "2004-05-04", "2004-05-05", "2004-05-06", "2004-05-07",
    "2004-10-01", "2004-10-04", "2004-10-05", "2004-10-06", "2004-10-07",

    "2005-01-03",
    "2005-02-07", "2005-02-08", "2005-02-09", "2005-02-10", "2005-02-11", "2005-02-14", "2005-02-15",
    "2005-05-02", "2005-05-03", "2005-05-04", "2005-05-05", "2005-05-06",
    "2005-10-03", "2005-10-04", "2005-10-05", "2005-10-06", "2005-10-07",

    "2006-01-02", "2006-01-03",
    "2006-01-26", "2006-01-27", "2006-01-30", "2006-01-31", "2006-02-01", "2006-02-02", "2006-02-03",
    "2006-05-01", "2006-05-02", "2006-05-03", "2006-05-04", "2006-05-05",
    "2006-10-02", "2006-10-03", "2006-10-04", "2006-10-05", "2006-10-06",

    "2007-01-01", "2007-01-02", "2007-01-03",
    "2007-02-19", "2007-02-20", "2007-02-21", "2007-02-22", "2007-02-23",
    "2007-05-01", "2007-05-02", "2007-05-03", "2007-05-04", "2007-05-07",
    "2007-10-01", "2007-10-02", "2007-10-03", "2007-10-04", "2007-10-05",
    "2007-12-31",

    "2008-01-01",
    "2008-02-06", "2008-02-07", "2008-02-08", "2008-02-11", "2008-02-12",
    "2008-04-04",
    "2008-05-01", "2008-05-02",
    "2008-06-09",
    "2008-09-15",
    "2008-09-29", "2008-09-30", "2008-10-01", "2008-10-02", "2008-10-03",

    "2009-01-01", "2009-01-02",
    "2009-01-26", "2009-01-27", "2009-01-28", "2009-01-29", "2009-01-30",
    "2009-04-06",
    "2009-05-01",
    "2009-05-28", "2009-05-29",
    "2009-10-01", "2009-10-02", "2009-10-05", "2009-10-06", "2009-10-07", "2009-10-08",

    "2010-01-01",
    "2010-02-15", "2010-02-16", "2010-02-17", "2010-02-18", "2010-02-19",
    "2010-04-05",
    "2010-05-03",
    "2010-06-14", "2010-06-15",
    "2010-06-16",
    "2010-09-22", "2010-09-23", "2010-09-24",
    "2010-10-01", "2010-10-04", "2010-10-05", "2010-10-06", "2010-10-07",

    "2011-01-03",
    "2011-02-02", "2011-02-03", "2011-02-04",
    "2011-02-07", "2011-02-08",
    "2011-04-04", "2011-04-05",
    "2011-05-02",
    "2011-06-06",
    "2011-09-12",
    "2011-10-03", "2011-10-04", "2011-10-05", "2011-10-06", "2011-10-07",

    "2012-01-02", "2012-01-03", "2012-01-23",
    "2012-01-24", "2012-01-25", "2012-01-26", "2012-01-27",
    "2012-04-02", "2012-04-03", "2012-04-04",
    "2012-04-30", "2012-05-01",
    "2012-06-22",
    "2012-10-01", "2012-10-02", "2012-10-03", "2012-10-04", "2012-10-05",

    "2013-01-01", "2013-01-02", "2013-01-03",
    "2013-02-11", "2013-02-12", "2013-02-13", "2013-02-14", "2013-02-15",
    "2013-04-04", "2013-04-05",
    "2013-04-29", "2013-04-30", "2013-05-01",
    "2013-06-10", "2013-06-11", "2013-06-12",
    "2013-09-19", "2013-09-20",
    "2013-10-01", "2013-10-02", "2013-10-03", "2013-10-04", "2013-10-07",

    "2014-01-01",
    "2014-01-31", "2014-02-03", "2014-02-04",
    "2014-02-05", "2014-02-06", "2014-04-07",
    "2014-05-01", "2014-05-02",
    "2014-06-02", "2014-09-08",
    "2014-10-01", "2014-10-02", "2014-10-03", "2014-10-06", "2014-10-07",

    "2015-01-01", "2015-01-02",
    "2015-02-18", "2015-02-19", "2015-02-20", "2015-02-23", "2015-02-24",
    "2015-04-06",
    "2015-05-01",
    "2015-06-22",
    "2015-09-03", "2015-09-04",
    "2015-10-01", "2015-10-02", "2015-10-05", "2015-10-06", "2015-10-07",

    "2016-01-01",
    "2016-02-08", "2016-02-09", "2016-02-10", "2016-02-11", "2016-02-12",
    "2016-04-04", "2016-05-02",
    "2016-06-09", "2016-06-10",
    "2016-09-15", "2016-09-16",
    "2016-10-03", "2016-10-04", "2016-10-05", "2016-10-06", "2016-10-07",

    "2017-01-02",
    "2017-01-27", "2017-01-30", "2017-01-31", "2017-02-01", "2017-02-02",
    "2017-04-03", "2017-04-04",
    "2017-05-01",
    "2017-05-29", "2017-05-30",
    "2017-10-02", "2017-10-03", "2017-10-04", "2017-10-05", "2017-10-06",

    "2018-01-01",
    "2018-02-15", "2018-02-16", "2018-02-19", "2018-02-20", "2018-02-21",
    "2018-04-05", "2018-04-06",
    "2018-04-30", "2018-05-01",
    "2018-06-18",
    "2018-09-24",
    "2018-10-01", "2018-10-02", "2018-10-03", "2018-10-04", "2018-10-05",
    "2018-12-31",

    "2019-01-01",
    "2019-02-04", "2019-02-05", "2019-02-06", "2019-02-07", "2019-02-08",
    "2019-04-05",
    "2019-05-01", "2019-05-02", "2019-05-03",
    "2019-06-07",
    "2019-09-13",
    "2019-10-01", "2019-10-02", "2019-10-03", "2019-10-04", "2019-10-07",

    "2020-01-01",
    "2020-01-24", "2020-01-27", "2020-01-28", "2020-01-29", "2020-01-30", "2020-01-31",
    "2020-04-06",
    "2020-05-01", "2020-05-04", "2020-05-05",
    "2020-06-25", "2020-06-26",
    "2020-10-01", "2020-10-02", "2020-10-05", "2020-10-06", "2020-10-07", "2020-10-08",

    "2021-01-01", "2021-01-02", "2021-01-03",
    "2021-02-11", "2021-02-12", "2021-02-13", "2021-02-14", "2021-02-15", "2021-02-16", "2021-02-17",
    "2021-04-03", "2021-04-04", "2021-04-05",
    "2021-05-01", "2021-05-02", "2021-05-03", "2021-05-04", "2021-05-05",
    "2021-06-12", "2021-06-13", "2021-06-14",
    "2021-09-19", "2021-09-20", "2021-09-21",
    "2021-10-01", "2021-10-02", "2021-10-03", "2021-10-04", "2021-10-05", "2021-10-06", "2021-10-07",

    "2022-01-01", "2022-01-02", "2022-01-03",
    "2022-01-31", "2022-02-01", "2022-02-02", "2022-02-03", "2022-02-04", "2022-02-05", "2022-02-06",
    "2022-04-03", "2022-04-04", "2022-04-05",
    "2022-04-30", "2022-05-01", "2022-05-02", "2022-05-03", "2022-05-04",
    "2022-06-03", "2022-06-04", "2022-06-05",
    "2022-09-10", "2022-09-11", "2022-09-12",
    "2022-10-01", "2022-10-02", "2022-10-03", "2022-10-04", "2022-10-05", "2022-10-06", "2022-10-07",

]


def trade_date_sse():
    launch_date = "1990-12-19"
    ran = pd.date_range(
        launch_date, datetime.datetime.now(), freq="B"
    ).strftime("%Y-%m-%d").tolist()
    return [i for i in ran if i not in trade_date_sse_exi]


trade_date_sse = trade_date_sse()

def QA_util_get_real_tradeday():

    """
    获取当前时间下真实的 tradeday

    如果当前是交易日的 早上 4 点 <9:00 开盘 -> 认定为上一个交易日
    """
    now =datetime.datetime.now()
    date =  str(now.date())
    tradeday =   QA_util_get_real_date(date)

    if now.hour<9:
        tradeday = QA_util_get_last_day(tradeday)

    return tradeday

def QA_util_format_date2str(cursor_date):
    """
    explanation:
        对输入日期进行格式化处理，返回格式为 "%Y-%m-%d" 格式字符串
        支持格式包括:
        1. str: "%Y%m%d" "%Y%m%d%H%M%S", "%Y%m%d %H:%M:%S",
                "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H%M%S"
        2. datetime.datetime
        3. pd.Timestamp
        4. int -> 自动在右边加 0 然后转换，譬如 '20190302093' --> "2019-03-02"
    params:
        * cursor_date->
            含义: 输入日期
            类型: str
            参数支持: []
    """
    if isinstance(cursor_date, datetime.datetime):
        cursor_date = str(cursor_date)[:10]
    elif isinstance(cursor_date, str):
        try:
            cursor_date = str(pd.Timestamp(cursor_date))[:10]
        except:
            raise ValueError('请输入正确的日期格式, 建议 "%Y-%m-%d"')
    elif isinstance(cursor_date, int):
        cursor_date = str(pd.Timestamp("{:<014d}".format(cursor_date)))[:10]
    else:
        raise ValueError('请输入正确的日期格式，建议 "%Y-%m-%d"')
    return cursor_date


def QA_util_get_next_period(datetime, frequence="1min"):
    """
    得到给定频率的下一个周期起始时间
    :param datetime: 类型 datetime eg: 2018-11-11 13:01:01
    :param frequence: 类型 str eg: '30min'
    :return: datetime eg: 2018-11-11 13:31:00
    """
    freq = {
        FREQUENCE.YEAR: "Y",
        FREQUENCE.QUARTER: "Q",
        FREQUENCE.MONTH: "M",
        FREQUENCE.WEEK: "W",
        FREQUENCE.DAY: "D",
        FREQUENCE.SIXTY_MIN: "60T",
        FREQUENCE.THIRTY_MIN: "30T",
        FREQUENCE.FIFTEEN_MIN: "15T",
        FREQUENCE.FIVE_MIN: "5T",
        FREQUENCE.ONE_MIN: "T",
    }
    return (pd.Period(datetime, freq=freq[frequence]) + 1).to_timestamp()


def QA_util_get_next_trade_date(
    cursor_date: Union[str, pd.Timestamp, datetime.datetime] = None, n: int = 1
) -> str:
    """
    得到后 n 个交易日 (如果当前日期为交易日，则不包含当前日期)
    e.g. 2020/12/25 为交易日，其后一个交易日为 2020/12/28; 2020/12/26 为非交易日，其后一个交易日为 2020/12/27

    Args:
        cursor_date(Union[str, pd.Timestamp, datetime.datetime], optional): 输入日期，默认为 None，即当天
        n(int, optional): 回溯交易日数目，默认为 1
    Returns:
        根据输入日期得到下 n 个交易日 (不包含当前交易日)

    """
    if not cursor_date:
        cursor_date = datetime.date.today().strftime("%Y-%m-%d")
    else:
        cursor_date = pd.Timestamp(cursor_date).strftime("%Y-%m-%d")
    if cursor_date in trade_date_sse:
        # 如果指定日期为交易日
        return trade_date_sse[trade_date_sse.index(cursor_date) + n]
    real_trade_date = QA_util_get_real_date(cursor_date, towards=-1)
    return trade_date_sse[trade_date_sse.index(real_trade_date) + n]


def QA_util_get_pre_trade_date(
    cursor_date: Union[str, pd.Timestamp, datetime.datetime] = None, n: int = 1
) -> str:
    """
    得到前 n 个交易日 (如果当前日期为交易日，则不包含当前日期)
    e.g. 2020/12/25 为交易日，其前一个交易日为 2020/12/24; 2020/12/26 为非交易日，其前一个交易日为 2020/12/25

    Args:
        cursor_date(Union[str, pd.Timestamp, datetime.datetime], optional): 输入日期，默认为 None，即当天
        n(int, optional): 回溯交易日数目，默认为 1
    Returns:
        str: 查询到的交易日
    """

    if not cursor_date:
        cursor_date = datetime.date.today().strftime("%Y-%m-%d")
    else:
        cursor_date = pd.Timestamp(cursor_date).strftime("%Y-%m-%d")
    if cursor_date in trade_date_sse:
        return trade_date_sse[trade_date_sse.index(cursor_date) - n]
    real_trade_date = QA_util_get_real_date(cursor_date, towards=1)
    return trade_date_sse[trade_date_sse.index(real_trade_date) - n]


def QA_util_if_trade(day):
    """
    得到前 n 个交易日 (不包含当前交易日)
    '日期是否交易'
    查询上面的 交易日 列表
    :param day: 类型 str eg: 2018-11-11
    :return: Boolean 类型
    """
    if day in trade_date_sse:
        return True
    else:
        return False


def QA_util_if_tradetime(
    _time=datetime.datetime.now(), market=MARKET_TYPE.STOCK_CN, code=None
):
    """
    explanation:
        时间是否交易

    params:
        * _time->
            含义: 指定时间
            类型: datetime
            参数支持: []
        * market->
            含义: 市场
            类型: int
            参数支持: [MARKET_TYPE.STOCK_CN]
        * code->
            含义: 代码
            类型: str
            参数支持: [None]
    """
    _time = datetime.datetime.strptime(str(_time)[0:19], "%Y-%m-%d %H:%M:%S")
    if market is MARKET_TYPE.STOCK_CN:
        if QA_util_if_trade(str(_time.date())[0:10]):
            if _time.hour in [10, 13, 14]:
                return True
            elif (
                _time.hour in [9] and _time.minute >= 15
            ):  # 修改成9:15 加入 9:15-9:30的盘前竞价时间
                return True
            elif _time.hour in [11] and _time.minute <= 30:
                return True
            else:
                return False
        else:
            return False
    elif market is MARKET_TYPE.FUTURE_CN:
        date_today = str(_time.date())
        date_yesterday = str((_time - datetime.timedelta(days=1)).date())

        is_today_open = QA_util_if_trade(date_today)
        is_yesterday_open = QA_util_if_trade(date_yesterday)

        # 考虑周六日的期货夜盘情况
        if is_today_open == False:  # 可能是周六或者周日
            if is_yesterday_open == False or (
                _time.hour > 2 or _time.hour == 2 and _time.minute > 30
            ):
                return False

        shortName = ""  # i , p
        for i in range(len(code)):
            ch = code[i]
            if ch.isdigit():  # ch >= 48 and ch <= 57:
                break
            shortName += code[i].upper()

        period = [[9, 0, 10, 15], [10, 30, 11, 30], [13, 30, 15, 0]]

        if shortName in ["IH", "IF", "IC"]:
            period = [[9, 30, 11, 30], [13, 0, 15, 0]]
        elif shortName in ["T", "TF"]:
            period = [[9, 15, 11, 30], [13, 0, 15, 15]]

        if 0 <= _time.weekday() <= 4:
            for i in range(len(period)):
                p = period[i]
                if (
                    _time.hour > p[0] or (_time.hour == p[0] and _time.minute >= p[1])
                ) and (
                    _time.hour < p[2] or (_time.hour == p[2] and _time.minute < p[3])
                ):
                    return True

        # 最新夜盘时间表_2019.03.29
        nperiod = [
            [["AU", "AG", "SC"], [21, 0, 2, 30]],
            [["CU", "AL", "ZN", "PB", "SN", "NI"], [21, 0, 1, 0]],
            [["RU", "RB", "HC", "BU", "FU", "SP"], [21, 0, 23, 0]],
            [
                [
                    "A",
                    "B",
                    "Y",
                    "M",
                    "JM",
                    "J",
                    "P",
                    "I",
                    "L",
                    "V",
                    "PP",
                    "EG",
                    "C",
                    "CS",
                ],
                [21, 0, 23, 0],
            ],
            [["SR", "CF", "RM", "MA", "TA", "ZC", "FG", "IO", "CY"], [21, 0, 23, 30]],
        ]

        for i in range(len(nperiod)):
            for j in range(len(nperiod[i][0])):
                if nperiod[i][0][j] == shortName:
                    p = nperiod[i][1]
                    condA = _time.hour > p[0] or (
                        _time.hour == p[0] and _time.minute >= p[1]
                    )
                    condB = _time.hour < p[2] or (
                        _time.hour == p[2] and _time.minute < p[3]
                    )
                    # in one day
                    if p[2] >= p[0]:
                        if (
                            (_time.weekday() >= 0 and _time.weekday() <= 4)
                            and condA
                            and condB
                        ):
                            return True
                    else:
                        if (
                            (_time.weekday() >= 0 and _time.weekday() <= 4) and condA
                        ) or (
                            (_time.weekday() >= 1 and _time.weekday() <= 5) and condB
                        ):
                            return True
                    return False
        return False


def QA_util_get_next_day(date, n=1):
    """
    explanation:
        得到下一个(n)交易日

    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
        * n->
            含义: 步长
            类型: int
            参数支持: [int]
    """
    date = str(date)[0:10]
    return QA_util_date_gap(date, n, "gt")


def QA_util_get_last_day(date, n=1):
    """
    explanation:
       得到上一个(n)交易日

    params:
        * date->
            含义: 日期
            类型: str
            参数支持: []
        * n->
            含义: 步长
            类型: int
            参数支持: [int]
    """
    date = str(date)[0:10]
    return QA_util_date_gap(date, n, "lt")


def QA_util_get_last_datetime(datetime, day=1):
    """
    explanation:
        获取几天前交易日的时间

    params:
        * datetime->
            含义: 指定时间
            类型: datetime
            参数支持: []
        * day->
            含义: 指定时间
            类型: int
            参数支持: []
    """

    date = str(datetime)[0:10]
    return "{} {}".format(QA_util_date_gap(date, day, "lt"), str(datetime)[11:])


def QA_util_get_next_datetime(datetime, day=1):
    date = str(datetime)[0:10]
    return "{} {}".format(QA_util_date_gap(date, day, "gt"), str(datetime)[11:])


def QA_util_get_real_date(date, trade_list=trade_date_sse, towards=-1):
    """
    explanation:
        获取真实的交易日期

    params:
        * date->
            含义: 日期
            类型: date
            参数支持: []
        * trade_list->
            含义: 交易列表
            类型: List
            参数支持: []
        * towards->
            含义: 方向， 1 -> 向前, -1 -> 向后
            类型: int
            参数支持: [1， -1]
    """
    date = str(date)[0:10]
    if towards == 1:
        if pd.Timestamp(date) >= pd.Timestamp(trade_list[-1]):
            return trade_list[-1]
        while date not in trade_list:
            date = str(
                datetime.datetime.strptime(str(date)[0:10], "%Y-%m-%d")
                + datetime.timedelta(days=1)
            )[0:10]
        else:
            return str(date)[0:10]
    elif towards == -1:
        if pd.Timestamp(date) <= pd.Timestamp(trade_list[0]):
            return trade_list[0]
        while date not in trade_list:
            date = str(
                datetime.datetime.strptime(str(date)[0:10], "%Y-%m-%d")
                - datetime.timedelta(days=1)
            )[0:10]
        else:
            return str(date)[0:10]


def QA_util_get_real_datelist(start, end):
    """
    explanation:
        取数据的真实区间，当start end中间没有交易日时返回None, None,
        同时返回的时候用 start,end=QA_util_get_real_datelist

    params:
        * start->
            含义: 开始日期
            类型: date
            参数支持: []
        * end->
            含义: 截至日期
            类型: date
            参数支持: []
    """
    real_start = QA_util_get_real_date(start, trade_date_sse, 1)
    real_end = QA_util_get_real_date(end, trade_date_sse, -1)
    if trade_date_sse.index(real_start) > trade_date_sse.index(real_end):
        return None, None
    else:
        return (real_start, real_end)


def QA_util_get_trade_range(start, end):
    """
    explanation:
       给出交易具体时间

    params:
        * start->
            含义: 开始日期
            类型: date
            参数支持: []
        * end->
            含义: 截至日期
            类型: date
            参数支持: []
    """
    start, end = QA_util_get_real_datelist(start, end)
    if start is not None:
        return trade_date_sse[
            trade_date_sse.index(start) : trade_date_sse.index(end) + 1 : 1
        ]
    else:
        return None


def QA_util_get_trade_gap(start, end):
    """
    explanation:
        返回start_day到end_day中间有多少个交易天 算首尾

    params:
        * start->
            含义: 开始日期
            类型: date
            参数支持: []
        * end->
            含义: 截至日期
            类型: date
            参数支持: []
    """
    start, end = QA_util_get_real_datelist(start, end)
    if start is not None:
        return trade_date_sse.index(end) + 1 - trade_date_sse.index(start)
    else:
        return 0


def QA_util_date_gap(date, gap, methods):
    """
    explanation:
        返回start_day到end_day中间有多少个交易天 算首尾

    params:
        * date->
            含义: 字符串起始日
            类型: str
            参数支持: []
        * gap->
            含义: 间隔多数个交易日
            类型: int
            参数支持: [int]
        * methods->
            含义: 方向
            类型: str
            参数支持: ["gt->大于", "gte->大于等于","小于->lt", "小于等于->lte", "等于->==="]
    """
    try:
        if methods in [">", "gt"]:
            return trade_date_sse[trade_date_sse.index(date) + gap]
        elif methods in [">=", "gte"]:
            return trade_date_sse[trade_date_sse.index(date) + gap - 1]
        elif methods in ["<", "lt"]:
            return trade_date_sse[trade_date_sse.index(date) - gap]
        elif methods in ["<=", "lte"]:
            return trade_date_sse[trade_date_sse.index(date) - gap + 1]
        elif methods in ["==", "=", "eq"]:
            return date

    except:
        return "wrong date"


def QA_util_get_trade_datetime(dt=datetime.datetime.now()):
    """
    explanation:
        获取交易的真实日期

    params:
        * dt->
            含义: 时间
            类型: datetime
            参数支持: []
    """

    # dt= datetime.datetime.now()

    if QA_util_if_trade(str(dt.date())) and dt.time() < datetime.time(15, 0, 0):
        return str(dt.date())
    else:
        return QA_util_get_real_date(str(dt.date()), trade_date_sse, 1)


def QA_util_get_order_datetime(dt):
    """
    explanation:
        获取委托的真实日期

    params:
        * dt->
            含义: 委托的时间
            类型: datetime
            参数支持: []

    """

    # dt= datetime.datetime.now()
    dt = datetime.datetime.strptime(str(dt)[0:19], "%Y-%m-%d %H:%M:%S")

    if QA_util_if_trade(str(dt.date())) and dt.time() < datetime.time(15, 0, 0):
        return str(dt)
    else:
        # print('before')
        # print(QA_util_date_gap(str(dt.date()),1,'lt'))
        return "{} {}".format(QA_util_date_gap(str(dt.date()), 1, "lt"), dt.time())


def QA_util_future_to_tradedatetime(real_datetime):
    """
    explanation:
        输入是真实交易时间,返回按期货交易所规定的时间* 适用于tb/文华/博弈的转换

    params:
        * real_datetime->
            含义: 真实交易时间
            类型: datetime
            参数支持: []
    """
    if len(str(real_datetime)) >= 19:
        dt = datetime.datetime.strptime(str(real_datetime)[0:19], "%Y-%m-%d %H:%M:%S")
        return (
            dt if dt.time() < datetime.time(21, 0) else QA_util_get_next_datetime(dt, 1)
        )
    elif len(str(real_datetime)) == 16:
        dt = datetime.datetime.strptime(str(real_datetime)[0:16], "%Y-%m-%d %H:%M")
        return (
            dt if dt.time() < datetime.time(21, 0) else QA_util_get_next_datetime(dt, 1)
        )


def QA_util_future_to_realdatetime(trade_datetime):
    """
    explanation:
       输入是交易所规定的时间,返回真实时间*适用于通达信的时间转换

    params:
        * trade_datetime->
            含义: 真实交易时间
            类型: datetime
            参数支持: []
    """
    if len(str(trade_datetime)) == 19:
        dt = datetime.datetime.strptime(str(trade_datetime)[0:19], "%Y-%m-%d %H:%M:%S")
        return (
            dt if dt.time() < datetime.time(21, 0) else QA_util_get_last_datetime(dt, 1)
        )
    elif len(str(trade_datetime)) == 16:
        dt = datetime.datetime.strptime(str(trade_datetime)[0:16], "%Y-%m-%d %H:%M")
        return (
            dt if dt.time() < datetime.time(21, 0) else QA_util_get_last_datetime(dt, 1)
        )
