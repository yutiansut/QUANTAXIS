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
MIN_SEC = {"1min": "60s", "5min": "300s",
           "15min": "900s", "30min": "1800s", "60min": "3600s"}


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
    掘金实现方式
    save current day's stock_min data
    """
    # 导入掘金模块且进行登录
    try:
        from gm.api import set_token
        from gm.api import history
        # 请自行将掘金量化的 TOKEN 替换掉 GMTOKEN
        set_token("9c5601171e97994686b47b5cbfe7b2fc8bb25b09")
    except:
        raise ModuleNotFoundError

    # 股票代码格式化
    code_list = list(
        map(
            lambda x: "SHSE." + x if x[0] == "6" else "SZSE." + x,
            QA_fetch_get_stock_list().code.unique().tolist(),
        ))
    coll = client.stock_min
    coll.create_index([
        ("code", pymongo.ASCENDING),
        ("time_stamp", pymongo.ASCENDING),
        ("date_stamp", pymongo.ASCENDING),
    ])
    err = []

    def __transform_gm_to_qa(df, type_):
        """
        将掘金数据转换为 qa 格式
        """

        if df is None or len(df) == 0:
            raise ValueError("没有掘金数据")

        df = df.rename(columns={
            "eob": "datetime",
            "volume": "vol",
            "symbol": "code"
        }).drop(["bob", "frequency", "position", "pre_close"], axis=1)
        df["code"] = df["code"].map(str).str.slice(5, )
        df["datetime"] = pd.to_datetime(df["datetime"].map(str).str.slice(
            0, 19))
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
                col_filter = {"code": str(code)[5:], "type": type_}
                ref_ = coll.find(col_filter)
                end_time = str(now_time())[0:19]
                if coll.count_documents(col_filter) > 0:
                    start_time = ref_[coll.count_documents(
                        col_filter) - 1]["datetime"]
                    print(start_time)
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min",
                             "5min",
                             "15min",
                             "30min",
                             "60min"
                             ].index(type_),
                            str(code)[5:],
                            start_time,
                            end_time,
                            type_,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        df = history(
                            symbol=code,
                            start_time=start_time,
                            end_time=end_time,
                            frequency=MIN_SEC[type_],
                            df=True
                        )
                        __data = __transform_gm_to_qa(df, type_)
                        if len(__data) > 1:
                            # print(QA_util_to_json_from_pandas(__data)[1::])
                            # print(__data)
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
                             "60min"
                             ].index(type_),
                            str(code)[5:],
                            start_time,
                            end_time,
                            type_,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        df = history(
                            symbol=code,
                            start_time=start_time,
                            end_time=end_time,
                            frequency=MIN_SEC[type_],
                            df=True
                        )
                        __data = __transform_gm_to_qa(df, type_)
                        if len(__data) > 1:
                            # print(__data)
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
                            # print(QA_util_to_json_from_pandas(__data)[1::])
        except Exception as e:
            QA_util_log_info(e, ui_log=ui_log)
            err.append(code)
            QA_util_log_info(err, ui_log=ui_log)

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
