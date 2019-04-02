# coding=utf-8
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

def QA_util_future_details(symbol_name):
    """
    输入期货合约名字,返回该合约的详情,方便清洗数据->比如把价格弄成PriceTick的整数倍
    """
    if type(symbol_name)!=str:
        print ("输入类型必须为字符串")
        return None
    else:
        #兼容直接输入具体合约名字的情况,比如输入RB1910
        for i in range(len(symbol_name)):
            if symbol_name[i].isdigit():
                symbol_name=symbol_name[:i]
                break
            symbol_name=symbol_name.upper()
        return future_details[symbol_name]

future_details={'AG': {'NameCN': '白银', 'VolumeMultiple': 15, 'PriceTick': 1.0},
 'AL': {'NameCN': '铝', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'AU': {'NameCN': '黄金', 'VolumeMultiple': 1000, 'PriceTick': 0.05},
 'BU': {'NameCN': '石油沥青', 'VolumeMultiple': 10, 'PriceTick': 2.0},
 'CU': {'NameCN': '铜', 'VolumeMultiple': 5, 'PriceTick': 10.0},
 'FU': {'NameCN': '燃料油', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'HC': {'NameCN': '热轧卷板', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'NI': {'NameCN': '镍', 'VolumeMultiple': 1, 'PriceTick': 10.0},
 'PB': {'NameCN': '铅', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'RB': {'NameCN': '螺纹钢', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'RU': {'NameCN': '天然橡胶', 'VolumeMultiple': 10, 'PriceTick': 5.0},
 'SN': {'NameCN': '锡', 'VolumeMultiple': 1, 'PriceTick': 10.0},
 'SP': {'NameCN': '漂针浆', 'VolumeMultiple': 10, 'PriceTick': 2.0},
 'WR': {'NameCN': '线材', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'ZN': {'NameCN': '锌', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'A': {'NameCN': '黄大豆', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'B': {'NameCN': '黄大豆', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'BB': {'NameCN': '细木工板', 'VolumeMultiple': 500, 'PriceTick': 0.05},
 'C': {'NameCN': '黄玉米', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'CS': {'NameCN': '玉米淀粉', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'EG': {'NameCN': '乙二醇', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'FB': {'NameCN': '中密度纤维板', 'VolumeMultiple': 500, 'PriceTick': 0.05},
 'I': {'NameCN': '铁矿石', 'VolumeMultiple': 100, 'PriceTick': 0.5},
 'J': {'NameCN': '冶金焦炭', 'VolumeMultiple': 100, 'PriceTick': 0.5},
 'JD': {'NameCN': '鲜鸡蛋', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'JM': {'NameCN': '焦煤', 'VolumeMultiple': 60, 'PriceTick': 0.5},
 'L': {'NameCN': '线型低密度聚乙烯', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'M': {'NameCN': '豆粕', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'P': {'NameCN': '棕榈油', 'VolumeMultiple': 10, 'PriceTick': 2.0},
 'PP': {'NameCN': '聚丙烯', 'VolumeMultiple': 5, 'PriceTick': 1.0},
 'V': {'NameCN': '聚氯乙烯', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'Y': {'NameCN': '豆油', 'VolumeMultiple': 10, 'PriceTick': 2.0},
 'AP': {'NameCN': '鲜苹果', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'CF': {'NameCN': '一号棉花', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'CY': {'NameCN': '棉纱', 'VolumeMultiple': 5, 'PriceTick': 5.0},
 'FG': {'NameCN': '玻璃', 'VolumeMultiple': 20, 'PriceTick': 1.0},
 'JR': {'NameCN': '粳稻', 'VolumeMultiple': 20, 'PriceTick': 1.0},
 'LR': {'NameCN': '晚籼稻', 'VolumeMultiple': 20, 'PriceTick': 1.0},
 'MA': {'NameCN': '甲醇MA', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'OI': {'NameCN': '菜籽油', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'PM': {'NameCN': '普通小麦', 'VolumeMultiple': 50, 'PriceTick': 1.0},
 'RI': {'NameCN': '早籼', 'VolumeMultiple': 20, 'PriceTick': 1.0},
 'RM': {'NameCN': '菜籽粕', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'RS': {'NameCN': '油菜籽', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'SF': {'NameCN': '硅铁', 'VolumeMultiple': 5, 'PriceTick': 2.0},
 'SM': {'NameCN': '锰硅', 'VolumeMultiple': 5, 'PriceTick': 2.0},
 'SR': {'NameCN': '白砂糖', 'VolumeMultiple': 10, 'PriceTick': 1.0},
 'TA': {'NameCN': '精对苯二甲酸', 'VolumeMultiple': 5, 'PriceTick': 2.0},
 'WH': {'NameCN': '优质强筋小麦', 'VolumeMultiple': 20, 'PriceTick': 1.0},
 'ZC': {'NameCN': '动力煤ZC', 'VolumeMultiple': 100, 'PriceTick': 0.2},
 'SC': {'NameCN': '原油', 'VolumeMultiple': 1000, 'PriceTick': 0.1}}

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
