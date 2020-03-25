from QUANTAXIS.QAUtil import (QASETTING, DATABASE, QA_util_log_info)
from QUANTAXIS.QAUtil.QAParameter import (FREQUENCE)
import pandas as pd
from datetime import datetime
import time
from dateutil.tz import tzutc
import pymongo

from QUANTAXIS.QAUtil.QADate_Adv import (
    QA_util_str_to_Unix_timestamp,
    QA_util_datetime_to_Unix_timestamp,
    QA_util_timestamp_to_str,
    QA_util_print_timestamp
)


def QA_util_save_raw_symbols(fetch_symnol_func, exchange):
    """
    explanation:
        保存获取的代码列表
    
    params:
        * fetch_symnol_func->
            含义: 获取代码列表的函数对象,注意这是一个函数对象,而不是函数运行的实体
            类型: func
            参数支持: []
        * exchange:
            含义: 交易所代码
            类型: str
            参数支持: []
    """
    symbols = fetch_symnol_func()
    col = QASETTING.client[exchange].symbols
    if col.find().count() == len(symbols):
        QA_util_log_info(
            "{} SYMBOLS are already existed and no more to update"
            .format(exchange)
        )
    else:
        #if ('_id' in symbols):
        #    # 有时有，必须单独删除
        #    symbols.drop(
        #        [
        #            '_id',
        #        ],
        #        axis=1,
        #        inplace=True
        #    )
        QA_util_log_info(
            "Delete the original {} symbols collections".format(exchange)
        )
        QASETTING.client.exchange.drop_collection("symbols")
        QA_util_log_info("Downloading the new symbols")
        col.insert_many(symbols)
        QA_util_log_info(
            "{} Symbols download is done! Thank you man!".format(exchange)
        )
    return symbols


def QA_util_find_missing_kline(
    symbol,
    freq,
    start_epoch=datetime(2017,
                         10,
                         1,
                         tzinfo=tzutc()),
    tzlocalize='Asia/Shanghai'
):
    """
    查找24小时不间断的连续交易市场中缺失的 kline 历史数据，生成缺失历史数据时间段
    """
    FREQUENCE_PERIOD_TIME = {
        FREQUENCE.ONE_MIN: 60,
        FREQUENCE.FIVE_MIN: 300,
        FREQUENCE.FIFTEEN_MIN: 900,
        FREQUENCE.THIRTY_MIN: 1800,
        FREQUENCE.SIXTY_MIN: 3600,
        FREQUENCE.HOUR: 3600,
        FREQUENCE.DAY: 86400,
    }

    if (freq != FREQUENCE.DAY):
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
        col.create_index(
            [("type",
              pymongo.ASCENDING),
             ('time_stamp',
              pymongo.ASCENDING)]
        )
        col.create_index([('time_stamp', pymongo.ASCENDING)])

        # 查询历史数据
        query_id = {"symbol": symbol, 'type': freq}
        refcount = col.count_documents(query_id)
        _data = []
        cursor = col.find(query_id).sort('time_stamp', 1)
        for item in cursor:
            _data.append(
                [
                    str(item['symbol']),
                    item['time_stamp'],
                    item['date'],
                    item['datetime'],
                    item['type']
                ]
            )

        _data = pd.DataFrame(
            _data,
            columns=[
                'symbol',
                'time_stamp',
                'date',
                'datetime',
                'type'
            ]
        )
        _data = _data.set_index(pd.DatetimeIndex(_data['datetime']), drop=False)
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
        query_id = {"symbol": symbol}
        refcount = col.count_documents(query_id)
        cursor = col.find(query_id).sort('time_stamp', 1)
        _data = []
        for item in cursor:
            _data.append(
                [
                    str(item['symbol']),
                    item['time_stamp'],
                    item['date'],
                    item['datetime']
                ]
            )

        _data = pd.DataFrame(
            _data,
            columns=['symbol',
                     'time_stamp',
                     'date',
                     'datetime']
        ).drop_duplicates()
        _data['date'] = pd.to_datetime(_data['date'])
        _data = _data.set_index(pd.DatetimeIndex(_data['date']), drop=False)

    if (freq != FREQUENCE.DAY):
        # cryptocurrency_min 中的 Date/Datetime 字段均为北京时间
        leak_datetime = pd.date_range(
            _data.index.min(),
            _data.index.max(),
            freq=freq
        ).difference(_data.index).tz_localize(tzlocalize)
        if (int(_data.iloc[0].time_stamp) >
            (QA_util_datetime_to_Unix_timestamp() + 120)):
            # 出现“未来”时间，一般是默认时区设置错误造成的
            raise Exception(
                'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                .format(
                    symbol,
                    freq,
                    QA_util_print_timestamp(_data.iloc[0].time_stamp),
                    QA_util_print_timestamp(
                        QA_util_datetime_to_Unix_timestamp()
                    )
                )
            )
    else:
        leak_datetime = pd.date_range(
            _data.index.min(),
            _data.index.max(),
            freq='1D'
        ).difference(_data.index).tz_localize(tzlocalize)

    if (int(time.mktime(start_epoch.utctimetuple())) > int(
            _data.iloc[0].time_stamp)):
        miss_kline = pd.DataFrame(columns=['expected', 'between', 'missing'])
    else:
        miss_kline = pd.DataFrame(
            [
                [
                    int(time.mktime(start_epoch.utctimetuple())),
                    int(_data.iloc[0].time_stamp),
                    '{} to {}'.format(start_epoch,
                                     _data.iloc[0].date)
                ]
            ],
            columns=['expected',
                     'between',
                     'missing']
        )

    expected = None
    for x in range(0, len(leak_datetime)):
        if (expected is None):
            expected = int(leak_datetime[x].timestamp())

        if ((expected is not None) and (x > 1) and (int(leak_datetime[x].timestamp()) != int(leak_datetime[x - 1].timestamp() + FREQUENCE_PERIOD_TIME[freq]))) or \
            ((expected is not None) and (x > 1) and (x == len(leak_datetime) - 1)):
            between = int(
                leak_datetime[x - 1].timestamp() + FREQUENCE_PERIOD_TIME[freq]
            )
            miss_kline = miss_kline.append(
                {
                    'expected':
                        int(expected),
                    'between':
                        int(between),
                    'missing':
                        '{} to {}'.format(
                            pd.to_datetime(expected,
                                           unit='s'
                                          ).tz_localize('Asia/Shanghai'),
                            pd.to_datetime(between,
                                           unit='s'
                                          ).tz_localize('Asia/Shanghai')
                        )
                },
                ignore_index=True
            )
            expected = int(leak_datetime[x].timestamp())

    if (int(_data.iloc[-1].time_stamp) + 1 < int(
            QA_util_datetime_to_Unix_timestamp())):
        miss_kline = miss_kline.append(
            {
                'expected':
                    int(_data.iloc[-1].time_stamp) + 1,
                'between':
                    int(QA_util_datetime_to_Unix_timestamp()),
                'missing':
                    '{} to {}'.format(
                        int(_data.iloc[0].time_stamp) + 1,
                        QA_util_datetime_to_Unix_timestamp()
                    )
            },
            ignore_index=True
        )
    miss_kline.sort_values(by='expected', ascending=True, inplace=True)
    if (len(miss_kline) > 0):
        if (miss_kline.iloc[0].expected > QA_util_datetime_to_Unix_timestamp()) and \
            (miss_kline.iloc[0].between > QA_util_datetime_to_Unix_timestamp()):
            miss_kline.drop(miss_kline.iloc[0], inplace=True)
    return miss_kline.values


if __name__ == '__main__':
    print(QA_util_find_missing_kline('btcusdt', FREQUENCE.ONE_MIN))
