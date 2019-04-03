import concurrent.futures
import datetime
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pandas as pd
import pymongo

import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
from QUANTAXIS.QAUtil import (DATABASE, QA_util_date_stamp,
                              QA_util_get_real_date, QA_util_log_info,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse)

TRADE_HOUR_END = 17


def now_time():
    """
    1. 当前日期如果是交易日且当前时间在 17:00 之前，默认行情取到上个交易日收盘
    2. 当前日期如果是交易日且当前时间在 17:00 之后，默认行情取到当前交易日收盘
    """
    return (str(
        QA_util_get_real_date(
            str(datetime.date.today() - datetime.timedelta(days=1)),
            trade_date_sse,
            -1,
        )) + " 17:00:00" if datetime.datetime.now().hour < TRADE_HOUR_END else str(
            QA_util_get_real_date(
                str(datetime.date.today()), trade_date_sse, -1)) + " 17:00:00")


def QA_SU_save_stock_min(client=DATABASE, ui_log=None, ui_progress=None):
    """
    聚宽实现方式
    save current day's stock_min data
    """
    # 导入聚宽模块且进行登录
    try:
        import jqdatasdk
        # 请自行将 JQUSERNAME 和 JQUSERPASSWD 修改为自己的账号密码
        jqdatasdk.auth("JQUSERNAME", "JQUSERPASSWD")
    except:
        raise ModuleNotFoundError

    # 股票代码格式化
    code_list = list(
        map(
            lambda x: x + ".XSHG" if x[0] == "6" else x + ".XSHE",
            QA_fetch_get_stock_list().code.unique().tolist(),
        ))
    coll = client.stock_min
    coll.create_index([
        ("code", pymongo.ASCENDING),
        ("time_stamp", pymongo.ASCENDING),
        ("date_stamp", pymongo.ASCENDING),
    ])
    err = []

    def __transform_jq_to_qa(df, code, type_):
        """
        处理 jqdata 分钟数据为 qa 格式，并存入数据库
        1. jdatasdk 数据格式:
                          open  close   high    low     volume       money
        2018-12-03 09:31:00  10.59  10.61  10.61  10.59  8339100.0  88377836.0
        2. 与 QUANTAXIS.QAFetch.QATdx.QA_fetch_get_stock_min 获取数据进行匹配，具体处理详见相应源码

                          open  close   high    low           vol        amount    ...
        datetime
        2018-12-03 09:31:00  10.99  10.90  10.99  10.90  2.211700e+06  2.425626e+07 ...
        """

        if df is None or len(df) == 0:
            raise ValueError("没有聚宽数据")

        df = df.reset_index().rename(columns={
            "index": "datetime",
            "volume": "vol",
            "money": "amount"
        })

        df["code"] = code
        df["date"] = df.datetime.map(str).str.slice(0, 10)
        df = df.set_index("datetime", drop=False)
        df["date_stamp"] = df["date"].apply(lambda x: QA_util_date_stamp(x))
        df["time_stamp"] = (
            df["datetime"].map(str).apply(lambda x: QA_util_time_stamp(x)))
        df["type"] = type_

        return df[[
            "open",
            "close",
            "high",
            "low",
            "vol",
            "amount",
            "datetime",
            "code",
            "date",
            "date_stamp",
            "time_stamp",
            "type",
        ]]

    def __saving_work(code, coll):
        QA_util_log_info(
            "##JOB03 Now Saving STOCK_MIN ==== {}".format(code), ui_log=ui_log)
        try:
            for type_ in ["1min", "5min", "15min", "30min", "60min"]:
                col_filter = {"code": str(code)[0:6], "type": type_}
                ref_ = coll.find(col_filter)
                end_time = str(now_time())[0:19]
                if coll.count_documents(col_filter) > 0:
                    start_time = ref_[coll.count_documents(
                        col_filter) - 1]["datetime"]
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min",
                             "5min",
                             "15min",
                             "30min",
                             "60min"].index(type_),
                            str(code)[0:6],
                            start_time,
                            end_time,
                            type_,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        df = jqdatasdk.get_price(
                            security=code,
                            start_date=start_time,
                            end_date=end_time,
                            frequency=type_.split("min")[0]+"m",
                        )
                        __data = __transform_jq_to_qa(
                            df, code=code[:6], type_=type_)
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
                else:
                    start_time = "2015-01-01 09:30:00"
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min",
                             "5min",
                             "15min",
                             "30min",
                             "60min"].index(type_),
                            str(code)[0:6],
                            start_time,
                            end_time,
                            type_,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        __data == __transform_jq_to_qa(
                            jqdatasdk.get_price(
                                security=code,
                                start_date=start_time,
                                end_date=end_time,
                                frequency=type_.split("min")[0]+"m",
                            ),
                            code=code[:6],
                            type_=type_
                        )
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
        except Exception as e:
            QA_util_log_info(e, ui_log=ui_log)
            err.append(code)
            QA_util_log_info(err, ui_log=ui_log)

    # 聚宽之多允许三个线程连接
    executor = ThreadPoolExecutor(max_workers=2)
    res = {
        executor.submit(__saving_work, code_list[i_], coll)
        for i_ in range(len(code_list))
    }
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        QA_util_log_info(
            'The {} of Total {}'.format(count,
                                        len(code_list)),
            ui_log=ui_log
        )

        strProgress = "DOWNLOAD PROGRESS {} ".format(
            str(float(count / len(code_list) * 100))[0:4] + "%")
        intProgress = int(count / len(code_list) * 10000.0)

        QA_util_log_info(
            strProgress,
            ui_log,
            ui_progress=ui_progress,
            ui_progress_int_value=intProgress
        )
        count = count + 1
    if len(err) < 1:
        QA_util_log_info("SUCCESS", ui_log=ui_log)
    else:
        QA_util_log_info(" ERROR CODE \n ", ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


if __name__ == "__main__":
    QA_SU_save_stock_min()
