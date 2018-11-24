import datetime
import time
from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta
from QUANTAXIS.QAUtil import (QASETTING, QA_util_log_info)

from QUANTAXIS.QAFetch.QAbinance import QA_fetch_binance_symbols, QA_fetch_binance_kline
from QUANTAXIS.QAUtil.QAcrypto import QA_SU_save_symbols
import pymongo

# binance的历史数据只是从2017年7月开始有，以前的貌似都没有保留 . author:Will
BINANCE_MIN_DATE = datetime.datetime(2017, 7, 1, tzinfo=tzutc())

FREQUANCY_DICT = {
    "1m": relativedelta(minutes=-1),
    "1d": relativedelta(days=-1),
    "1h": relativedelta(hours=-1)
}


def QA_SU_save_binance(frequency):
    symbol_list = QA_fetch_binance_symbols()
    col = QASETTING.client.binance[frequency]
    col.create_index(
        [("symbol", pymongo.ASCENDING), ("start_time", pymongo.ASCENDING)], unique=True)

    end = datetime.datetime.now(tzutc()) + relativedelta(days=-1, hour=0, minute=0, second=0, microsecond=0)

    for index, symbol_info in enumerate(symbol_list):
        QA_util_log_info('The {} of Total {}'.format
                         (symbol_info['symbol'], len(symbol_list)))
        QA_util_log_info('DOWNLOAD PROGRESS {} '.format(str(
            float(index / len(symbol_list) * 100))[0:4] + '%')
                         )
        ref = col.find({"symbol": symbol_info['symbol']}).sort("start_time", -1)

        if ref.count() > 0:
            start_stamp = ref.next()['close_time'] / 1000
            start_time = datetime.datetime.fromtimestamp(start_stamp)
            QA_util_log_info('UPDATE_SYMBOL {} Trying updating {} from {} to {}'.format(
                frequency, symbol_info['symbol'], start_time, end))
        else:
            start_time = BINANCE_MIN_DATE
            QA_util_log_info('NEW_SYMBOL {} Trying downloading {} from {} to {}'.format(
                frequency, symbol_info['symbol'], start_time, end))

        data = QA_fetch_binance_kline(symbol_info['symbol'],
                                      time.mktime(start_time.utctimetuple()), time.mktime(end.utctimetuple()), frequency)
        if data is None:
            QA_util_log_info('SYMBOL {} from {} to {} has no data'.format(
                symbol_info['symbol'], start_time, end))
            continue
        col.insert_many(data)


def QA_SU_save_binance_1min():
    QA_SU_save_binance('1m')


def QA_SU_save_binance_1day():
    QA_SU_save_binance("1d")


def QA_SU_save_binance_1hour():
    QA_SU_save_binance("1h")


def QA_SU_save_binance_symbol():
    QA_SU_save_symbols(QA_fetch_binance_symbols, "binance")


if __name__ == '__main__':
    QA_SU_save_binance_symbol()
