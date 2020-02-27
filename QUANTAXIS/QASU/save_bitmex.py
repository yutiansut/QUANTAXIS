# coding: utf-8
# Author: Unknown
# Contributor: 阿财（Rgveda@github）（11652964@qq.com）
# Created date: 2018-06-08
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
import math
from dateutil.tz import tzutc
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import pandas as pd

from QUANTAXIS.QAUtil import (
    DATABASE,
    QASETTING,
    QA_util_log_info,
    QA_util_to_json_from_pandas
)
from QUANTAXIS.QAUtil.QADate_Adv import (QA_util_timestamp_to_str)
from QUANTAXIS.QAFetch.QABitmex import (
    QA_fetch_bitmex_symbols,
    QA_fetch_bitmex_kline,
    Bitmex2QA_FREQUENCY_DICT
)
from QUANTAXIS.QAUtil.QAcrypto import QA_util_save_raw_symbols
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_crypto_asset_list)

import pymongo


def QA_SU_save_bitmex(frequency):
    """
    Save bitmex kline "smart"
    """
    if (frequency not in ["1day", '1d', 'day']):
        return QA_SU_save_bitmex_min(frequency)
    else:
        return QA_SU_save_bitmex_day(frequency)


def QA_SU_save_bitmex_day(
    frequency='1d',
    client=DATABASE,
    ui_log=None,
    ui_progress=None,
):
    """
    获取 bitmex K线 日线数据，统一转化字段保存数据为 crypto_asset_day
    """
    symbol_list = QA_fetch_crypto_asset_list(market='bitmex')
    col = client.crypto_asset_day
    col.create_index(
        [
            ('market',
             pymongo.ASCENDING),
            ("symbol",
             pymongo.ASCENDING),
            ("date_stamp",
             pymongo.ASCENDING)
        ],
        unique=True
    )

    end = datetime.datetime.now(tzutc())

    QA_util_log_info('Starting DOWNLOAD PROGRESS of day Klines from bitmex... ')
    for index in range(len(symbol_list)):
        symbol_info = symbol_list.iloc[index]
        QA_util_log_info(
            'The "{}" #{} of total in {}'.format(
                symbol_info['symbol'],
                index,
                len(symbol_list)
            )
        )
        QA_util_log_info(
            'DOWNLOAD PROGRESS {} '
            .format(str(float(index / len(symbol_list) * 100))[0:4] + '%')
        )
        query_id = {
            "symbol": symbol_info['symbol'],
            'market': symbol_info['market']
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
                    symbol_info['symbol'],
                    Bitmex2QA_FREQUENCY_DICT['1d'],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )
        else:
            start_time = symbol_info.get('listing', "2018-01-01T00:00:00Z")
            start_time = parse(start_time)
            QA_util_log_info(
                'NEW_SYMBOL "{}" Trying downloading "{}" from {} to {}'.format(
                    symbol_info['symbol'],
                    Bitmex2QA_FREQUENCY_DICT['1d'],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )

        data = QA_fetch_bitmex_kline(
            symbol_info['symbol'],
            start_time,
            end,
            frequency='1d'
        )
        if data is None:
            QA_util_log_info(
                'SYMBOL "{}" from {} to {} has no data'.format(
                    symbol_info['symbol'],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )
            continue
        QA_util_log_info(
            'SYMBOL {} Recived {} from "{}" to {} in total {} klines'.format(
                Bitmex2QA_FREQUENCY_DICT['1d'],
                symbol_info['symbol'],
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(data[0]['date_stamp'])
                ),
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(data[-1]['date_stamp'])
                ),
                len(data)
            )
        )
        col.insert_many(data)
    QA_util_log_info(
        'DOWNLOAD PROGRESS of day Klines from bitmex accomplished '
    )


def QA_SU_save_bitmex_min(
    frequency='1m',
    client=DATABASE,
):
    """
    获取 bitmex K线 分钟线数据，统一转化字段保存数据为 crypto_asset_min issue：已知问题：目前测试无法获得 bitmex K线 分钟线数据
    """
    symbol_list = QA_fetch_crypto_asset_list(market='bitmex')
    col = client.crypto_asset_min
    col.create_index(
        [
            ('market',
             pymongo.ASCENDING),
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
            ('market',
             pymongo.ASCENDING),
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

    QA_util_log_info('Starting DOWNLOAD PROGRESS of min Klines from bitmex... ')
    for index in range(len(symbol_list)):
        symbol_info = symbol_list.iloc[index]
        QA_util_log_info(
            'The "{}" #{} of total in {}'.format(
                symbol_info['symbol'],
                index,
                len(symbol_list)
            )
        )
        QA_util_log_info(
            'DOWNLOAD PROGRESS {} '
            .format(str(float(index / len(symbol_list) * 100))[0:4] + '%')
        )
        query_id = {
            "symbol": symbol_info['symbol'],
            'market': symbol_info['market'],
            'type': Bitmex2QA_FREQUENCY_DICT[frequency]
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
                    symbol_info['symbol'],
                    Bitmex2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )
        else:
            start_time = symbol_info.get('listing', "2018-01-01T00:00:00Z")
            start_time = parse(start_time)
            QA_util_log_info(
                'NEW_SYMBOL "{}" Trying downloading "{}" from {} to {}'.format(
                    symbol_info['symbol'],
                    Bitmex2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )

        data = QA_fetch_bitmex_kline(
            symbol_info['symbol'],
            start_time,
            end,
            frequency
        )
        if data is None:
            QA_util_log_info(
                'SYMBOL "{}" from {} to {} has no data'.format(
                    symbol_info['symbol'],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                )
            )
            continue
        QA_util_log_info(
            'SYMBOL {} Recived "{}" from {} to {} in total {} klines'.format(
                Bitmex2QA_FREQUENCY_DICT[frequency],
                symbol_info['symbol'],
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(data[0]['time_stamp'])
                ),
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(data[-1]['time_stamp'])
                ),
                len(data)
            )
        )
        col.insert_many(data)
    QA_util_log_info(
        'DOWNLOAD PROGRESS of min Klines from bitmex accomplished '
    )


def QA_SU_save_bitmex_1min():
    QA_SU_save_bitmex_min(frequency='1m')


def QA_SU_save_bitmex_1day():
    QA_SU_save_bitmex_day()


def QA_SU_save_bitmex_1hour():
    QA_SU_save_bitmex_min(frequency="1h")


def QA_SU_get_bitmex_symbol(
    market="bitmex",
    client=DATABASE,
):
    """
    返回 bitmex 交易对信息
    """


def QA_SU_save_bitmex_symbol(
    market="bitmex",
    client=DATABASE,
):
    """
    保存 bitmex 交易对信息
    """
    QA_util_log_info('Downloading {:s} symbol list...'.format(market))

    # 保存 bitmex API 原始 Symbol 数据备查阅，自动交易用得着
    raw_symbol_lists = QA_util_save_raw_symbols(QA_fetch_bitmex_symbols, market)

    if (len(raw_symbol_lists) > 0):
        # 保存到 QUANTAXIS.crypto_asset_list 数字资产列表，为了跨市场统一查询做数据汇总
        symbol_lists = pd.DataFrame(raw_symbol_lists)

        # market,symbol为 mongodb 索引字段，保存之前必须要检查存在
        symbol_lists['market'] = market
        symbol_lists['category'] = symbol_lists['typ']
        symbol_lists.rename(
            {
                'rootSymbol': 'base_currency',
                'quoteCurrency': 'quote_currency',
            },
            axis=1,
            inplace=True
        )
        symbol_lists['price_precision'] = symbol_lists.apply(
            lambda x: 2 + -1 * int(math.log10(float(x.maintMargin))),
            axis=1
        )
        symbol_lists['name'] = symbol_lists['symbol']
        symbol_lists['desc'] = ''

        # 移除非共性字段，这些字段只有 broker 才关心，做对应交易所 broker 接口的时候在交易所 raw_symbol_lists
        # 数据中读取。
        symbol_lists = symbol_lists[[
            'symbol',
            'name',
            'market',
            'state',
            'category',
            'base_currency',
            'quote_currency',
            'price_precision',
            'desc'
        ]]
        symbol_lists['created_at'] = int(
            time.mktime(datetime.datetime.now().utctimetuple())
        )
        symbol_lists['updated_at'] = int(
            time.mktime(datetime.datetime.now().utctimetuple())
        )

        coll_crypto_asset_list = client.crypto_asset_list
        coll_crypto_asset_list.create_index(
            [('market',
              pymongo.ASCENDING),
             ('symbol',
              pymongo.ASCENDING)],
            unique=True
        )
        try:
            query_id = {'market': market}
            if (coll_crypto_asset_list.count_documents(query_id) > 0):
                # 删掉重复数据
                query_id = {
                    'market': market,
                    'symbol': {
                        '$in': symbol_lists['symbol'].tolist()
                    }
                }
                coll_crypto_asset_list.delete_many(query_id)
            coll_crypto_asset_list.insert_many(
                QA_util_to_json_from_pandas(symbol_lists)
            )
            return symbol_lists
        except:
            print(
                'QA_SU_save_bitmex_symbol(): Insert_many(symbol) to "crypto_asset_list" got Exception {}'
                .format(len(data))
            )
            pass
        return []


if __name__ == '__main__':
    QA_SU_save_bitmex_symbol()
    QA_SU_save_bitmex_1day()
    QA_SU_save_bitmex_1hour()
