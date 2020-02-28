# coding: utf-8
# Author: Will
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
from QUANTAXIS.QAFetch.QAbinance import (
    QA_fetch_binance_symbols,
    QA_fetch_binance_kline,
    Binance2QA_FREQUENCY_DICT
)
from QUANTAXIS.QAUtil.QAcrypto import QA_util_save_raw_symbols
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_crypto_asset_list)

import pymongo

# binance的历史数据只是从2017年7月开始有，以前的貌似都没有保留 .  author:Will
BINANCE_MIN_DATE = datetime.datetime(2017, 7, 1, tzinfo=tzutc())


def QA_SU_save_binance(frequency):
    """
    Save binance kline "smart"
    """
    if (frequency not in ["1d", "1day", "day"]):
        return QA_SU_save_binance_min(frequency)
    else:
        return QA_SU_save_binance_day(frequency)


def QA_SU_save_binance_day(frequency, ui_log=None, ui_progress=None):
    """
    Save binance day kline
    """
    market = 'binance'
    symbol_list = QA_fetch_crypto_asset_list(market='binance')
    col = DATABASE.crypto_asset_day
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

    QA_util_log_info(
        'Starting DOWNLOAD PROGRESS of day Klines from binance... ',
        ui_log=ui_log,
        ui_progress=ui_progress
    )
    for index in range(len(symbol_list)):
        symbol_info = symbol_list.iloc[index]
        # 上架仅处理交易对
        QA_util_log_info(
            'The "{}" #{} of total in {}'.format(
                symbol_info['symbol'],
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
        query_id = {"symbol": symbol_info['symbol'], 'market': market}
        ref = col.find(query_id).sort('time_stamp', -1)

        if (col.count_documents(query_id) > 0):
            start_stamp = ref.next()['date_stamp']
            start_time = datetime.datetime.fromtimestamp(start_stamp)
            QA_util_log_info(
                'UPDATE_SYMBOL "{}" Trying updating "{}" from {} to {}'.format(
                    symbol_info['symbol'],
                    Binance2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
        else:
            start_time = BINANCE_MIN_DATE
            QA_util_log_info(
                'NEW_SYMBOL "{}" Trying downloading "{}" from {} to {}'.format(
                    symbol_info['symbol'],
                    Binance2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )

        data = QA_fetch_binance_kline(
            symbol_info['symbol'],
            time.mktime(start_time.utctimetuple()),
            time.mktime(end.utctimetuple()),
            frequency
        )
        if data is None:
            QA_util_log_info(
                'SYMBOL "{}" from {} to {} has no data'.format(
                    symbol_info['symbol'],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
            continue
        QA_util_log_info(
            'SYMBOL "{}" Recived "{}" from {} to {} in total {} klines'.format(
                symbol_info['symbol'],
                Binance2QA_FREQUENCY_DICT[frequency],
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
        query_id = {
            "symbol": symbol_info['symbol'],
            'market': market,
            'date_stamp': {
                '$in': list(map(lambda x: x['date_stamp'],
                                data))
            }
        }
        if (symbol_info['symbol'] == 'LRCETH'):
            #print(len(data)) # To do: 这个会抛出异常，有空再解决
            pass
        if (col.count_documents(query_id) > 0):
            # 删掉重复数据
            col.delete_many(query_id)
        try:
            col.insert_many(data)
        except:
            QA_util_log_expection(
                'QA_SU_save_binance_day():Insert_many(kline) to {} got Exception {}'
                .format(symbol_info['symbol'],
                        len(data))
            )
            pass
    QA_util_log_info(
        'DOWNLOAD PROGRESS of day Klines from binance accomplished.',
        ui_log=ui_log,
        ui_progress=ui_progress
    )


def QA_SU_save_binance_min(frequency, ui_log=None, ui_progress=None):
    """
    Save binance min kline
    """
    market = 'binance'
    symbol_list = QA_fetch_crypto_asset_list(market='binance')
    col = DATABASE.crypto_asset_min
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

    QA_util_log_info(
        'Starting DOWNLOAD PROGRESS of min Klines from binance... ',
        ui_log=ui_log,
        ui_progress=ui_progress
    )
    for index in range(len(symbol_list)):
        symbol_info = symbol_list.iloc[index]
        # 上架仅处理交易对
        QA_util_log_info(
            'The "{}" #{} of total in {}'.format(
                symbol_info['symbol'],
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
            "symbol": symbol_info['symbol'],
            'market': market,
            'type': Binance2QA_FREQUENCY_DICT[frequency]
        }
        ref = col.find(query_id).sort('time_stamp', -1)

        if (col.count_documents(query_id) > 0):
            start_stamp = ref.next()['time_stamp']
            start_time = datetime.datetime.fromtimestamp(start_stamp)
            QA_util_log_info(
                'UPDATE_SYMBOL "{}" Trying updating "{}" from {} to {}'.format(
                    symbol_info['symbol'],
                    Binance2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )
        else:
            start_time = BINANCE_MIN_DATE
            QA_util_log_info(
                'NEW_SYMBOL "{}" Trying downloading "{}" from {} to {}'.format(
                    symbol_info['symbol'],
                    Binance2QA_FREQUENCY_DICT[frequency],
                    QA_util_timestamp_to_str(start_time),
                    QA_util_timestamp_to_str(end)
                ),
                ui_log=ui_log,
                ui_progress=ui_progress
            )

        data = QA_fetch_binance_kline(
            symbol_info['symbol'],
            time.mktime(start_time.utctimetuple()),
            time.mktime(end.utctimetuple()),
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
            'SYMBOL "{}" Recived "{}" from {} to {} in total {} klines'.format(
                symbol_info['symbol'],
                Binance2QA_FREQUENCY_DICT[frequency],
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(data[0]['time_stamp'])
                ),
                time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(data[-1]['time_stamp'])
                ),
                len(data)
            ),
            ui_log=ui_log,
            ui_progress=ui_progress
        )
        query_id = {
            "symbol": symbol_info['symbol'],
            'market': market,
            'type': Binance2QA_FREQUENCY_DICT[frequency],
            'time_stamp': {
                '$in': list(map(lambda x: x['time_stamp'],
                                data))
            }
        }
        if (col.count_documents(query_id) > 0):
            # 删掉重复数据
            col.delete_many(query_id)
        try:
            col.insert_many(data)
        except:
            QA_util_log_expection(
                'QA_SU_save_binance_min():Insert_many(kline) to {} got Exception {}'
                .format(symbol_info['symbol'],
                        len(data))
            )
            pass
    QA_util_log_info(
        'DOWNLOAD PROGRESS of min Klines from binance accomplished.',
        ui_log=ui_log,
        ui_progress=ui_progress
    )


def QA_SU_save_binance_1min():
    QA_SU_save_binance('1m')


def QA_SU_save_binance_1day():
    QA_SU_save_binance("1d")


def QA_SU_save_binance_1hour():
    QA_SU_save_binance("1h")


def QA_SU_save_binance_symbol(client=DATABASE, market="binance"):
    """
    保存币安交易对信息
    """
    QA_util_log_info('Downloading {:s} symbol list...'.format(market))

    # 保存 Binance API 原始 Symbol 数据备查阅，自动交易用得着
    raw_symbol_lists = QA_util_save_raw_symbols(
        QA_fetch_binance_symbols,
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
                'baseAssetPrecision': 'price_precision',
                'baseAsset': 'base_currency',
                'quoteAsset': 'quote_currency',
                'status': 'state',
            },
            axis=1,
            inplace=True
        )
        symbol_lists['name'] = symbol_lists.apply(
            lambda x: '{:s}/{:s}'.
            format(x['base_currency'].upper(),
                   x['quote_currency'].upper()),
            axis=1
        )
        symbol_lists['desc'] = symbol_lists['name']
        symbol_lists['created_at'] = int(
            time.mktime(datetime.datetime.now().utctimetuple())
        )
        symbol_lists['updated_at'] = int(
            time.mktime(datetime.datetime.now().utctimetuple())
        )

        # 移除非共性字段，这些字段只有 broker 才关心，做对应交易所 broker 接口的时候在交易所 raw_symbol_lists
        # 数据中读取。
        symbol_lists.drop(
            [
                '_id',
                'baseCommissionPrecision',
                'quotePrecision',
                'filters',
                'icebergAllowed',
                'isMarginTradingAllowed',
                'isSpotTradingAllowed',
                'ocoAllowed',
                'orderTypes',
                'quoteCommissionPrecision',
                'quoteOrderQtyMarketAllowed',
            ],
            axis=1,
            inplace=True
        )

        # 删除不交易的交易对
        symbol_lists = symbol_lists[symbol_lists['state'].isin(['TRADING'])]

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
            QA_util_log_expection(
                'QA_SU_save_binance_symbol: Insert_many(symbol) to "crypto_asset_list" got Exception {}'
                .format(len(data))
            )
            pass
        return []


if __name__ == '__main__':
    QA_SU_save_binance_symbol()
    #QA_SU_save_binance_1day()
    #QA_SU_save_binance_1hour()
