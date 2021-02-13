# /usr/bin/env python3
"""
网络查询接口：
1. 个股查询
    - QA_fetch_get_individual_financial: 查询个股指定时间段指定财务报表指定报告类型数据
2. 截面查询
    - QA_fetch_get_crosssection_financial: 查询指定报告期指定报表指定报告类型数据
本地查询接口：
1. 截面查询
    - QA_fetch_crosssection_financial
2. 高级查询
    - QA_fetch_financial_adv
"""

import datetime
import time
from typing import List, Tuple, Union

import pandas as pd
import pymongo
import tushare as ts

from QUANTAXIS.QAFactor.utils import QA_fmt_code, QA_fmt_code_list
from QUANTAXIS.QAFetch.QAQuery_Advance import QA_fetch_stock_list
from QUANTAXIS.QAFetch.QATushare import get_pro
from QUANTAXIS.QAUtil import (DATABASE, QASETTING, QA_util_date_int2str,
                              QA_util_date_stamp, QA_util_get_pre_trade_date,
                              QA_util_get_real_date, QA_util_log_info,
                              QA_util_to_json_from_pandas)

REPORT_DATE_TAILS = ["0331", "0630", "0930", "1231"]
SHEET_TYPE = ["income", "balancesheet", "cashflow"]
REPORT_TYPE = ['1', '2', '3', '4', '5', '11']


def QA_fetch_get_individual_financial(
        code: str,
        start: Union[str, datetime.datetime, pd.Timestamp] = None,
        end: Union[str, datetime.datetime, pd.Timestamp] = None,
        report_date: Union[str, datetime.datetime] = None,
        sheet_type: str = "income",
        report_type: Union[int, str] = 1,
        fields: Union[str, Tuple, List] = None,
        wait_seconds: int = 61,
        max_trial: int = 3) -> pd.DataFrame:
    """个股财务报表网络查询接口，注意，这里的 start 与 end 是针对 report_date 进行范围查询

    Args:
        code (str): 股票代码
        start (Union[str, datetime.datetime, pd.Timestamp], optional): 查询起始时间，默认为 None
        end (Union[str, datetime.datetime, pd.Timestamp], optional): 查询结束时间，默认为 None
        report_date (Union[str, datetime.datetime], optional): 报告期. 默认为 None，如果使用了 report_date, 则 start 与 end 参数不再起作用
        sheet_type (str, optional): 报表类型，默认为 "income" 类型
            (利润表 "income"|
            资产负债表 "balancesheet"|
            现金流量表 "cashflow"|
            业绩预告 "forecast"|
            业绩快报 "express")
        report_type (Union[int, str], optional): 报告类型. 默认为 1。
            (1	合并报表	上市公司最新报表（默认）|
            2	单季合并	单一季度的合并报表 |
            3	调整单季合并表	调整后的单季合并报表（如果有） |
            4	调整合并报表	本年度公布上年同期的财务报表数据，报告期为上年度 |
            5	调整前合并报表	数据发生变更，将原数据进行保留，即调整前的原数据 |
            6	母公司报表	该公司母公司的财务报表数据 |
            7	母公司单季表	母公司的单季度表 |
            8	母公司调整单季表	母公司调整后的单季表 |
            9	母公司调整表	该公司母公司的本年度公布上年同期的财务报表数据 |
            10 母公司调整前报表	母公司调整之前的原始财务报表数据 |
            11 调整前合并报表	调整之前合并报表原数据 |
            12 母公司调整前报表	母公司报表发生变更前保留的原数据)
        fields (Union[str, Tuple, List], optional): 指定数据范围，如果设置为 None，则返回所有数据. 默认为 None.
        wait_seconds (int, optional): 等待重试时间. 默认为 61 秒.
        max_trial (int, optional): 最大重试次数. 默认为 3.

    Returns:
        pd.DataFrame: 返回指定个股时间范围内指定类型的报表数据
    """
    def _get_individual_financial(code, report_date, report_type, sheet_type, fields, wait_seconds, trial_count):
        nonlocal pro, max_trial
        if trial_count >= max_trial:
            raise ValueError("[ERROR]\tEXCEED MAX TRIAL!")
        try:
            if not fields:
                df = eval(
                    f"pro.{sheet_type}(ts_code='{code}', period='{report_date}', report_type={report_type})")
            else:
                df = eval(
                    f"pro.{sheet_type}(ts_code='{code}', period='{report_date}', report_type={report_type}, fields={fields})")
            return df.rename(columns={"ts_code": "code", "end_date": "report_date"})
        except Exception as e:
            print(e)
            time.sleep(wait_seconds)
            _get_individual_financial(
                code, report_date, report_type, sheet_type, fields, wait_seconds, trial_count+1)

    pro = get_pro()
    report_type = int(report_type)
    if (not start) and (not end) and (not report_date):
        raise ValueError(
            "[QRY_DATES ERROR]\tparam 'start', 'end' and 'report_date' should not be none at the same time!")
    if isinstance(fields, str):
        fields = sorted(list(set([fields, "ts_code", "end_date",
                                  "ann_date", "f_ann_date", "report_type", "update_flag"])))
    if report_date:
        report_date = pd.Timestamp(report_date)
        year = report_date.year
        report_date_lists = [
            pd.Timestamp(str(year) + report_date_tail) for report_date_tail in REPORT_DATE_TAILS]
        if report_date not in report_date_lists:
            raise ValueError("[REPORT_DATE ERROR]")
        if sheet_type not in ["income", "balancesheet", "cashflow", "forecast", "express"]:
            raise ValueError("[SHEET_TYPE ERROR]")
        if report_type not in range(1, 13):
            raise ValueError("[REPORT_TYPE ERROR]")
        report_dates = [report_date]
    else:
        start = pd.Timestamp(start)
        start_year = start.year
        end = pd.Timestamp(end)
        end_year = end.year
        origin_year_ranges = pd.date_range(
            str(start_year), str(end_year+1), freq='Y').map(str).str.slice(0, 4).tolist()
        origin_report_ranges = pd.Series([
            pd.Timestamp(year + report_date_tail) for year in origin_year_ranges for report_date_tail in REPORT_DATE_TAILS])
        report_dates = origin_report_ranges.loc[(
            origin_report_ranges >= start) & (origin_report_ranges <= end)]
    df = pd.DataFrame()
    for report_date in report_dates:
        df = df.append(_get_individual_financial(
            code=QA_fmt_code(code, "ts"),
            report_date=report_date.strftime("%Y%m%d"),
            report_type=report_type,
            sheet_type=sheet_type,
            fields=fields,
            wait_seconds=wait_seconds,
            trial_count=0))
    df.code = QA_fmt_code_list(df.code)
    return df.reset_index(drop=True)


def QA_fetch_get_crosssection_financial(
        report_date: Union[str, datetime.datetime, pd.Timestamp],
        report_type: Union[int, str] = 1,
        sheet_type: str = "income",
        fields: Union[str, Tuple, List] = None,
        wait_seconds: int = 61,
        max_trial: int = 3) -> pd.DataFrame:
    """截面财务报表网络查询接口

    Args:
        report_date (Union[str, datetime.datetime, pd.Timestamp]): 报告期
        report_type (Union[int, str], optional): 报告类型，默认值为 1.
            (1	合并报表	上市公司最新报表（默认）|
             2	单季合并	单一季度的合并报表 |
             3	调整单季合并表	调整后的单季合并报表（如果有） |
             4	调整合并报表	本年度公布上年同期的财务报表数据，报告期为上年度 |
             5	调整前合并报表	数据发生变更，将原数据进行保留，即调整前的原数据 |
             6	母公司报表	该公司母公司的财务报表数据 |
             7	母公司单季表	母公司的单季度表 |
             8	母公司调整单季表	母公司调整后的单季表 |
             9	母公司调整表	该公司母公司的本年度公布上年同期的财务报表数据 |
             10 母公司调整前报表	母公司调整之前的原始财务报表数据 |
             11 调整前合并报表	调整之前合并报表原数据 |
             12 母公司调整前报表	母公司报表发生变更前保留的原数据)

        sheet_type (str, optional): 报表类型，默认为 "income".
            (利润表 "income"|
             资产负债表 "balancesheet"|
             现金流量表 "cashflow"|
             业绩预告 "forecast"|
             业绩快报 "express")
        fields (Union[str, List], optional): 数据范围，默认为 None，返回所有数据.
        wait_seconds (int, optional): 查询超时时间, 默认为 61.
        max_trial (int, optional): 查询最大尝试次数, 默认为 3.

    Returns:
        pd.DataFrame: 指定报告期的指定财务报表数据
    """
    def _get_crosssection_financial(report_date, report_type, sheet_type, fields, wait_seconds, trial_count):
        nonlocal pro, max_trial
        if trial_count >= max_trial:
            raise ValueError("[ERROR]\tEXCEED MAX TRIAL!")
        try:
            if not fields:
                print(
                    f"pro.{sheet_type}_vip(period='{report_date}', report_type={report_type})")
                df = eval(
                    f"pro.{sheet_type}_vip(period='{report_date}', report_type={report_type})")
            else:
                df = eval(
                    f"pro.{sheet_type}_vip(period='{report_date}', report_type={report_type}, fields={fields})")
            if df.empty:
                return df
            df.ts_code = QA_fmt_code_list(df.ts_code)
            return df.rename(columns={"ts_code": "code", "end_date": "report_date"}).sort_values(by=['ann_date', 'f_ann_date'])
        except Exception as e:
            print(e)
            time.sleep(wait_seconds)
            _get_crosssection_financial(
                report_date, report_type, sheet_type, fields, wait_seconds, trial_count + 1)

    # Tushare 账号配置
    pro = get_pro()

    # 设置标准报告期格式
    report_date = pd.Timestamp(report_date)
    report_type = int(report_type)
    year = report_date.year
    std_report_dates = [
        str(year) + report_date_tail for report_date_tail in REPORT_DATE_TAILS]

    # Tushare 接口支持的日期格式
    if report_date.strftime("%Y%m%d") not in std_report_dates:
        raise ValueError("[REPORT_DATE ERROR]")

    # fields 格式化处理
    if isinstance(fields, str):
        fields = sorted(list(set([fields, "ts_code", "end_date",
                                  "ann_date", "f_ann_date", "report_type", "update_flag"])))

    # 目前支持利润表，资产负债表和现金流量表
    if sheet_type not in SHEET_TYPE:
        raise ValueError("[SHEET_TYPE ERROR]")
    if report_type not in range(1, 13):
        raise ValueError("[REPORT_TYTPE ERROR]")

    return _get_crosssection_financial(
        report_date=report_date.strftime("%Y%m%d"),
        report_type=report_type,
        sheet_type=sheet_type,
        fields=fields,
        wait_seconds=wait_seconds,
        trial_count=0)


# FIXME: Add Fetch Get Method of Daily Basic
def QA_fetch_get_daily_basic(
        code: Union[str, List, Tuple] = None,
        trade_date: Union[str, pd.Timestamp, datetime.datetime] = None,
        fields: Union[str, List, Tuple] = None,
        wait_seconds: int = 61,
        max_trial: int = 3
) -> pd.DataFrame:
    """
    从网络获取市场指定交易日重要基本面指标，用于选股分析和报表展示

    Args:
        code(Union[str, List, Tuple], optional): 指定股票代码，默认为 None，即对应交易日的全市场股票
        trade_date(Union[str, pd.Timestamp, datetime.datetime], optional): 指定交易日期, 默认为 None, 即距离当前
            日期最近的交易日
        fields(Union[str, List, Tuple], optional): 默认为 None，如果指定为某一单个 str，默认返回 DataFrame 包括
            交易日等附加信息
        wait_seconds (int, optional): 查询超时时间, 默认为 61.
        max_trial (int, optional): 查询最大尝试次数, 默认为 3.

    Returns:
        pd.DataFrame: 指定交易日指定范围指定标的的每日基本面指标信息
    """
    def _fetch_get_daily_basic(trade_date, fields, trial_count):
        nonlocal pro, max_trial
        try:
            if trial_count >= max_trial:
                raise ValueError("[ERROR]\tEXCEED MAX TRIAL!")
            if not trade_date:
                trade_date = QA_util_get_pre_trade_date(
                    datetime.date.today(), 1).replace("-", "")
            else:
                trade_date = pd.Timestamp(trade_date).strftime("%Y%m%d")
            if not fields:
                qry = f"pro.daily_basic(trade_date={trade_date})"
            else:
                if isinstance(fields, str):
                    fields = list(set([fields] + ["ts_code", "trade_date"]))
                fields = ",".join(fields)
                qry = "pro.daily_basic(trade_date={trade_date}, fields={fields})"
            df = eval(qry)
            if df is None:
                raise ValueError("[ERROR]")
            return df
        except:
            time.sleep(61)
            _fetch_get_daily_basic(
                trade_date, fields, trial_count+1
            )

    pro = get_pro()
    df = _fetch_get_daily_basic(
        trade_date=trade_date, fields=fields, trial_count=0)
    if df.empty:
        return df
    else:
        df = df.rename(columns={"ts_code": "code"})
        df.code = QA_fmt_code_list(df.code)
        df = df.set_index("code")
    if not code:
        return df
    if isinstance(code, str):
        code = (code,)
    # exclude code which not in rtn dataframe
    filter_idx = df.index.intersection(code)
    return df.loc[filter_idx]


def QA_fetch_crosssection_financial(
        report_date: Union[str, datetime.datetime, pd.Timestamp],
        report_type: Union[int, str] = 1,
        sheet_type: str = "income",
        fields: Union[str, Tuple, List] = None) -> pd.DataFrame:
    """本地查询截面财务数据接口

    Args:
        report_date (Union[str, datetime.datetime, pd.Timestamp]): 报告期
        report_type (Union[int, str], optional): 报告类型，默认为 1.
            (1	合并报表	上市公司最新报表（默认）|
             2	单季合并	单一季度的合并报表 |
             3	调整单季合并表	调整后的单季合并报表（如果有） |
             4	调整合并报表	本年度公布上年同期的财务报表数据，报告期为上年度 |
             5	调整前合并报表	数据发生变更，将原数据进行保留，即调整前的原数据 |
             11 调整前合并报表	调整之前合并报表原数据)

        sheet_type (str, optional): 报表类型，默认为 "income".
        fields (Union[str, Tuple, List], optional): 子段，默认为 None，返回所有字段.

    Returns:
        pd.DataFrame: 指定报告期指定报表数据
    """
    if isinstance(fields, str):
        fields = sorted(list(set([fields, "code", "report_date",
                                  "ann_date", "f_ann_date", "report_type", "update_flag"])))
    coll = eval(f"DATABASE.{sheet_type}")
    report_date = pd.Timestamp(report_date).strftime("%Y%m%d")
    cursor = coll.find(
        {
            "report_date": report_date,
            "report_type": str(report_type)
        }
    )
    res = pd.DataFrame([item for item in cursor])
    if res.empty:
        return pd.DataFrame()
    res.report_date = pd.to_datetime(res.report_date, utc=False)
    if not fields:
        return res.drop(columns="_id")
    return res.drop(columns="_id")[fields]


def QA_fetch_financial_adv(
        code: Union[str, Tuple, List] = None,
        start: Union[str, datetime.datetime, pd.Timestamp] = None,
        end: Union[str, datetime.datetime, pd.Timestamp] = None,
        report_date: Union[str, datetime.datetime, pd.Timestamp] = None,
        report_type: Union[int, str] = None,
        sheet_type: str = "income",
        fields: Union[str, Tuple, List] = None) -> pd.DataFrame:
    """本地获取指定股票或者指定股票列表，指定时间范围或者报告期，指定报告类型的指定财务报表数据

    Args:
        code (Union[str, Tuple, List], optional): 指定股票代码或列表，默认为 None, 全市场股票
        start (Union[str, datetime.datetime, pd.Timestamp], optional): 起始时间
        end (Union[str, datetime.datetime, pd.Timestamp], optional): 结束时间
        report_date (Union[str, datetime.datetime, pd.Timestamp], optional): 报告期
        report_type (Union[int, str], optional): 报告类型，默认为 1.
            (1	合并报表	上市公司最新报表（默认）|
             2	单季合并	单一季度的合并报表 |
             3	调整单季合并表	调整后的单季合并报表（如果有） |
             4	调整合并报表	本年度公布上年同期的财务报表数据，报告期为上年度 |
             5	调整前合并报表	数据发生变更，将原数据进行保留，即调整前的原数据 |
             11 调整前合并报表	调整之前合并报表原数据)
        sheet_type (str, optional): 报表类型，默认为 "income".
        fields (List, optional): 字段，默认为 None，返回所有字段.

    Returns:
        pd.DataFrame: 指定条件的本地报表数据
    """
    if (not start) and (not end) and (not report_date):
        raise ValueError(
            "[DATE ERROR]\t 'start', 'end' 与 'report_date' 不能同时为 None")
    if isinstance(code, str):
        code = (code,)
    if not report_type:
        report_type = ("1", "2", "4", "5", "11")
    if isinstance(report_type, int) or isinstance(report_type, str):
        report_type = (str(report_type), )
    else:
        report_type = list(map(str, report_type))

    coll = eval(f"DATABASE.{sheet_type}")
    qry = {}
    if not report_date:
        if not end:
            end = datetime.date.today()
        start = pd.Timestamp(start)
        end = pd.Timestamp(end)
        start_date_stamp = QA_util_date_stamp(start)
        end_date_stamp = QA_util_date_stamp(end)
        if not code:
            qry = {
                "f_ann_date_stamp": {
                    "$gte": start_date_stamp,
                    "$lte": end_date_stamp
                },
                "report_type": {
                    "$in": report_type
                }
            }
        else:
            qry = {
                "code": {
                    "$in": code
                },
                "f_ann_date_stamp": {
                    "$gte": start_date_stamp,
                    "$lte": end_date_stamp
                },
                "report_type": {
                    "$in": report_type
                }
            }
    else:
        report_date_stamp = QA_util_date_stamp(report_date)
        if not code:
            qry = {
                "report_date_stamp": report_date_stamp,
                "report_type": {
                    "$in": report_type
                }
            }
        else:
            qry = {
                "code": {
                    "$in": code
                },
                "report_date_stamp": report_date_stamp,
                "report_type": {
                    "$in": report_type
                }
            }
    if isinstance(fields, str):
        fields = list(
            set([fields, "code", "ann_date", "report_date", "f_ann_date"]))
    elif fields:
        fields = list(
            set(list(fields) + ["code", "ann_date", "report_date", "f_ann_date"]))

    cursor = coll.find(qry, batch_size=10000).sort([
        ("report_date_stamp", pymongo.ASCENDING),
        ("f_ann_date_stamp", pymongo.ASCENDING)])
    if fields:
        df = pd.DataFrame(cursor).drop(columns="_id")[fields].set_index("code")
        df.report_date = pd.to_datetime(df.report_date, utc=False)
        df.ann_date = pd.to_datetime(df.ann_date, utc=False)
        df.f_ann_date = pd.to_datetime(df.f_ann_date, utc=False)
    else:
        df = pd.DataFrame(cursor).drop(columns="_id").set_index("code")
        df.report_date = pd.to_datetime(df.report_date, utc=False)
        df.ann_date = pd.to_datetime(df.ann_date, utc=False)
        df.f_ann_date = pd.to_datetime(df.f_ann_date, utc=False)
    return df


def QA_fetch_last_financial(
        code: Union[str, List, Tuple] = None,
        cursor_date: Union[str, datetime.datetime, pd.Timestamp] = None,
        report_label: Union[int, str] = None,
        report_type: Union[int, str, List, Tuple] = None,
        sheet_type: str = "income",
        fields: Union[str, List, Tuple] = None) -> pd.DataFrame:
    """获取距离指定日期 (cursor_date) 最近的原始数据 (不包含在 cursor_date 发布的财务数据)，
       当同时输入 cursor_date 与 report_date 时，以 report_date 作为查询标准
       注意：
           这里的 report_type 仅支持 (1,4, 5) 三种类型，以避免混淆合并数据和单季数据等
       说明：
           柳工 (000528) 在 2018 年 8 月 30 日发布半年报，之后在 2018 年 9 月 29 日发布修正报告，
           - 如果输入的 cursor_date 为 2018-08-31, 那么获取到的就是原始半年报，对应 report_type == 5
           - 如果输入的 cursor_date 为 2018-09-30，那么获取到的就是最新合并报表，对应 report_type == 1
           - 如果对应的 cursor_date 为 2019-08-31，需要获取 2018 年半年报，那么就返回柳工在 2019 年 8 月 29 日发布的上年同期基准，对应 report_type == 4

    Args:
        code (Union[str, List, Tuple], optional): 股票代码或股票列表，默认为 None, 查询所有股票
        cursor_date (Union[str, datetime.datetime, pd.Timestamp]): 查询截面日期 (一般指调仓日), 默认为 None
        report_label (Union[str, int], optional): 指定报表类型，这里的类型分类为一季报，半年报，三季报，年报, 默认为 None，即选择距离 cursor_date 最近的报表类型
        report_type (Union[str, List, Tuple], optional): [description]. 报表类型，默认为 None. 即距离 cursor_date 最近的财报，不指定类型，避免引入未来数据
            (1	合并报表	上市公司最新报表（默认）|
             2  单季合并报表
             4	调整合并报表	本年度公布上年同期的财务报表数据，报告期为上年度 |
             5	调整前合并报表	数据发生变更，将原数据进行保留，即调整前的原数据)
        sheet_type (str, optional): 报表类型，默认为 "income".
        fields (Union[str, List, Tuple], optional): 字段, 默认为 None, 返回所有字段

    Returns:
        pd.DataFrame: 复合条件的财务数据
    """
    def _trans_financial_type(x):
        if x.empty:
            return x
        if sheet_type == "balancesheet":
            # 资产负债表属于时点信息，直接返回
            return x
        else:
            if x.iloc[0].report_date[4:] in ['0331', '1231']:
                # 一季报而言，单季合并与普通合并没有区别，直接返回
                # 年报而言，不存在单季概念
                return x.iloc[0]
            if x.iloc[0].report_type in ['1', '4', '5']:
                return x.iloc[0]
            if x.iloc[0].report_type == '2':
                # 尝试查找同一报告期报告类型为 '1' 或 '4' 的报表数据
                # try:
                #     if (x.shape[0] > 1) & (x.iloc[1].report_date == x.iloc[0].report_date) & (x.iloc[1].report_type in ['1', '4']):
                #         return x.iloc[1]
                # except:
                #     return pd.Series()
                # 尝试直接利用单季数据进行拼接
                cursor_x = x.loc[x.report_date.map(str).str.slice(
                    0, 4) == x.iloc[0].report_date[:4]]
                cursor_x = cursor_x.drop_duplicates(subset = ['report_date'], keep='first')
                cursor_x = cursor_x.loc[cursor_x.report_date <=
                                        x.iloc[0].report_date]
                cursor_x = cursor_x.fillna(0)
                non_numeric_columns = sorted(["f_ann_date", "f_ann_date_stamp", "ann_date", "ann_date_stamp", "report_date", "report_date_stamp",
                    "update_flag", "report_type", "code", "report_label"])
                columns = sorted(list(set(cursor_x.columns) - set(non_numeric_columns)))
                rtn_se = cursor_x[columns].sum(axis=0)
                rtn_se = rtn_se.append(cursor_x[non_numeric_columns].iloc[0])
                return rtn_se
    if isinstance(code, str):
        code = (code,)
    if not report_type:
        report_type = ["1", "2", "4", "5"]
    else:
        if isinstance(report_type, int):
            report_type = str(report_type)
        if isinstance(report_type, str):
            if report_type not in ["1", "4", "5"]:
                raise ValueError("[REPORT_TYPE ERROR]")
            report_type = (report_type,)
        else:
            report_type = list(set(report_type) & set('1', '2', '4', '5'))

    if sheet_type not in SHEET_TYPE:
        raise ValueError(f"[SHEET_TYPE ERROR]")
    if report_label:
        report_label = str(report_label)

    if isinstance(fields, str):
        fields = list(
            set([fields, "code", "ann_date", "report_date", "f_ann_date", "report_type"]))
    elif fields:
        fields = list(
            set(fields + ["code", "ann_date", "report_date", "f_ann_date", "report_type"]))

    coll = eval(f"DATABASE.{sheet_type}")
    if (not code) and (not report_label):
        # 为了加快检索速度，从当前日期往前至多回溯一季度，实际调仓时，仅考虑当前能拿到的最新数据，调仓周期一般以月, 季为单位，
        # 最长一般为年报，而修正报表如果超过 1 个季度，基本上怼调仓没有影响，这里以 1 年作为回溯基准
        qry = {
            "f_ann_date_stamp": {
                "$gt": QA_util_date_stamp((pd.Timestamp(cursor_date) - pd.Timedelta(days=400)).strftime("%Y-%m-%d")),
                "$lt": QA_util_date_stamp(cursor_date)
            },
            "report_type": {
                "$in": report_type
            }}
        cursor = coll.find(qry, batch_size=10000).sort([
            ("report_date_stamp", pymongo.DESCENDING),
            ("f_ann_date_stamp", pymongo.DESCENDING)])
        try:
            if not fields:
                df = pd.DataFrame(cursor).drop(columns="_id")
            else:
                df = pd.DataFrame(cursor).drop(columns="_id")[fields]
        except:
            raise ValueError("[QRY ERROR]")
        if sheet_type == "balancesheet":
            return df.groupby("code").apply(lambda x: x.iloc[0])
        return df.groupby("code").apply(_trans_financial_type).unstack()
    if not report_label:
        qry = {
            "code": {
                "$in": code
            },
            "f_ann_date_stamp": {
                "$gt": QA_util_date_stamp((pd.Timestamp(cursor_date) - pd.Timedelta(days=400)).strftime("%Y-%m-%d")),
                "$lt": QA_util_date_stamp(cursor_date)
            },
            "report_type": {"$in": report_type}}
        cursor = coll.find(qry, batch_size=10000).sort([
            ("report_date_stamp", pymongo.DESCENDING),
            ("f_ann_date_stamp", pymongo.DESCENDING)])
        try:
            if not fields:
                df = pd.DataFrame(cursor).drop(columns="_id")
            else:
                df = pd.DataFrame(cursor).drop(columns="_id")[fields]
        except:
            raise ValueError("[QRY ERROR]")
        if sheet_type == "balancesheet":
            return df.groupby("code").apply(lambda x: x.iloc[0])
        return df.groupby("code").apply(_trans_financial_type).unstack()
    if not code:
        qry = {
            "f_ann_date_stamp": {
                "$gt": QA_util_date_stamp((pd.Timestamp(cursor_date) - pd.Timedelta(days=400)).strftime("%Y-%m-%d")),
                "$lt": QA_util_date_stamp(cursor_date)
            },
            "report_type": {
                "$in": report_type
            },
            "report_label": report_label
        }
        cursor = coll.find(qry, batch_size=10000).sort([
            ("report_date_stamp", pymongo.DESCENDING),
            ("f_ann_date_stamp", pymongo.DESCENDING)])
        try:
            if not fields:
                df = pd.DataFrame(cursor).drop(columns="_id")
            else:
                df = pd.DataFrame(cursor).drop(columns="_id")[fields]
        except:
            raise ValueError("[QRY ERROR]")
        if sheet_type == "balancesheet":
            return df.groupby("code").apply(lambda x: x.iloc[0])
        return df.groupby("code").apply(_trans_financial_type).unstack()
    else:
        qry = {
            "code": {
                "$in": code
            },
            "f_ann_date_stamp": {
                "$gt": QA_util_date_stamp((pd.Timestamp(cursor_date) - pd.Timedelta(days=400)).strftime("%Y-%m-%d")),
                "$lt": QA_util_date_stamp(cursor_date)
            },
            "report_type": {
                "$in": report_type
            },
            "report_label": report_label
        }
        cursor = coll.find(qry, batch_size=10000).sort([
            ("report_date_stamp", pymongo.DESCENDING),
            ("f_ann_date_stamp", pymongo.DESCENDING)])
        try:
            if not fields:
                df = pd.DataFrame(cursor).drop(columns="_id")
            else:
                df = pd.DataFrame(cursor).drop(columns="_id")[fields]
        except:
            raise ValueError("[QRY ERROR]")
        # df.report_date = pd.to_datetime(df.report_date, utc=False)
        # df.ann_date = pd.to_datetime(df.ann_date, utc=False)
        # df.f_ann_date = pd.to_datetime(df.f_ann_date, utc=False)
        if sheet_type == "balancesheet":
            return df.groupby("code").apply(lambda x: x.iloc[0])
        return df.groupby("code").apply(_trans_financial_type).unstack()


def QA_fetch_stock_basic(
        code: Union[str, List, Tuple] = None,
        status: Union[str, List, Tuple] = 'L') -> pd.DataFrame:
    """获取股票基本信息

    Args:
        code (Union[str, List, Tuple], optional): 股票代码或列表，默认为 None，获取全部股票
        status (Union[str, List, Tuple], optional): 股票状态, 默认为 'L', 即仍在上市的股票，如果为 None， 则返回所有状态股票

    Returns:
        pd.DataFrame: 股票基本信息
    """
    coll = DATABASE.stock_basic
    if isinstance(code, str):
        code = (code,)
    if isinstance(status, str):
        status = (status,)
    qry = {}
    if not status:
        if not code:
            qry = {}
        else:
            qry = {
                "code": {
                    "$in": code
                }
            }
    else:
        if not code:
            qry = {
                "status": {
                    "$in": status
                }
            }
        else:
            qry = {
                "code": {
                    "$in": code
                },
                "status": {
                    "$in": status
                }
            }
    cursor = coll.find(qry)
    res = pd.DataFrame(cursor)
    if res.empty:
        return res
    else:
        res.list_date = pd.to_datetime(res.list_date, utc=False)
        return res.drop(columns="_id").set_index("code")


def QA_fetch_stock_name(
        code: Union[str, List, Tuple] = None,
        cursor_date: Union[str, datetime.datetime, pd.Timestamp] = None
) -> pd.DataFrame:
    """获取股票历史曾用名

    Args:
        code (Union[str, List, Tuple], optional): 股票代码或列表，默认为 None，查询所有股票.
        cursor (Union[str, datetime.datetime, pd.Timestamp], optional): 截止时间，股票名称距离 cursor_date 最近的名字 

    Returns:
        pd.DataFrame: 股票历史曾用名
    """
    coll = DATABASE.namechange
    if isinstance(code, str):
        code = [code]
    qry = {}
    if not code:
        if not cursor_date:
            qry = {}
        else:
            qry = {
                "start_date_stamp": {
                    "$lte": QA_util_date_stamp(cursor_date)
                },
                "end_date_stamp": {
                    "$gte": QA_util_date_stamp(cursor_date)
                }
            }
    else:
        if not cursor_date:
            qry = {
                "code": {
                    "$in": code
                }
            }
        else:
            qry = {
                "code": {
                    "$in": code
                },
                "start_date_stamp": {
                    "$lte": QA_util_date_stamp(cursor_date)
                },
                "end_date_stamp": {
                    "$gte": QA_util_date_stamp(cursor_date)
                }
            }
    cursor = coll.find(qry)
    res = pd.DataFrame(cursor)
    if res.empty:
        return res
    else:
        res.start_date = pd.to_datetime(res.start_date, utc=False)
        res.end_date = pd.to_datetime(res.end_date, utc=False)
        return res.drop(columns="_id").set_index("code").sort_values(by="start_date_stamp").drop_duplicates(keep="last").sort_index()


def QA_fetch_industry_adv(
    code: Union[str, List, Tuple] = None,
    cursor_date: Union[str, datetime.datetime] = None,
    start: Union[str, datetime.datetime] = None,
    end: Union[str, datetime.datetime] = None,
    levels: Union[str, List, Tuple] = None,
    src: str = "sw"
) -> pd.DataFrame:
    """本地获取指定股票或股票列表的行业

    Args:
        code (Union[str, List, Tuple], optional): 股票代码或列表，默认为 None, 查询所有股票代码.
        cursor_date (Union[str, datetime.datetime], optional): 一般指调仓日，此时不需要再设置 start 与 end
        start(Union[str, datetime.datetime], optional): 起始时间，默认为 None.
        end(Union[str, datetime.datetime], optional): 截止时间, 默认为 None.
        levels (Union[str, List, Tuple], optional): [description]. 对应行业分级级别，默认为 None，查询所有行业分级数据
        src (str, optional): 分级来源，默认为 "sw"(目前仅支持申万行业分类).

    Returns:
        pd.DataFrame: 行业信息
    """
    coll = DATABASE.industry
    if not code:
        code = QA_fetch_stock_list().index.tolist()
    if isinstance(code, str):
        code = [code]
    if isinstance(levels, str):
        levels = [levels, ]
    if not levels:
        levels = ["l1", "l2", "l3"]
    levels = list(map(lambda x: x.lower(), levels))
    df_tmp = pd.DataFrame()
    if not cursor_date:
        if not start:
            qry = {
                "code": {
                    "$in": code
                },
                "level": {
                    "$in": levels
                },
                "src": src.lower()
            }
        else:
            qry = {
                "code": {
                    "$in": code
                },
                "level": {
                    "$in": levels
                },
                "src": src.lower(),
                "in_date_stamp": {
                    "$lte": QA_util_date_stamp(pd.Timestamp(start).strftime("%Y-%m-%d"))
                }
            }
        if coll.count_documents(filter=qry) < 1:
            print("找不到对应行业数据")
            return pd.DataFrame()
        cursor = coll.find(qry)
        df_tmp = pd.DataFrame(cursor).drop(columns="_id")
        if end:
            df_tmp = df_tmp.loc[df_tmp.out_date_stamp > QA_util_date_stamp(
                pd.Timestamp(end).strftime("%Y-%m-%d"))]
    else:
        qry = {
            "code": {
                "$in": code
            },
            "level": {
                "$in": levels
            },
            "src": src.lower(),
            "in_date_stamp": {
                "$lte": QA_util_date_stamp(pd.Timestamp(cursor_date).strftime("%Y-%m-%d"))
            }
        }
        if coll.count_documents(filter=qry) < 1:
            print("找不到对应行业数据")
            return pd.DataFrame()
        cursor = coll.find(qry)
        df_tmp = pd.DataFrame(cursor).drop(columns="_id")
        df_tmp.loc[df_tmp.out_date_stamp > QA_util_date_stamp(
            pd.Timestamp(cursor_date).strftime("%Y-%m-%d"))]
        df_tmp.in_date = pd.to_datetime(df_tmp.in_date, utc=False)
        df_tmp.out_date = pd.to_datetime(df_tmp.out_date, utc=False)
    return df_tmp.drop(columns=["in_date_stamp", "out_date_stamp"])


def QA_fetch_daily_basic(
    code: Union[str, List, Tuple] = None,
    start: Union[str, pd.Timestamp, datetime.datetime] = None,
    end: Union[str, pd.Timestamp, datetime.datetime] = None,
    cursor_date: Union[str, pd.Timestamp, datetime.datetime] = None,
    fields: Union[str, Tuple, List]= None
) -> pd.DataFrame:
    """获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等

    Args:
        code (Union[str, List, Tuple], optional): 指定股票代码或列表,  默认为 None，获取全市场
        start (Union[str, pd.Timestamp, datetime.datetime], optional): 起始日期，默认为 None
        end (Union[str, pd.Timestamp, datetime.datetime], optional): 结束日期，默认为 None
        cursor_date (Union[str, pd.Timestamp, datetime.datetime], optional): 指定日期，与 start 和 end 冲突，只能选择 cursor_date
           或者 start, end
        fields (Union[str, Tuple, List], optional): 指定 fields

    Returns:
        pd.DataFrame: 以日期，股票名为 Multiindex 的基本信息
    """
    if isinstance(code, str):
        code = (code,)
    if not code:
        if (not start) and (not cursor_date):
            raise ValueError(
                "[ERROR]\tstart and end and cursor_date cannot all be none!")
        if not cursor_date:
            if not end:
                end_stamp = QA_util_date_stamp(datetime.date.today())
            else:
                end_stamp = QA_util_date_stamp(end)
            start_stamp = QA_util_date_stamp(start)
            qry = {
                "trade_date_stamp": {
                    "$gte": start_stamp,
                    "$lte": end_stamp
                }
            }
        else:
            real_trade_date = QA_util_get_real_date(cursor_date)
            trade_date_stamp = QA_util_date_stamp(real_trade_date)
            qry = {
                "trade_date_stamp":  trade_date_stamp
            }
    else:
        if (not start) and (not cursor_date):
            raise ValueError(
                "[ERROR]\tstart and end and cursor_date cannot all be none!")
        if not cursor_date:
            if not end:
                end_stamp = QA_util_date_stamp(datetime.date.today())
            else:
                end_stamp = QA_util_date_stamp(end)
            start_stamp = QA_util_date_stamp(start)
            qry = {
                "code": {
                    "$in": code
                },
                "trade_date_stamp": {
                    "$gte": start_stamp,
                    "$lte": end_stamp
                }
            }
        else:
            real_trade_date = QA_util_get_real_date(cursor_date)
            trade_date_stamp = QA_util_date_stamp(real_trade_date)
            qry = {
                "code": {
                    "$in": code
                },
                "trade_date_stamp": trade_date_stamp
            }
    coll = DATABASE.daily_basic
    cursor = coll.find(qry)
    df = pd.DataFrame(cursor)
    if df.empty:
        return df
    df = df.rename(columns={"trade_date": "date"}).drop(
        columns="_id")
    df.date = pd.to_datetime(df.date, utc=False)
    df = df.set_index(["date", "code"]).sort_index()
    if not fields:
        return df
    return df[fields]


if __name__ == "__main__":
    # print(QA_fetch_get_individual_financial(
    #     "000001", "2020-01-01", "2020-12-31"))
    # print(QA_fetch_get_individual_financial(
    #      "000001", report_date="2020-03-31", fields="basic_eps"))
    # print(QA_fetch_get_crosssection_financial('2020-03-31'))
    # print(QA_fetch_crosssection_financial("2020-03-31", fields="basic_eps"))
    # df = QA_fetch_financial_adv(start="2018-06-30", end="2018-09-30")
    # print(df.loc['000528', ["report_date", "f_ann_date",
    #                         "ann_date", "basic_eps", "report_type", "update_flag", "report_label"]])
    # print(df)
    # print(QA_fetch_stock_basic(status="D"))
    # 最近财务数据获取测试
    # print(QA_fetch_last_financial(
    #     code="000596", cursor_date="2020-10-08"))
    # print(QA_fetch_last_financial(
    #         code=QA_fetch_stock_list().index.tolist(), cursor_date="2020-10-08"))
    # print(QA_fetch_last_financial(
    #         code = '000001', cursor_date = '2020-10-08'
    # ))
    code = QA_fetch_stock_list().index.tolist()
    cursor_date = '2020-10-08'
    df_origin = QA_fetch_last_financial(code = code, cursor_date = cursor_date, sheet_type = "balancesheet")
    # print(QA_fetch_last_financial(
    #     cursor_date="2018-08-31"))
    # print(QA_fetch_last_financial(
    #     cursor_date="2018-08-31", code=["000528"], fields=["report_date", "ann_date", "f_ann_date", "update_flag"]))
    # print(QA_fetch_financial_adv(
    #     cursor_date="2018-08-31"))
    # 股票基本信息获取测试
    # print(QA_fetch_stock_basic("000001"))
    # print(QA_fetch_stock_basic(status=["P", "D"]))
    # 行业获取测试
    # print(QA_fetch_industry_adv(start="1998-01-01", end="2020-12-02").head())
    # print(QA_fetch_industry_adv(["000001", "600000"],
    #                             start="1998-01-01", end="2020-12-02"))
    # print(QA_fetch_industry_adv(
    #     ["000001", "600000"], cursor_date="2020-12-02"))
    # print(QA_fetch_stock_name(
    #     code=['000001', '000002'], cursor_date="20081009"))
    # print(QA_fetch_daily_basic(cursor_date="2018-01-01"))
