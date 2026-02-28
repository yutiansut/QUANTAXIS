# coding: utf-8
#
# Baostock 数据源适配
#
# 提供与 TDX 版本尽量兼容的接口：
# - QA_fetch_get_stock_day(code, start, end, if_fq='00', type_='pd')
# - QA_fetch_get_stock_list()
#

from __future__ import division

import time
import datetime
from typing import List

import baostock as bs
import pandas as pd

from QUANTAXIS.QAUtil import (
    QA_util_date_stamp,
    QA_util_time_stamp,
    QA_util_log_info,
)


def _bs_login() -> None:
    """登录 baostock，失败时重试几次。"""
    last_err = None
    for i in range(3):
        lg = bs.login()
        if lg.error_code == "0":
            return
        last_err = lg.error_msg
        QA_util_log_info(
            f"baostock login failed: {lg.error_msg}, retry {i + 1}"
        )
        time.sleep(1)
    raise RuntimeError(f"baostock login failed: {last_err}")


def _bs_logout() -> None:
    try:
        bs.logout()
    except Exception:
        pass


def _baostock_code(code: str) -> str:
    """将 000001 转为 baostock 代码 sz.000001 / sh.600000。"""
    code = str(code)
    if code.startswith("6"):
        return f"sh.{code}"
    return f"sz.{code}"


def _map_if_fq_to_adjustflag(if_fq: str) -> str:
    """
    QUANTAXIS if_fq -> baostock adjustflag

    '00' / 'bfq' : 不复权 -> '3'
    '01' / 'qfq' : 前复权 -> '2'
    '02' / 'hfq' : 后复权 -> '1'
    """
    if str(if_fq) in ["qfq", "01"]:
        return "2"
    if str(if_fq) in ["hfq", "02"]:
        return "1"
    return "3"


def QA_fetch_get_stock_day(
    code: str,
    start: str,
    end: str,
    if_fq: str = "00",
    type_: str = "pd",
):
    """
    使用 baostock 获取股票日线数据。

    :param code: 股票代码，如 '000001'
    :param start: 'YYYY-MM-DD'
    :param end:   'YYYY-MM-DD'
    :param if_fq: '00' 不复权, '01' 前复权, '02' 后复权
    :param type_: 'pd' 返回 DataFrame, 'json' 返回 list[dict]
    """
    _bs_login()
    try:
        bs_code = _baostock_code(code)
        adjustflag = _map_if_fq_to_adjustflag(if_fq)

        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,code,open,high,low,close,volume,amount",
            start_date=start,
            end_date=end,
            frequency="d",
            adjustflag=adjustflag,
        )
        if rs.error_code != "0":
            raise RuntimeError(f"baostock query error: {rs.error_msg}")

        data_list: List[list] = []
        while rs.next():
            data_list.append(rs.get_row_data())

        if not data_list:
            return pd.DataFrame() if type_ in ["pd", "pandas"] else []

        df = pd.DataFrame(data_list, columns=rs.fields)

        # 类型转换
        for col in ["open", "high", "low", "close", "volume", "amount"]:
            df[col] = df[col].astype(float)

        # 补充 QUANTAXIS 常用字段
        df["code"] = df["code"].apply(lambda x: x.split(".")[-1])
        df["date"] = df["date"].astype(str)
        df["date_stamp"] = df["date"].apply(QA_util_date_stamp)
        df["time_stamp"] = df["date"].apply(
            lambda x: QA_util_time_stamp(f"{x} 00:00:00")
        )

        df = df.set_index("date", drop=False)

        if type_ in ["pd", "pandas", "P"]:
            return df
        return df.to_dict("records")
    finally:
        _bs_logout()


def QA_fetch_get_stock_list():
    """
    使用 baostock 获取股票列表，返回格式尽量与 TDX 版兼容：

    columns: code, volunit, decimal_point, name, pre_close, sse
    index: (code, sse)
    """
    _bs_login()
    try:
        rs = bs.query_stock_basic()
        if rs.error_code != "0":
            raise RuntimeError(f"baostock stock_basic error: {rs.error_msg}")

        data_list: List[list] = []
        while rs.next():
            data_list.append(rs.get_row_data())

        if not data_list:
            return pd.DataFrame()

        df = pd.DataFrame(data_list, columns=rs.fields)
        # baostock: code 形如 sh.600000 / sz.000001
        df["sse"] = df["code"].apply(lambda x: x.split(".")[0])
        df["code"] = df["code"].apply(lambda x: x.split(".")[-1])

        df["name"] = df["code_name"]
        df["volunit"] = 100
        df["decimal_point"] = 2
        df["pre_close"] = 0.0

        df = df[["code", "volunit", "decimal_point", "name", "pre_close", "sse"]]
        df = df.drop_duplicates(["code", "sse"])
        df = df.set_index(["code", "sse"], drop=False)

        return df
    finally:
        _bs_logout()

