# coding: utf-8
# Author: 阿财（Rgveda@github）（11652964@qq.com）
# Created date: 2020-02-27
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
# The above copyright notice and this permission notice shall be included in
# all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import datetime
import time
from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta
import pandas as pd

from QUANTAXIS.QAUtil import (
    DATABASE,
    QASETTING,
    QA_util_log_info,
    QA_util_log_expection,
    QA_util_to_json_from_pandas
)
from QUANTAXIS.QAUtil.QADate_Adv import (
    QA_util_timestamp_to_str,
    QA_util_datetime_to_Unix_timestamp,
    QA_util_print_timestamp
)
from QUANTAXIS.QAFetch.QAOKEx import (
    QA_fetch_okex_symbols,
    QA_fetch_okex_kline,
    QA_fetch_okex_kline_min,
    OKEx2QA_FREQUENCY_DICT
)
from QUANTAXIS.QAUtil.QAcrypto import (
    QA_util_save_raw_symbols,
    QA_util_find_missing_kline
)
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_cryptocurrency_list)

import pymongo

# OKEx的历史数据只提供2000个bar
OKEx_MIN_DATE = datetime.datetime(2017, 10, 1, tzinfo=tzutc())
OKEx_EXCHANGE = 'OKEX'
OKEx_SYMBOL = 'OKEX.{}'


def QA_SU_save_okex(frequency):
    """
    Save OKEx kline "smart"
    """
    if (frequency not in ["1d", '86400', "1day", "day"]):
        return QA_SU_save_okex_min(frequency)
    else:
        return QA_SU_save_okex_day(frequency)


def QA_SU_save_okex_day(
    frequency='86400', 
    ui_log=None, 
    ui_progress=None):
    """
    Save OKEx day kline K线 日线数据，统一转化字段保存数据为 crypto_asset_day
    """
    symbol_template = OKEx_SYMBOL
    symbol_list = QA_fetch_cryptocurrency_list(OKEx_EXCHANGE)
    col = DATABASE.cryptocurrency_day
    col.create_index(
        [
            ("symbol",
             pymongo.ASCENDING),
            ("date_stamp",
             pymongo.ASCENDING)
        ],
        unique=True
    )

    end = datetime.datetime.now(tzutc())

    QA_util_log_info(
        'Starting DOWNLOAD PROGRESS of day Klines from {:s}... '.format(OKEx_EXCHANGE),
        ui_log=ui_log,
        ui_progress=ui_progress
    )
    for index in range(len(symbol_list)):
        symbol_info = symbol_list.iloc[index]
        QA_util_log_info(
            'The "{}" #{} of total in {}'.format(
                symbol_template.format(symbol_info['symbol']),
                index,
                len(symbol_list)
            ),
            ui_log=ui_log,
            ui_progress=ui_progress
        )
        QA_util_log_info(
            'DOWNLOAD PROGRESS {} '
            .format(str(float(index / len(symbol_list) * 100))[0:4] + '%'),
            ui_log=ui_log,
            ui_progress=ui_progress
        )
        query_id = {
            "symbol": symbol_template.format(symbol_info['symbol']),
        }
        ref = col.find(query_id).sort('date_stamp', -1)

        if (col.count_documents(query_id) > 0):
            start_stamp = ref.next()['date_stamp']
            start_time = datetime.datetime.fromtimestamp(
                start_stamp + 1,
                tz=tzutc()
            )
            QA_util_log_info(
                'UPDATE_SYMBOL "{}" Trying updating "{}" from {} to {}'.format(
                    symbol_template.format(symbol_info['symbol']),
                    OKEx2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
            # 查询到 Kline 缺漏，点抓取模式，按缺失的时间段精确请求K线数据
            missing_data_list = QA_util_find_missing_kline(
                symbol_template.format(symbol_info['symbol']),
                OKEx2QA_FREQUENCY_DICT[frequency],
            )[::-1]
        else:
            start_time = OKEx_MIN_DATE
            QA_util_log_info(
                'NEW_SYMBOL "{}" Trying downloading "{}" from {} to {}'.format(
                    symbol_template.format(symbol_info['symbol']),
                    OKEx2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
            
            miss_kline = pd.DataFrame(
                [
                    [
                        int(QA_util_datetime_to_Unix_timestamp(start_time)),
                        int(QA_util_datetime_to_Unix_timestamp(end)),
                        '{} to {}'.format(start_time,
                                         end)
                    ]
                ],
                columns=['expected',
                         'between',
                         'missing']
            )
            missing_data_list = miss_kline.values

        if len(missing_data_list) > 0:
            # 查询确定中断的K线数据起止时间，缺分时数据，补分时数据
            expected = 0
            between = 1
            missing = 2
            reqParams = {}
            for i in range(len(missing_data_list)):
                reqParams['from'] = int(missing_data_list[i][expected])
                reqParams['to'] = int(missing_data_list[i][between])
                if (reqParams['from'] >
                    (QA_util_datetime_to_Unix_timestamp() + 120)):
                    # 出现“未来”时间，一般是默认时区设置错误造成的
                    QA_util_log_info(
                        'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                        .format(
                            symbol_template.format(symbol_info['symbol']),
                            frequency,
                            QA_util_print_timestamp(reqParams['from']),
                            QA_util_print_timestamp(
                                QA_util_datetime_to_Unix_timestamp()
                            )
                        )
                    )
                    # 跳到下一个时间段
                    continue

                QA_util_log_info(
                    'Fetch "{:s}" slices "{:s}" kline：{:s} to {:s}'.format(
                        symbol_template.format(symbol_info['symbol']),
                        OKEx2QA_FREQUENCY_DICT[frequency],
                        QA_util_timestamp_to_str(
                            missing_data_list[i][expected]
                        )[2:16],
                        QA_util_timestamp_to_str(
                            missing_data_list[i][between]
                        )[2:16]
                    )
                )
                data = QA_fetch_okex_kline(
                    symbol_info['symbol'],
                    time.mktime(start_time.utctimetuple()),
                    time.mktime(end.utctimetuple()),
                    frequency,
                    callback_func=QA_SU_save_data_okex_callback
                )

        if data is None:
            QA_util_log_info(
                'SYMBOL "{}" from {} to {} has no data'.format(
                    symbol_template.format(symbol_info['symbol']),
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
            continue
    QA_util_log_info(
        'DOWNLOAD PROGRESS of day Klines from {:s} accomplished.'.format(OKEx_EXCHANGE),
        ui_log=ui_log,
        ui_progress=ui_progress
    )


def QA_SU_save_okex_min(
    frequency='60', 
    ui_log=None, 
    ui_progress=None):
    """
    Save OKEx min kline 分钟线数据，统一转化字段保存数据为 crypto_asset_min
    """
    symbol_template = OKEx_SYMBOL
    symbol_list = QA_fetch_cryptocurrency_list(OKEx_EXCHANGE)
    col = DATABASE.cryptocurrency_min
    col.create_index(
        [
            ("symbol",
             pymongo.ASCENDING),
            ('time_stamp',
             pymongo.ASCENDING),
            ('date_stamp',
             pymongo.ASCENDING)
        ]
    )
    col.create_index(
        [
            ("symbol",
             pymongo.ASCENDING),
            ("type",
             pymongo.ASCENDING),
            ('time_stamp',
             pymongo.ASCENDING)
        ],
        unique=True
    )

    end = datetime.datetime.now(tzutc())

    QA_util_log_info(
        'Starting DOWNLOAD PROGRESS of min Klines from {:s}... '.format(OKEx_EXCHANGE),
        ui_log=ui_log,
        ui_progress=ui_progress
    )
    for index in range(len(symbol_list)):
        symbol_info = symbol_list.iloc[index]
        # 上架仅处理交易对
        QA_util_log_info(
            'The "{}" #{} of total in {}'.format(
                symbol_template.format(symbol_info['symbol']),
                index,
                len(symbol_list)
            ),
            ui_log=ui_log,
            ui_progress=ui_progress
        )
        QA_util_log_info(
            'DOWNLOAD PROGRESS {} '
            .format(str(float(index / len(symbol_list) * 100))[0:4] + '%'),
            ui_log=ui_log,
            ui_progress=ui_progress
        )
        query_id = {
            "symbol": symbol_template.format(symbol_info['symbol']),
            'type': OKEx2QA_FREQUENCY_DICT[frequency]
        }
        ref = col.find(query_id).sort('time_stamp', -1)

        if (col.count_documents(query_id) > 0):
            start_stamp = ref.next()['time_stamp']
            start_time = datetime.datetime.fromtimestamp(
                start_stamp + 1,
                tz=tzutc()
            )
            QA_util_log_info(
                'UPDATE_SYMBOL "{}" Trying updating "{}" from {} to {}'.format(
                    symbol_template.format(symbol_info['symbol']),
                    OKEx2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )

            # 查询到 Kline 缺漏，点抓取模式，按缺失的时间段精确请求K线数据
            missing_data_list = QA_util_find_missing_kline(
                symbol_template.format(symbol_info['symbol']),
                OKEx2QA_FREQUENCY_DICT[frequency],
            )[::-1]
        else:
            start_time = OKEx_MIN_DATE
            QA_util_log_info(
                'NEW_SYMBOL "{}" Trying downloading "{}" from {} to {}'.format(
                    symbol_template.format(symbol_info['symbol']),
                    OKEx2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
            miss_kline = pd.DataFrame(
                [
                    [
                        int(QA_util_datetime_to_Unix_timestamp(start_time)),
                        int(QA_util_datetime_to_Unix_timestamp(end)),
                        '{} to {}'.format(start_time,
                                         end)
                    ]
                ],
                columns=['expected',
                         'between',
                         'missing']
            )
            missing_data_list = miss_kline.values

        if len(missing_data_list) > 0:
            # 查询确定中断的K线数据起止时间，缺分时数据，补分时数据
            expected = 0
            between = 1
            missing = 2
            reqParams = {}
            for i in range(len(missing_data_list)):
                reqParams['from'] = int(missing_data_list[i][expected])
                reqParams['to'] = int(missing_data_list[i][between])
                if (reqParams['from'] >
                    (QA_util_datetime_to_Unix_timestamp() + 120)):
                    # 出现“未来”时间，一般是默认时区设置错误造成的
                    QA_util_log_info(
                        'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                        .format(
                            symbol_template.format(symbol_info['symbol']),
                            frequency,
                            QA_util_print_timestamp(reqParams['from']),
                            QA_util_print_timestamp(
                                QA_util_datetime_to_Unix_timestamp()
                            )
                        )
                    )
                    # 跳到下一个时间段
                    continue

                QA_util_log_info(
                    'Fetch "{:s}" slices "{:s}" kline：{:s} to {:s}'.format(
                        symbol_template.format(symbol_info['symbol']),
                        OKEx2QA_FREQUENCY_DICT[frequency],
                        QA_util_timestamp_to_str(
                            missing_data_list[i][expected]
                        )[2:16],
                        QA_util_timestamp_to_str(
                            missing_data_list[i][between]
                        )[2:16]
                    )
                )
                data = QA_fetch_okex_kline_min(
                    symbol_info['symbol'],
                    start_time=reqParams['from'],
                    end_time=reqParams['to'],
                    frequency=frequency,
                    callback_func=QA_SU_save_data_okex_callback
                )

        if data is None:
            QA_util_log_info(
                'SYMBOL "{}" from {} to {} has no MORE data'.format(
                    symbol_template.format(symbol_info['symbol']),
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )
            continue
    QA_util_log_info(
        'DOWNLOAD PROGRESS of min Klines from {:s} accomplished.'.format(OKEx_EXCHANGE),
        ui_log=ui_log,
        ui_progress=ui_progress
    )


def QA_SU_save_okex_1min():
    QA_SU_save_okex('60')


def QA_SU_save_okex_1day():
    QA_SU_save_okex("86400")


def QA_SU_save_okex_1hour():
    QA_SU_save_okex("3600")


def QA_SU_save_okex_symbol(
    market=OKEx_EXCHANGE,
    client=DATABASE,
):
    """
    保存OKEx交易对信息
    """
    market =  market.upper()
    QA_util_log_info('Downloading {:s} symbol list...'.format(market))

    # 保存 OKEx API 原始 Symbol 数据备查阅，自动交易用得着
    raw_symbol_lists = QA_util_save_raw_symbols(
        QA_fetch_okex_symbols,
        market
    )
    if (len(raw_symbol_lists) > 0):
        # 保存到 QUANTAXIS.crypto_asset_list 数字资产列表，为了跨市场统一查询做数据汇总
        symbol_lists = pd.DataFrame(raw_symbol_lists)

        # market,symbol为 mongodb 索引字段，保存之前必须要检查存在
        symbol_lists['market'] = market
        symbol_lists['category'] = 1
        symbol_lists.rename(
            {
                'instrument_id': 'symbol',
                'tick_size': 'price_precision',
            },
            axis=1,
            inplace=True
        )

        symbol_lists['state'] = 'online'
        symbol_lists['name'] = symbol_lists.apply(
            lambda x: '{:s}/{:s}'.
            format(x['base_currency'].upper(),
                   x['quote_currency'].upper()),
            axis=1
        )
        symbol_lists['desc'] = symbol_lists['name']

        # 移除非共性字段，这些字段只有 broker 才关心，做对应交易所 broker 接口的时候在交易所 raw_symbol_lists
        # 数据中读取。
        symbol_lists.drop(
            [
                'min_size',
                'size_increment',
            ],
            axis=1,
            inplace=True
        )
        if ('_id' in symbol_lists.columns.values):
            # 有时有，必须单独删除
            symbol_lists.drop(
                [
                    '_id',
                ],
                axis=1,
                inplace=True
            )

        symbol_lists['created_at'] = int(
            time.mktime(datetime.datetime.now().utctimetuple())
        )
        symbol_lists['updated_at'] = int(
            time.mktime(datetime.datetime.now().utctimetuple())
        )

        coll_cryptocurrency_list = client.cryptocurrency_list
        coll_cryptocurrency_list.create_index(
            [('market',
              pymongo.ASCENDING),
             ('symbol',
              pymongo.ASCENDING)],
            unique=True
        )
        try:
            query_id = {'market': market}
            if (coll_cryptocurrency_list.count_documents(query_id) > 0):
                # 删掉重复数据
                query_id = {
                    'market': market,
                    'symbol': {
                        '$in': symbol_lists['symbol'].tolist()
                    }
                }
                coll_cryptocurrency_list.delete_many(query_id)
            coll_cryptocurrency_list.insert_many(
                QA_util_to_json_from_pandas(symbol_lists)
            )
            return symbol_lists
        except:
            QA_util_log_expection(
                'QA_SU_save_okex_symbol(): Insert_many(symbol) to "cryptocurrency_list" got Exception with {} klines'
                .format(len(symbol_lists))
            )
            pass
        return []


def QA_SU_save_data_okex_callback(data, freq):
    """
    异步获取数据回调用的 MongoDB 存储函数，okex返回数据也是时间倒序排列
    """
    symbol_template = OKEx_SYMBOL
    QA_util_log_info(
        'SYMBOL "{}" Recived "{}" from {} to {} in total {} klines'.format(
            data.iloc[0].symbol,
            freq,
            time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(data.iloc[-1].time_stamp)
            )[2:16],
            time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime(data.iloc[0].time_stamp)
            )[2:16],
            len(data)
        )
    )
    if (freq not in ['1day', '86400', 'day', '1d']):
        col = DATABASE.cryptocurrency_min
        col.create_index(
            [
                ("symbol",
                 pymongo.ASCENDING),
                ('time_stamp',
                 pymongo.ASCENDING),
                ('date_stamp',
                 pymongo.ASCENDING)
            ]
        )
        col.create_index(
            [
                ("symbol",
                 pymongo.ASCENDING),
                ("type",
                 pymongo.ASCENDING),
                ('time_stamp',
                 pymongo.ASCENDING)
            ],
            unique=True
        )

        # 查询是否新 tick
        query_id = {
            "symbol": data.iloc[0].symbol,
            'type': data.iloc[0].type,
            'time_stamp': {
                '$in': data['time_stamp'].tolist()
            }
        }
        refcount = col.count_documents(query_id)
    else:
        col = DATABASE.cryptocurrency_day
        col.create_index(
            [
                ("symbol",
                 pymongo.ASCENDING),
                ("date_stamp",
                 pymongo.ASCENDING)
            ],
            unique=True
        )

        # 查询是否新 tick
        query_id = {
            "symbol": data.iloc[0].symbol,
            'date_stamp': {
                '$in': data['date_stamp'].tolist()
            }
        }
        refcount = col.count_documents(query_id)
    if refcount > 0:
        if (len(data) > 1):
            # 删掉重复数据
            col.delete_many(query_id)
            data = QA_util_to_json_from_pandas(data)
            col.insert_many(data)
        else:
            # 持续接收行情，更新记录
            data.drop('created_at', axis=1, inplace=True)
            data = QA_util_to_json_from_pandas(data)
            col.replace_one(query_id, data[0])
    else:
        # 新 tick，插入记录
        data = QA_util_to_json_from_pandas(data)
        col.insert_many(data)


if __name__ == '__main__':
    QA_SU_save_okex_min('900')
    QA_SU_save_okex_symbol()
    #QA_SU_save_okex_1day()
    #QA_SU_save_okex_1hour()
    QA_SU_save_okex_1min()
