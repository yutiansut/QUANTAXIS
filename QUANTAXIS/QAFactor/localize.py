"""
数据本地化方案
1. 更新方式分为两种：全量更新与增量更新
2. 考虑到 tushare 的查询接口太过简陋，同时考虑到查询限制，针对增量更新，作如下假设
    - 对 report_type = 1 的财务数据，更新从最新的两期财务报告期开始往后
    - 对 report_type = 5，11 的财务数据，增量更新时间为 report_type 最新一起财务报告期往前追溯 3 年
    - 对 report_type = 4 的财务数据，也是往前追溯 3 年
"""
import datetime
import time
from typing import List, Tuple, Union

import pandas as pd
import pymongo
import tushare as ts

from QUANTAXIS.QAFactor.fetcher import (REPORT_DATE_TAILS, REPORT_TYPE,
                                        SHEET_TYPE,
                                        QA_fetch_crosssection_financial,
                                        QA_fetch_get_crosssection_financial,
                                        QA_fetch_get_daily_basic,
                                        QA_fetch_get_individual_financial,
                                        QA_fetch_stock_basic)
from QUANTAXIS.QAFactor.utils import QA_fmt_code, QA_fmt_code_list
from QUANTAXIS.QAFetch.QATushare import get_pro
from QUANTAXIS.QASetting.QALocalize import (cache_path, download_path, qa_path,
                                            setting_path)
from QUANTAXIS.QAUtil import (DATABASE, QASETTING, QA_util_date_int2str,
                              QA_util_date_stamp, QA_util_get_next_trade_date,
                              QA_util_get_pre_trade_date, QA_util_log_info,
                              QA_util_to_json_from_pandas, trade_date_sse)
from QUANTAXIS.QAUtil.QADate_trade import QA_util_get_pre_trade_date
from QUANTAXIS.QAUtil.QASql import ASCENDING, DESCENDING
from QUANTAXIS.QAUtil.QATransform import QA_util_to_json_from_pandas


def QA_ts_update_all(
    start: Union[str, datetime.datetime] = None,
    end: Union[str, datetime.datetime] = None,
    wait_seconds: int = 61,
    report_type: Union[int, str] = "1",
    max_trial=3,
) -> pd.DataFrame:
    """
    全量更新

    ---
    :param start: 开始时间 (以 report_date 作为比较标准)
    :param end: 结束时间 (以 report_date 作为比较标准)
    :param report_type: 报告类型
    :param wait_seconds: 等待时间
    :param max_trial: 超时重试次数
    """

    def _ts_update_all(report_date, report_type, sheet_type, wait_seconds, max_trial):
        # 获取指定报告期，指定报告类型，指定报表类型的截面数据
        df = QA_fetch_get_crosssection_financial(
            report_date=report_date,
            report_type=report_type,
            sheet_type=sheet_type,
            wait_seconds=wait_seconds,
            max_trial=max_trial,
        )
        coll = eval(f"DATABASE.{sheet_type}")
        # 考虑到查找的方式，可能根据股票代码查找，可能根据报告期查找，可能根据公告期查找，可能根据最后公告期查找，可能根据报告类型查找
        coll.create_index(
            [
                ("code", ASCENDING),
                ("report_label", ASCENDING),
                ("report_date", DESCENDING),
                ("report_type", ASCENDING),
                ("report_date_stamp", ASCENDING),
                ("ann_date_stamp", ASCENDING),
                ("f_ann_date_stamp", ASCENDING),
            ],
            unique=False,
        )
        # FIXME: insert_many may be better
        for item in QA_util_to_json_from_pandas(df):
            report_label = None
            if item["report_date"].endswith("0331"):
                report_label = "1"
            elif item["report_date"].endswith("0630"):
                report_label = "2"
            elif item["report_date"].endswith("0930"):
                report_label = "3"
            elif item["report_date"].endswith("1231"):
                report_label = "4"
            item["report_label"] = report_label
            coll.update_one(
                {
                    "code": item["code"],
                    "report_label": report_label,
                    "report_date": item["report_date"],
                    "report_type": item["report_type"],
                    "report_date_stamp": QA_util_date_stamp(item["report_date"]),
                    "ann_date_stamp": QA_util_date_stamp(item["ann_date"]),
                    "f_ann_date_stamp": QA_util_date_stamp(item["f_ann_date"]),
                },
                {"$set": item},
                upsert=True,
            )

    # 如果不指定起始年份，默认从 1990-01-01 开始
    if not start:
        start = pd.Timestamp("1990-01-01")
    else:
        start = pd.Timestamp(start)
    if not end:
        end = pd.Timestamp(datetime.date.today())
    else:
        end = pd.Timestamp(end)

    # 生成报告期列表
    start_year = start.year
    end_year = end.year
    origin_report_dates = pd.Series(
        [
            pd.Timestamp(year + date_tail)
            for year in pd.date_range(str(start_year), str(end_year + 1), freq="1Y")
            .map(str)
            .str.slice(0, 4)
            for date_tail in REPORT_DATE_TAILS
        ]
    )
    report_dates = origin_report_dates.loc[
        (origin_report_dates >= start) & (origin_report_dates <= end)
    ]

    # Tushare 接口配置
    pro = get_pro()

    # 对 SHEET_TYPE 中所列财务报表进行循环
    for sheet_type in SHEET_TYPE:
        # 对指定报告期列表进行循环
        for report_date in report_dates:
            _ts_update_all(
                report_date=report_date.strftime("%Y%m%d"),
                report_type=report_type,
                sheet_type=sheet_type,
                wait_seconds=wait_seconds,
                max_trial=max_trial,
            )


def QA_ts_update_inc(wait_seconds: int = 61, max_trial=3) -> pd.DataFrame:
    """
    增量更新

    :param wait_seconds: 等待时间
    :param max_trial: 超时重试次数
    ---
    """
    for sheet_type in SHEET_TYPE:
        coll = eval(f"DATABASE.{sheet_type}")
        coll.create_index(
            [
                ("code", ASCENDING),
                ("report_label", ASCENDING),  # 方便指定季报查询
                ("report_date", ASCENDING),  # 方便进行最新报告期的查找
                ("report_type", ASCENDING),
                ("report_date_stamp", ASCENDING),
                ("ann_date_stamp", ASCENDING),
                ("f_ann_date_stamp", ASCENDING),
            ],
            unique=False,
        )
        for report_type in REPORT_TYPE:
            try:
                # 使用最新的合并报表作为基准
                # 当前数据库已经包含了这个代码的数据， 继续增量更新
                # 加入这个判断的原因是因为如果股票是刚上市的 数据库会没有数据 所以会有负索引问题出现
                type_count = coll.count_documents(
                    filter={"report_type": report_type})
                if type_count > 0:
                    # 接着上次获取的日期继续更新
                    ref = coll.find({"report_type": report_type})
                    cursor_date = ref[type_count - 1]["report_date"]
                    cursor_year = pd.Timestamp(cursor_date).year
                    report_dates = None
                    if report_type == "1" or report_type == "2":  # 往前回溯一期
                        fmt_report_date = sorted(
                            [
                                (str(year) + tail)
                                for year in range(
                                    cursor_year - 1, datetime.date.today().year + 1
                                )
                                for tail in REPORT_DATE_TAILS
                            ]
                        )
                        report_dates = fmt_report_date[
                            fmt_report_date.index(cursor_date) - 1:
                        ]
                    else:  # 往前回溯三年
                        fmt_report_date = sorted(
                            [
                                (str(year) + tail)
                                for year in range(
                                    cursor_year - 3, datetime.date.today().year + 1
                                )
                                for tail in REPORT_DATE_TAILS
                            ]
                        )
                        report_dates = fmt_report_date[0:]

                    if not report_dates:
                        raise ValueError("[REPORT_DATES ERROR]")
                    for report_date in report_dates:
                        df_1 = QA_fetch_get_crosssection_financial(
                            report_date=report_date,
                            report_type=report_type,
                            sheet_type=sheet_type,
                            wait_seconds=wait_seconds,
                            max_trial=max_trial,
                        )
                        df_2 = QA_fetch_crosssection_financial(
                            report_date=report_date,
                            report_type=report_type,
                            sheet_type=sheet_type,
                        )
                        # df_1 = df_1.where(pd.notnull(df_1), None)
                        # df_2 = df_2.where(pd.notnull(df_2), None)
                        if df_2.empty:
                            js = QA_util_to_json_from_pandas(df_1)
                            for item in js:
                                report_label = None
                                if item["report_date"].endswith("0331"):
                                    report_label = "1"
                                elif item["report_date"].endswith("0630"):
                                    report_label = "2"
                                elif item["report_date"].endswith("0930"):
                                    report_label = "3"
                                elif item["report_date"].endswith("1231"):
                                    report_label = "4"
                                item["report_label"] = report_label
                                coll.update_one(
                                    {
                                        "code": item["code"],
                                        "report_label": report_label,
                                        "report_date": item["report_date"],
                                        "report_type": item["report_type"],
                                        "report_date_stamp": QA_util_date_stamp(
                                            item["report_date"]
                                        ),
                                        "ann_date_stamp": QA_util_date_stamp(
                                            item["ann_date"]
                                        ),
                                        "f_ann_date_stamp": QA_util_date_stamp(
                                            item["f_ann_date"]
                                        ),
                                    },
                                    {"$set": item},
                                    upsert=True,
                                )
                        else:

                            def _func(x):
                                if x[-4:] == "0331":
                                    return "1"
                                elif x[-4:] == "0630":
                                    return "2"
                                elif x[-4:] == "0930":
                                    return "3"
                                else:
                                    return "4"

                            df_2 = df_2[df_1.columns]
                            df_1_1 = df_1.loc[
                                (df_1.report_date == report_date)
                                & (df_1.report_type == report_type)
                                & (df_1.update_flag == "0")
                            ].set_index("code")
                            df_2_1 = df_2.loc[
                                (df_2.report_date == report_date)
                                & (df_2.report_type == report_type)
                                & (df_2.update_flag == "0")
                            ].set_index("code")
                            if (
                                (not df_1_1.empty)
                                and (not df_2_1.empty)
                                and len(df_1_1.index.difference(df_2_1.index))
                            ):
                                df_1_1 = df_1_1.loc[
                                    df_1_1.index.difference(df_2_1.index)
                                ].reset_index()
                                df_1_1["ann_date_stamp"] = df_1_1.ann_date.apply(
                                    QA_util_date_stamp
                                )
                                df_1_1["f_ann_date_stamp"] = df_1_1.f_ann_date.apply(
                                    QA_util_date_stamp
                                )
                                df_1_1["report_date_stamp"] = df_1_1.report_date.apply(
                                    QA_util_date_stamp
                                )
                                # TODO: add appendix
                                df_1_1["report_label"] = df_1_1["report_date"].apply(
                                    _func
                                )
                                js = QA_util_to_json_from_pandas(df_1_1)
                                coll.insert_many(js)
                            df_1_2 = df_1.loc[
                                (df_1.report_date == report_date)
                                & (df_1.report_type == report_type)
                                & (df_1.update_flag == "1")
                            ].set_index("code")
                            df_2_2 = df_2.loc[
                                (df_2.report_date == report_date)
                                & (df_2.report_type == report_type)
                                & (df_2.update_flag == "1")
                            ].set_index("code")
                            if (
                                (not df_1_2.empty)
                                and (not df_2_2.empty)
                                and len(df_1_2.index.difference(df_2_2.index))
                            ):
                                df_1_2 = df_1_2.loc[
                                    df_1_2.index.difference(df_2_2.index)
                                ].reset_index()
                                df_1_2["ann_date_stamp"] = df_1_2.ann_date.apply(
                                    QA_util_date_stamp
                                )
                                df_1_2["f_ann_date_stamp"] = df_1_2.f_ann_date.apply(
                                    QA_util_date_stamp
                                )
                                df_1_2["report_date_stamp"] = df_1_2.report_date.apply(
                                    QA_util_date_stamp
                                )
                                df_1_2["report_label"] = df_1_2["report_date"].apply(
                                    _func
                                )
                                js = QA_util_to_json_from_pandas(df_1_2)
                                coll.insert_many(js)
                else:
                    QA_ts_update_all(report_type=report_type)
            except Exception as e:
                print(e)


def QA_ts_update_stock_basic():
    """
    本地化所有股票基本信息
    """
    coll = DATABASE.stock_basic
    coll.create_index(
        [("code", ASCENDING), ("status", ASCENDING),
         ("list_date_stamp", ASCENDING)],
        unique=True,
    )

    # 初始化数据接口
    pro = get_pro()
    # 获取所有数据
    df_1 = pro.stock_basic(exchange="", list_status="L")
    df_2 = pro.stock_basic(exchange="", list_status="P")
    df_3 = pro.stock_basic(exchange="", list_status="D")
    df_1["status"] = "L"
    df_2["status"] = "P"
    df_3["status"] = "D"
    df = df_1.append(df_2).append(df_3)
    df["code"] = QA_fmt_code_list(df.ts_code)
    df["list_date_stamp"] = df.list_date.apply(QA_util_date_stamp)
    df = df.where(pd.notnull(df), None)
    js = QA_util_to_json_from_pandas(df.drop(columns=["ts_code", "symbol"]))
    for item in js:
        qry = {
            "code": item["code"],
            "status": item["status"],
            "list_date_stamp": item["list_date_stamp"],
        }
        if coll.count_documents(qry) == 0:  # 增量更新
            coll.insert_one(item)


def QA_ts_update_namechange():
    """
    保存所有股票的历史曾用名
    """
    # 建表
    coll = DATABASE.namechange
    coll.create_index(
        [
            ("code", ASCENDING),
            ("start_date_stamp", ASCENDING),
            ("end_date_stamp", ASCENDING),
            ("ann_date_stamp", ASCENDING),
        ],
        unique=True,
    )
    # 初始化数据接口
    pro = get_pro()
    # 获取历史所有股票
    symbol_list = sorted(
        list(set(QA_fmt_code_list(QA_fetch_stock_basic().index.tolist(), "ts")))
    )
    df = pd.DataFrame()
    for i, symbol in enumerate(symbol_list):
        if i % 100 == 0:
            print(f"Saving {i}th stock name, stock is {symbol}")
        try:
            df = df.append(pro.namechange(ts_code=symbol))
        except:
            time.sleep(61)
            try:
                df = df.append(pro.namechange(ts_code=symbol))
            except:
                raise ValueError("[ERROR]\t数据获取失败")
    # df.to_csv("test.csv")
    df["code"] = QA_fmt_code_list(df["ts_code"])
    df["start_date_stamp"] = df["start_date"].apply(QA_util_date_stamp)
    df["end_date_stamp"] = df["end_date"].apply(QA_util_date_stamp)
    df["ann_date_stamp"] = df["ann_date"].apply(QA_util_date_stamp)
    df = df.where(pd.notnull(df), None)
    js = QA_util_to_json_from_pandas(df.drop(columns=["ts_code"]))
    for item in js:
        if not item["end_date"]:
            item["end_date_stamp"] = 9999999999
        qry = {
            "code": item["code"],
            "start_date_stamp": item["start_date_stamp"],
            "end_date_stamp": item["end_date_stamp"],
            "ann_date_stamp": item["ann_date_stamp"],
        }
        if coll.count_documents(qry) == 0:
            coll.insert_one(item)


def QA_ts_update_industry(
    level: Union[str, List, Tuple] = ["L1", "L2", "L3"],
    src: Union[str, List, Tuple] = "SW",
):
    """
    保存个股行业信息
    """
    pro = get_pro()
    if isinstance(level, str):
        level = [level]
    if isinstance(src, str):
        src = [src]
    df_industry = pd.DataFrame()
    for s in src:
        for lv in level:
            try:
                df_tmp = pro.index_classify(level=lv, src=s)
                df_tmp["src"] = "sw"
                df_industry = df_industry.append(df_tmp)
            except Exception as e1:
                print(e1)
                time.sleep(61)
                try:
                    df_tmp = pro.index_classify(level=lv, src=s)
                    df_tmp["src"] = "sw"
                    df_industry = df_industry.append(df_tmp)
                except Exception as e2:
                    raise ValueError(e2)
    df_results = pd.DataFrame()
    for idx, item in df_industry.iterrows():
        if idx % 100 == 0:
            print(f"currently saving {idx}th record")
        try:
            df_tmp = pro.index_member(index_code=item["index_code"])
            df_tmp["industry_name"] = item["industry_name"]
            df_tmp["level"] = item["level"].lower()
            df_tmp["src"] = item["src"].lower()
            df_results = df_results.append(df_tmp)
        except Exception as e1:
            print(e1)
            time.sleep(61)
            try:
                df_tmp = pro.index_member(index_code=item["index_code"])
                df_tmp["industry_name"] = item["industry_name"]
                df_tmp["level"] = item["level"].lower()
                df_tmp["src"] = item["src"].lower()
                df_results = df_results.append(df_tmp)
            except Exception as e2:
                raise ValueError(e2)
    df_results.con_code = QA_fmt_code_list(df_results.con_code)
    df_results = df_results.rename(columns={"con_code": "code"})
    df_results = df_results.sort_values(by="code")
    coll = DATABASE.industry
    coll.create_index(
        [
            ("code", ASCENDING),
            ("level", ASCENDING),
            ("src", ASCENDING),
            ("in_date_stamp", DESCENDING),
            ("out_date_stamp", DESCENDING),
        ],
        unique=False,
    )
    for item in QA_util_to_json_from_pandas(df_results):
        item["in_date_stamp"] = QA_util_date_stamp(item["in_date"])
        if not item["out_date"]:
            item["out_date_stamp"] = 9999999999
        else:
            item["out_date_stamp"] = QA_util_date_stamp(item["out_date_stamp"])
        coll.update_one(
            {
                "code": item["code"],
                "level": item["level"],
                "src": item["src"],
                "in_date_stamp": item["in_date_stamp"],
            },
            {"$set": item},
            upsert=True,
        )
    print('finished saving industry')


def QA_ts_update_daily_basic():
    """
    更新每日全市场重要基本面指标，用于选股分析和报表展示
    """
    coll = DATABASE.daily_basic
    coll.create_index(
        [("code", ASCENDING), ("trade_date_stamp", ASCENDING)],
        unique=True,
    )
    ref = coll.find({})
    cnt = coll.count()
    start_date = "1990-01-01"
    if cnt > 0:
        start_date = ref[cnt - 1]["trade_date"]
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    if end_date != start_date:
        start_trade_date = QA_util_get_next_trade_date(start_date)
        end_trade_date = QA_util_get_pre_trade_date(end_date)
    else:
        return
    for trade_date in trade_date_sse[
        trade_date_sse.index(start_trade_date): trade_date_sse.index(end_trade_date) + 1
    ]:
        print(f"saveing {trade_date} daily basic")
        df = QA_fetch_get_daily_basic(trade_date=trade_date)
        if df.empty:
            continue
        df = df.where(df.notnull(), None).reset_index()
        df["trade_date_stamp"] = df["trade_date"].apply(QA_util_date_stamp)
        js = QA_util_to_json_from_pandas(df)
        coll.insert_many(js)


if __name__ == "__main__":
    # QA_ts_update_all()
    # QA_ts_update_inc()
    # QA_ts_update_industry()
    # QA_ts_update_stock_basic()
    # QA_ts_update_namechange()
    QA_ts_update_daily_basic()
