"""
用于将本地掘金分钟数据转换为 QA 格式
有条件的用户可自行转换
"""

import datetime
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pandas as pd
import pymongo
import os

import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
from QUANTAXIS.QAUtil import (
    DATABASE, QA_util_date_stamp, QA_util_get_real_date, QA_util_log_info,
    QA_util_time_stamp, QA_util_to_json_from_pandas, trade_date_sse)


def QA_SU_trans_stock_min(client=DATABASE, ui_log=None, ui_progress=None,
                          data_path: str = "D:\\gm\\", type_="1min"):
    """
    将掘金本地数据导入 QA 数据库
    :param client:
    :param ui_log:
    :param ui_progress:
    :param data_path: 存放掘金数据的路径，默认文件名格式为类似 "SHSE.600000.csv" 格式
    """
    code_list = list(map(lambda x: x.split(".")[1], os.listdir(data_path)))
    coll = client.stock_min
    coll.create_index([
        ("code", pymongo.ASCENDING),
        ("time_stamp", pymongo.ASCENDING),
        ("date_stamp", pymongo.ASCENDING),
    ])
    err = []

    def __transform_gm_to_qa(file_path: str = None, end_time: str = None, type_="1min"):
        """
        导入相应 csv 文件，并处理格式
        1. 这里默认为掘金数据格式:
                 amount                        bob  close                        eob frequency  high   low  open  position  pre_close       symbol  volume
              0  2522972.0  2018-08-16 09:30:00+08:00   9.84  2018-08-16 09:31:00+08:00       60s  9.87  9.84  9.87         0        0.0  SHSE.600000  255900
              1  3419453.0  2018-08-16 09:31:00+08:00   9.89  2018-08-16 09:32:00+08:00       60s  9.90  9.84  9.86         0        0.0  SHSE.600000  346400
              ...
        2. 与 QUANTAXIS.QAFetch.QATdx.QA_fetch_get_stock_min 获取数据进行匹配，具体处理详见相应源码

                              open  close   high    low           vol        amount    ...
           datetime
           2018-12-03 09:31:00  10.99  10.90  10.99  10.90  2.211700e+06  2.425626e+07 ...
        """

        if file_path is None:
            raise ValueError("输入文件地址")

        df_local = pd.read_csv(file_path)

        # 列名处理
        df_local = df_local.rename(columns={
            "eob": "datetime",
            "volume": "vol",
            "symbol": "code"
        }).drop(["bob", "frequency", "position", "pre_close"], axis=1)

        # 格式处理
        df_local["code"] = df_local["code"].map(str).str.slice(5, )
        df_local["datetime"] = pd.to_datetime(df_local["datetime"].map(str).str.slice(
            0, 19))
        df_local["date"] = df_local.datetime.map(str).str.slice(0, 10)
        df_local = df_local.set_index("datetime", drop=False)
        df_local["date_stamp"] = df_local["date"].apply(
            lambda x: QA_util_date_stamp(x))
        df_local["time_stamp"] = (
            df_local["datetime"].map(str).apply(lambda x: QA_util_time_stamp(x)))
        df_local["type"] = type_

        df_local = df_local.loc[slice(None, end_time)]
        df_local["datetime"] = df_local["datetime"].map(str)
        df_local["type"] = type_

        return df_local[[
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
            col_filter = {"code": code, "type": type_}
            ref_ = coll.find(col_filter)
            end_time = ref_[0]['datetime']  # 本地存储分钟数据最早的时间
            filename = "SHSE."+code + \
                ".csv" if code[0] == '6' else "SZSE."+code+".csv"
            __data = __transform_gm_to_qa(
                data_path+filename, end_time, type_)  # 加入 end_time， 避免出现数据重复

            QA_util_log_info(
                "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                    type_,
                    code,
                    __data['datetime'].iloc[0],
                    __data['datetime'].iloc[-1],
                    type_,
                ),
                ui_log=ui_log,
            )
            if len(__data) > 1:
                coll.insert_many(
                    QA_util_to_json_from_pandas(__data)[1::])
        except Exception as e:
            QA_util_log_info(e, ui_log=ui_log)
            err.append(code)
            QA_util_log_info(err, ui_log=ui_log)

    executor = ThreadPoolExecutor(max_workers=4)
    res = {
        executor.submit(__saving_work, code_list[i_], coll)
        for i_ in range(len(code_list))
    }
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        strProgress = "TRANSFORM PROGRESS {} ".format(
            str(float(count / len(code_list) * 100))[0:4] + "%")
        intProgress = int(count / len(code_list) * 10000.0)
        count = count + 1
    if len(err) < 1:
        QA_util_log_info("SUCCESS", ui_log=ui_log)
    else:
        QA_util_log_info(" ERROR CODE \n ", ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)

    if len(err) < 1:
        QA_util_log_info("SUCCESS", ui_log=ui_log)
    else:
        QA_util_log_info(" ERROR CODE \n ", ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


if __name__ == "__main__":
    QA_SU_trans_stock_min()()
