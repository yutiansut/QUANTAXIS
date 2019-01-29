"""
尝试从聚宽、掘金等量化平台更新股票分钟数据
注意：
1.使用聚宽请自行安装 jqdatasdk 并填写账号密码，
  目前其免费额度是每日 100W 条，需要提额的可以自行加其客户，邀请码 8741，可以免费提额到 1000W 条;
2. 使用掘金量化请自行安装 gm, 掘金量化目前仅支持 3.6+，自行填写 token，
  目前其免费额度是每日 800W 条数据
使用方法:
1. 使用聚宽更新数据，请将 'JQUSERNAME' 和 'JQUSERPASSWD' 修改为自己在聚宽注册的账号密码
2. 使用掘金更新数据，请将 'GMTOKEN' 修改为掘金量化终端中的 token 值
3. 在 '__main__' 中直接调用相关函数
4. 代码文件核心在于转换 聚宽、掘金等数据为 QA 相一致格式, 文末还带有转换天软数据的代码，有条件的
   人可以自行转换相应天软分钟数据
"""

import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import pandas as pd
import pymongo

import QUANTAXIS as QA
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
from QUANTAXIS.QAUtil import (
    DATABASE, QA_util_date_stamp, QA_util_get_real_date, QA_util_log_info,
    QA_util_time_stamp, QA_util_to_json_from_pandas, trade_date_sse)


def now_time():
    return (str(
        QA_util_get_real_date(
            str(datetime.date.today() - datetime.timedelta(days=1)),
            trade_date_sse,
            -1,
        )) + " 17:00:00" if datetime.datetime.now().hour < 15 else str(
            QA_util_get_real_date(
                str(datetime.date.today()), trade_date_sse, -1)) + " 15:00:00")


def QA_SU_jq_save_stock_min(client=DATABASE, ui_log=None, ui_progress=None):
    """
    聚宽实现方式
    save current day's stock_min data
    """

    try:
        import jqdatasdk

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

    def __transform_jq_to_qa(df, code):
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
            raise ValueError("输入 JQData 数据")

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
            df["datetime"].map(str).apply(lambda x: QA_util_date_stamp(x)))
        df["type"] = "1min"

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
            for type in ["1min"]:
                ref_ = coll.find({"code": str(code)[0:6], "type": type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]["datetime"]
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min"].index(type),
                            str(code)[0:6],
                            start_time,
                            end_time,
                            type,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        df = jqdatasdk.get_price(
                            security=code,
                            start_date=start_time,
                            end_date=end_time,
                            frequency=type[:2],
                        )
                        __data = __transform_jq_to_qa(df, code=code[:6])
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
                else:
                    start_time = "2015-01-01 09:30:00"
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min"].index(type),
                            str(code)[0:6],
                            start_time,
                            end_time,
                            type,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        __data == __transform_jq_to_qa(
                            jqdatasdk.get_price(
                                security=code,
                                start_date=start_time,
                                end_date=end_time,
                                frequency=type[:2],
                            ),
                            code=code[:6],
                        )
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
        except Exception as e:
            QA_util_log_info(e, ui_log=ui_log)
            err.append(code)
            QA_util_log_info(err, ui_log=ui_log)

    executor = ThreadPoolExecutor(max_workers=2)
    # executor.map((__saving_work,  stock_list[i_], coll),URLS)
    res = {
        executor.submit(__saving_work, code_list[i_], coll)
        for i_ in range(len(code_list))
    }
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        # QA_util_log_info(
        #    'The {} of Total {}'.format(count,
        #                                 len(code_list)),
        #    ui_log=ui_log
        # )

        strProgress = "DOWNLOAD PROGRESS {} ".format(
            str(float(count / len(code_list) * 100))[0:4] + "%")
        intProgress = int(count / len(code_list) * 10000.0)
        # QA_util_log_info(
        #    strProgress,
        #     ui_log,
        #     ui_progress=ui_progress,
        #     ui_progress_int_value=intProgress
        # )
        count = count + 1
    if len(err) < 1:
        QA_util_log_info("SUCCESS", ui_log=ui_log)
    else:
        QA_util_log_info(" ERROR CODE \n ", ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


def QA_SU_gm_save_stock_min(client=DATABASE, ui_log=None, ui_progress=None):
    """
    掘金量化实现方式
    save current day's stock_min data
    """

    try:
        from gm.api import set_token
        from gm.api import history

        set_token("GMTOKEN")
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

    def __transform_gm_to_qa(df):
        """
        将掘金数据转换为 qa 格式
        """

        if df is None or len(df) == 0:
            raise ValueError("掘金数据转换时没有数据")

        df = df.rename(columns={
            "eob": "datetime",
            "volume": "vol",
            "symbol": "code"
        }).drop(["bob", "frequency", "position", "pre_close"], axis=1)
        df["code"] = df["code"].map(str).str.slice(5)
        df["datetime"] = pd.to_datetime(df["datetime"].map(str).str.slice(
            0, 19))
        df["date"] = df.datetime.map(str).str.slice(0, 10)
        df = df.set_index("datetime", drop=False)
        df["date_stamp"] = df["date"].apply(lambda x: QA_util_date_stamp(x))
        df["time_stamp"] = (
            df["datetime"].map(str).apply(lambda x: QA_util_date_stamp(x)))
        df["type"] = "1min"

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

    def __saveing_work(code, coll):
        QA_util_log_info(
            "##JOB03 Now Saving STOCK_MIN ==== {}".format(code), ui_log=ui_log)
        try:
            for type in ["1min"]:
                ref_ = coll.find({"code": str(code)[0:6], "type": type})
                end_time = str(now_time())[0:19]
                if ref_.count() > 0:
                    start_time = ref_[ref_.count() - 1]["datetime"]
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min"].index(type),
                            str(code)[0:6],
                            start_time,
                            end_time,
                            type,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        df = history(
                            symbol=code,
                            start_time=start_time,
                            end_time=end_time,
                            frequency=type,
                        )
                        __data = __transform_gm_to_qa(df, code=code[:6])
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
                        __data == __transform_gm_to_qa(df, code=code[:6])
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
                else:
                    start_time = "2015-01-01 09:30:00"
                    QA_util_log_info(
                        "##JOB03.{} Now Saving {} from {} to {} == {}".format(
                            ["1min"].index(type),
                            str(code)[0:6],
                            start_time,
                            end_time,
                            type,
                        ),
                        ui_log=ui_log,
                    )
                    if start_time != end_time:
                        df = history(
                            symbol=code,
                            start_time=start_time,
                            end_time=end_time,
                            frequency=type,
                        )
                        __data = __transform_gm_to_qa(df, code=code[:6])
                        if len(__data) > 1:
                            coll.insert_many(
                                QA_util_to_json_from_pandas(__data)[1::])
        except Exception as e:
            QA_util_log_info(e, ui_log=ui_log)
            err.append(code)
            QA_util_log_info(err, ui_log=ui_log)

    executor = ThreadPoolExecutor(max_workers=2)
    # executor.map((__saving_work,  stock_list[i_], coll),URLS)
    res = {
        executor.submit(__saving_work, code_list[i_], coll)
        for i_ in range(len(code_list))
    }
    count = 0
    for i_ in concurrent.futures.as_completed(res):
        # QA_util_log_info(
        #    'The {} of Total {}'.format(count,
        #                                 len(code_list)),
        #    ui_log=ui_log
        # )

        strProgress = "DOWNLOAD PROGRESS {} ".format(
            str(float(count / len(code_list) * 100))[0:4] + "%")
        intProgress = int(count / len(code_list) * 10000.0)
        # QA_util_log_info(
        #    strProgress,
        #     ui_log,
        #     ui_progress=ui_progress,
        #     ui_progress_int_value=intProgress
        # )
        count = count + 1
    if len(err) < 1:
        QA_util_log_info("SUCCESS", ui_log=ui_log)
    else:
        QA_util_log_info(" ERROR CODE \n ", ui_log=ui_log)
        QA_util_log_info(err, ui_log=ui_log)


def transform_ss_to_qa(file_path: str = None):
    """
    导入相应 csv 文件，并处理格式
    1. 这里默认为天软数据格式:

         time                  symbol      open    high    low     close   volume  amount
       0 2013-08-01 09:31:00	SH600000	7.92	7.92	7.87	7.91	518700	4105381
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
    df_local = df_local.rename(columns={"time": "datetime", "volume": "vol"})

    # 格式处理
    df_local = df_local.assign(
        code=df_local.symbol.map(str).str.slice(2),
        date=df_local.datetime.map(str).str.slice(0, 10),
    ).drop(
        "symbol", axis=1)
    df_local = df_local.assign(
        datetime=pd.to_datetime(df_local.datetime),
        date_stamp=df_local.date.apply(lambda x: QA_util_date_stamp(x)),
        time_stamp=df_local.datetime.apply(lambda x: QA_util_time_stamp(x)),
        type="1min",
    ).set_index(
        "datetime", drop=False)
    df_local["datetime"] = df_local["datetime"].map(str)
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


def transform_jq_to_qa(_data, code_name: str = None):
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

    if _data is None or len(_data) == 0:
        raise ValueError("输入 JQData 格式数据")

    df_local = _data.reset_index().rename(columns={
        "index": "datetime",
        "volume": "vol",
        "money": "amount"
    })

    df_local["code"] = code_name
    df_local["date"] = df_local.datetime.map(str).str.slice(0, 10)
    df_local = df_local.set_index("datetime", drop=False)
    df_local["date_stamp"] = df_local["date"].apply(
        lambda x: QA_util_date_stamp(x))
    df_local["time_stamp"] = (
        df_local["datetime"].map(str).apply(lambda x: QA_util_date_stamp(x)))
    df_local["type"] = "1min"

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


def transform_gm_to_qa(df):
    """
    将掘金数据转换为 qa 格式
    """
    df = df.rename(columns={
        "eob": "datetime",
        "volume": "vol",
        "symbol": "code"
    }).drop(["bob", "frequency", "position", "pre_close"], axis=1)
    df["code"] = df["code"].map(str).str.slice(5)
    df["datetime"] = pd.to_datetime(df["datetime"].map(str).str.slice(0, 19))
    df["date"] = df.datetime.map(str).str.slice(0, 10)
    df = df.set_index("datetime", drop=False)
    df["date_stamp"] = df["date"].apply(lambda x: QA_util_date_stamp(x))
    df["time_stamp"] = df["datetime"].map(str).apply(
        lambda x: QA_util_date_stamp(x))
    df["type"] = "1min"

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


if __name__ == "__main__":
    QA_SU_jq_save_stock_min()
    # QA_SU_gm_save_stock_min()
