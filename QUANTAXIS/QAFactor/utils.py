"""
辅助函数
"""
import datetime
import math
import re
import warnings
from functools import partial
from typing import List, Tuple, Union

import jqdatasdk
import numpy as np
import pandas as pd
import statsmodels.api as sm

from QUANTAXIS.QAFactor.parameters import (
    DAYS_PER_WEEK,
    DAYS_PER_MONTH,
    DAYS_PER_QUARTER,
    DAYS_PER_YEAR,
    FREQUENCE_TYPE
)


def get_frequence(frequence: str = None):
    """
    对于输入的 frequence 进行格式化，以符合 pandas 的 resample 需求

    参数
    ---
    :param frequence: 频率，格式类似 'min', '1D', '10D'
    """
    if frequence is not None:
        pattern = re.compile(r"\d+")
        interval = pattern.findall(frequence)
        if not interval:
            interval = "1"
            if frequence.lower() != "min":
                frequence = frequence[0]
            assert frequence.lower() in FREQUENCE_TYPE
            frequence = interval + frequence.lower()
        else:
            interval = interval[0]
            if frequence.replace(interval, "").lower() != "min":
                frequence = frequence.replace(interval, "").lower()[0]
            assert frequence.replace(interval, "").lower() in FREQUENCE_TYPE
            frequence = interval + frequence.replace(interval, "").lower()
    else:
        warnings.warn("没有指定频率信息，设置为日线")
        frequence = "1D"
    return frequence


def QA_fmt_quarter(cursor_date: datetime.datetime):
    """
    将输入的 cursor_date 格式化为财报对应日期
    :param cursor_date: 指定日期
    :return:
    """
    if cursor_date.month in [3, 12]:
        return pd.Timestamp(cursor_date.year, cursor_date.month, 31)
    else:
        return pd.Timestamp(cursor_date.year, cursor_date.month, 30)


def QA_fmt_code_list(
        code_list: Union[str,
                         Tuple[str],
                         List[str]],
        style: str = None
):
    """
    为了适应不同行情源股票代码，加入对股票代码格式化的操作, 目前支持 “聚宽” “掘金” “万得” “天软”
    股票代码格式格式化

    参数
    ---
    :param code_list: 股票代码或列表
    :param style: 行情源
    """

    def _fmt_code(code: str, style: str):
        code = pattern.findall(code)[0]
        if style in ["jq", "joinquant", "聚宽"]:
            return code + ".XSHG" if code[0] == "6" else code + ".XSHE"
        if style in ["wd", "windcode", "万得"]:
            return code + ".SH" if code[0] == "6" else code + ".SZ"
        if style in ["gm", "goldminer", "掘金"]:
            return "SHSE." + code if code[0] == "6" else "SZSE." + code
        if style in ["ss", "skysoft", "天软"]:
            return "SH" + code if code[0] == "6" else "SZ" + code
        else:
            return code

    pattern = re.compile(r"\d+")
    if isinstance(code_list, str):
        return [_fmt_code(code_list, style)]
    else:
        fmt_code = partial(_fmt_code, style=style)
        return list(map(fmt_code, code_list))


def get_period(period: str):
    """
    根据频率获取 pandas 的 time interval

    参数
    ---
    :param period: 指定的时间间隔，'1H1min', '2D3H', '1Q3min' 等
    """
    origin_period = period
    assert isinstance(period, str)
    pattern = re.compile(r"\d+")
    freqs = pattern.split(period)
    flag = np.all(
        [
            freq.lower() in ["",
                             "y",
                             "w",
                             "q",
                             "m",
                             "d",
                             "h",
                             "min"] for freq in freqs
        ]
    )
    total_interval = ""
    if not flag:
        raise ValueError("检查 period 格式")
    if "min" in period:
        min_interval = re.findall("\d+min", period.lower())[0]
        period = period.lower().replace(min_interval, "")
    hour_interval = re.findall("\d+h", period)
    day_interval = re.findall("\d+d", period)
    week_interval = re.findall("\d+w", period)
    month_interval = re.findall("\d+m", period)
    quarter_interval = re.findall("\d+q", period)
    year_interval = re.findall("\d+y", period)
    day_count = 0
    hour_count = 0
    if day_interval:
        day_count += int(re.findall("\d+", day_interval[0])[0])
    if week_interval:
        day_count += DAYS_PER_WEEK * \
            int(re.findall("\d+", week_interval[0])[0])
    if month_interval:
        day_count += DAYS_PER_MONTH * int(
            re.findall("\d+",
                       month_interval[0])[0]
        )
    if quarter_interval:
        day_count += DAYS_PER_QUARTER * int(
            re.findall("\d+",
                       quarter_interval[0])[0]
        )
    if year_interval:
        day_count += DAYS_PER_YEAR * \
            int(re.findall("\d+", year_interval[0])[0])
    day_interval = str(day_count) + "d"
    if "min" in origin_period:
        return "".join([day_interval] + hour_interval) + min_interval
    else:
        return "".join([day_interval] + hour_interval)


def get_forward_returns_columns(columns: pd.Index) -> pd.Index:
    """
    从输入的列索引中取出相应的远期收益的列

    参数
    ---
    :param columns: 列索引

    返回
    ---
    :return: 相应远期收益对应列
    """
    syntax = re.compile("^period_\d+")
    return columns[columns.astype("str").str.contains(syntax, regex=True)]


def rate_of_return(period_ret: pd.Series, base_period: str) -> pd.Series:
    """
    跨期收益转换
    假设 factor_data 对应的收益率列名为 period_30D, period_150D, period_450D, 如果以
    period_30D 作为基准，假设 period_150D 的收益率为 r, 那么 period_150D 在收益率稳定
    的情况下，理论上， period_30 从 period_150D 换算下来的收益率应该为 (1+r)^{30/150} - 1

    参数
    ---
    :param period_ret: 包含远期收益的数据，名称应该包括相应周期
    :param base_period: 转换中使用的基准周期，譬如 ('1 days', '1D', '30m', '3h', '1D1h', etc)
    """
    period_len = get_period(period_ret.name.replace("period_", ""))
    base_period = get_period(base_period.replace("period_", ""))
    # pattern = re.compile(r"\d+")
    # interval = pattern.findall(period_len)[0]
    # base_interval = pattern.findall(base_period)[0]
    # if (period_len.replace(interval,
    #                        "") != "min") or (period_len.replace(interval,
    #                                                             "") != "d"):
    #     if period_len.replace(interval, "") == "m":
    #         period_len = int(interval) * pd.Timedelta(days=DAYS_PER_MONTH)
    #         base_period = int(base_interval) * pd.Timedelta(days=DAYS_PER_MONTH)
    #     elif period_len.replace(interval, "") == "q":
    #         period_len = int(interval) * pd.Timedelta(days=DAYS_PER_QUARTER)
    #         base_period = int(base_interval) * pd.Timedelta(
    #             days=DAYS_PER_QUARTER
    #         )
    #     elif period_len.replace(interval, "") == "y":
    #         period_len = int(interval) * pd.Timedelta(days=DAYS_PER_YEAR)
    #         base_period = int(base_interval) * pd.Timedelta(days=DAYS_PER_YEAR)
    conversion_factor = pd.Timedelta(base_period) / pd.Timedelta(period_len)
    return period_ret.add(1).pow(conversion_factor).sub(1.0)


def std_conversion(period_std: pd.Series, base_period: str) -> pd.Series:
    """
    跨期收益标准差转换

    参数
    ---
    :param period_std: 远期收益标准差, 名称包含相应周期
    :param base_period: 转换使用的基准周期

    返回
    ---
    转换后的收益标准差
    """
    period_len = get_period(period_std.name.replace("period_", ""))
    base_period = get_period(base_period.replace("period_", ""))
    conversion_factor = pd.Timedelta(period_len) / pd.Timedelta(base_period)
    return period_std / np.sqrt(conversion_factor)


def add_custom_calendar_timedelta(input, timedelta):
    """
    """
    days = timedelta.components.days
    offset = timedelta - pd.Timedelta(days=days)
    return input + days + offset


def diff_custom_calendar_timedeltas(start, end, freq):
    raise NotImplementedError


"""
    if not isinstance(freq, (Day, BusinessDay, CustomBusinessDay)):
        raise ValueError("freq must be Day, BusinessDay or CustomBusinessDay")

    weekmask = getattr(freq, "weekmask", None)
    holidays = getattr(freq, "holidays", None)

    if weekmask is None and holidays is None:
        if isinstance(freq, Day):
            weekmask = "Mon Tue Wed Thu Fri Sat Sun"
            holidays = []
        elif isinstance(freq, BusinessDay):
            weekmask = "Mon Tue Wed Thu Fri"
            holidays = []

    if weekmask is not None and holidays is not None:
        actual_days = np.busday_count(
            np.array(start).astype("datetime64[D]"),
            np.array(end).astype("datetime64[D]"),
            weekmask,
            holidays,
        )
    else:
        actual_days = pd.date_range(start, end, freq=freq).shape[0] - 1
        if not freq.onOffset(start):
            actual_days -= 1

    timediff = end - start
    delta_days = timediff.components.days - actual_days
    return timediff - pd.Timedelta(days=delta_days)
"""
