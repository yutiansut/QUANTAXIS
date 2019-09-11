# coding=utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
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
import math

import numpy as np
import pandas as pd

from QUANTAXIS.QAUtil.QADate_trade import (
    QA_util_date_gap,
    QA_util_get_real_datelist,
    QA_util_get_trade_range,
    QA_util_if_trade,
    trade_date_sse
)


def QA_util_make_future_min_index(day, type_='1min'):
    """创建期货分钟线的index

    Arguments:
        day {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    if QA_util_if_trade(day) is True:
        return pd.date_range(
            str(day) + '21:00:00',
            str(day) + '',
            freq=type_,
            closed='right'
        ).append(
            pd.date_range(
                str(day) + ' 13:00:00',
                str(day) + ' 15:00:00',
                freq=type_,
                closed='right'
            )
        )
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_min_index(day, type_='1min'):
    """创建股票分钟线的index

    Arguments:
        day {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    if QA_util_if_trade(day) is True:
        return pd.date_range(
            str(day) + ' 09:30:00',
            str(day) + ' 11:30:00',
            freq=type_,
            closed='right'
        ).append(
            pd.date_range(
                str(day) + ' 13:00:00',
                str(day) + ' 15:00:00',
                freq=type_,
                closed='right'
            )
        )
    else:
        return pd.DataFrame(['No trade'])


def QA_util_make_hour_index(day, type_='1h'):
    """创建股票的小时线的index

    Arguments:
        day {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    if QA_util_if_trade(day) is True:
        return pd.date_range(
            str(day) + ' 09:30:00',
            str(day) + ' 11:30:00',
            freq=type_,
            closed='right'
        ).append(
            pd.date_range(
                str(day) + ' 13:00:00',
                str(day) + ' 15:00:00',
                freq=type_,
                closed='right'
            )
        )
    else:
        return pd.DataFrame(['No trade'])


def QA_util_time_gap(time, gap, methods, type_):
    '分钟线回测的时候的gap'
    min_len = int(240 / int(str(type_).split('min')[0]))
    day_gap = math.ceil(gap / min_len)

    if methods in ['>', 'gt']:
        data = pd.concat(
            [
                pd.DataFrame(QA_util_make_min_index(day,
                                                    type_))
                for day in trade_date_sse[trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ):trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ) + day_gap + 1]
            ]
        ).reset_index()
        return np.asarray(
            data[data[0] > time].head(gap)[0].apply(lambda x: str(x))
        ).tolist()[-1]
    elif methods in ['>=', 'gte']:
        data = pd.concat(
            [
                pd.DataFrame(QA_util_make_min_index(day,
                                                    type_))
                for day in trade_date_sse[trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ):trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ) + day_gap + 1]
            ]
        ).reset_index()

        return np.asarray(
            data[data[0] >= time].head(gap)[0].apply(lambda x: str(x))
        ).tolist()[-1]
    elif methods in ['<', 'lt']:
        data = pd.concat(
            [
                pd.DataFrame(QA_util_make_min_index(day,
                                                    type_))
                for day in trade_date_sse[trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ) - day_gap:trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ) + 1]
            ]
        ).reset_index()

        return np.asarray(
            data[data[0] < time].tail(gap)[0].apply(lambda x: str(x))
        ).tolist()[0]
    elif methods in ['<=', 'lte']:
        data = pd.concat(
            [
                pd.DataFrame(QA_util_make_min_index(day,
                                                    type_))
                for day in trade_date_sse[trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ) - day_gap:trade_date_sse.index(
                    str(
                        datetime.datetime.strptime(time,
                                                   '%Y-%m-%d %H:%M:%S').date()
                    )
                ) + 1]
            ]
        ).reset_index()

        return np.asarray(
            data[data[0] <= time].tail(gap)[0].apply(lambda x: str(x))
        ).tolist()[0]
    elif methods in ['==', '=', 'eq']:
        return time


"""
期货交易所交易时间：
 
(一)大连、上海、郑州交易所
 
集合竞价申报时间：08：55—08：59
集合竞价撮合时间：08：59—09：00
正常开盘交易时间：09：00－11：30 （小节休息10：15－10：30）
13：30－15：00

提示：客户下单时间为集合竞价时间和正常交易时间。在8：59—9：00竞价结束时间和交易所小节休息时间（上午10:15-10:30）下单，交易系统将不接受指令，并视之为废单。（时间以交易所时钟报时为准）

(二)上期所夜盘
 
集合竞价申报时间：20：55—20：59
集合竞价撮合时间：20：59—21：00
正常开盘交易时间：21：00－02：30 （黄金、白银、原油）
21：00－01：00 （铜、铝、锌、铅、镍、锡）
21：00－23：00（天然橡胶、螺纹钢、热轧卷板、石油沥青、燃料油、纸浆）

提示：法定节假日的前一日没有夜盘交易。

（三）大商所夜盘
19.03.29开始大商所夜盘交易品种和交易时间都有所更改
http://www.dce.com.cn/dalianshangpin/yw/fw/jystz/ywtz/6156940/index.html

集合竞价申报时间：20：55—20：59
集合竞价撮合时间：20：59—21：00
正常开盘交易时间：21：00—23：00 （豆一、豆二、豆油、豆粕、焦煤、焦炭、棕榈油、铁矿石、
                                线型低密度聚乙烯、聚氯乙烯、聚丙烯、乙二醇、玉米、玉米淀粉和玉米期权）

提示：法定节假日的前一日没有夜盘交易。
 
（四）郑商所夜盘
 
集合竞价申报时间：20：55—20：59
集合竞价撮合时间：20：59—21：00
正常开盘交易时间：21：00－23：30 （白糖、棉花、菜粕、甲醇、PTA、动力煤、玻璃、菜籽油、棉纱）

提示：法定节假日的前一日没有夜盘交易。
 
(五)中金所

股指:集合竞价时间：9：25—9：30
正常开盘交易时间：9：30-11：30（第一节）；13：00-15：00（第二节）

国债：
集合竞价时间：9：10-9：15
正常开盘交易时间：9：15-11：30（第一节）；13：00-15：15（第二节）
最后交易日交易时间：9：15-11：30


"""

if __name__ == '__main__':
    pass
