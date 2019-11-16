# coding: utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2019 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import datetime

import numpy
import pandas as pd
from pandas import DataFrame

from QUANTAXIS.QAUtil import (DATABASE, QA_Setting, QA_util_date_stamp,
                              QA_util_date_valid, QA_util_dict_remove_key,
                              QA_util_log_info, QA_util_code_tolist, QA_util_date_str2int, QA_util_date_int2str,
                              QA_util_sql_mongo_sort_DESCENDING,
                              QA_util_time_stamp, QA_util_to_json_from_pandas,
                              trade_date_sse)
from QUANTAXIS.QAData.financial_mean import financial_dict

"""
按要求从数据库取数据，并转换成numpy结构

2018-07-30 修改 增加batch_size  可以做到8MB/S-30mb/s的传输速度

"""


def QA_fetch_stock_day(code, start, end, format='numpy', frequence='day', collections=DATABASE.stock_day):
    """'获取股票日线'

    Returns:
        [type] -- [description]

        感谢@几何大佬的提示
        https://docs.mongodb.com/manual/tutorial/project-fields-from-query-results/#return-the-specified-fields-and-the-id-field-only

    """

    start = str(start)[0:10]
    end = str(end)[0:10]
    #code= [code] if isinstance(code,str) else code

    # code checking
    code = QA_util_code_tolist(code)

    if QA_util_date_valid(end):

        cursor = collections.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0}, batch_size=10000)
        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.assign(volume=res.vol, date=pd.to_datetime(
                res.date)).drop_duplicates((['date', 'code'])).query('volume>1').set_index('date', drop=False)
            res = res.loc[:, ['code', 'open', 'high', 'low',
                             'close', 'volume', 'amount', 'date']]
        except:
            res = None
        if format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif format in ['json', 'dict']:
            return QA_util_to_json_from_pandas(res)
        # 多种数据格式
        elif format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print("QA Error QA_fetch_stock_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        QA_util_log_info(
            'QA Error QA_fetch_stock_day data parameter start=%s end=%s is not right' % (start, end))


def QA_fetch_stock_min(code, start, end, format='numpy', frequence='1min', collections=DATABASE.stock_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    else:
        print("QA Error QA_fetch_stock_min parameter frequence=%s is none of 1min 1m 5min 5m 15min 15m 30min 30m 60min 60m" % frequence)

    _data = []
    # code checking
    code = QA_util_code_tolist(code)

    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    }, {"_id": 0}, batch_size=10000)

    res = pd.DataFrame([item for item in cursor])
    try:
        res = res.assign(volume=res.vol, datetime=pd.to_datetime(
            res.datetime)).query('volume>1').drop_duplicates(['datetime', 'code']).set_index('datetime', drop=False)
        # return res
    except:
        res = None
    if format in ['P', 'p', 'pandas', 'pd']:
        return res
    elif format in ['json', 'dict']:
        return QA_util_to_json_from_pandas(res)
    # 多种数据格式
    elif format in ['n', 'N', 'numpy']:
        return numpy.asarray(res)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(res).tolist()
    else:
        print("QA Error QA_fetch_stock_min format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
        return None


def QA_fetch_stock_transaction(code, start, end, format='numpy', frequence='tick', collections=DATABASE.stock_transaction):
    '获取股票分钟线'
    if frequence in ['tick', 'TICK', 'transaction']:
        frequence = 'tick'
    else:
        print("QA Error QA_fetch_stock_transaction parameter frequence=%s is none of tick Tick transaction" % frequence)

    _data = []
    # code checking
    code = QA_util_code_tolist(code)

    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, "type": frequence
    }, {"_id": 0}, batch_size=10000)

    res = pd.DataFrame([item for item in cursor])
    try:
        res = res.assign(volume=res.vol, datetime=pd.to_datetime(
            res.datetime)).query('volume>1').drop_duplicates(['datetime', 'code']).set_index('datetime', drop=False)
        # return res
    except:
        res = None
    if format in ['P', 'p', 'pandas', 'pd']:
        return res
    elif format in ['json', 'dict']:
        return QA_util_to_json_from_pandas(res)
    # 多种数据格式
    elif format in ['n', 'N', 'numpy']:
        return numpy.asarray(res)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(res).tolist()
    else:
        print("QA Error QA_fetch_stock_transaction format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
        return None

def QA_fetch_index_transaction(code, start, end, format='numpy', frequence='tick', collections=DATABASE.index_transaction):
    '获取股票分钟线'
    if frequence in ['tick', 'TICK', 'transaction']:
        frequence = 'tick'
    else:
        print("QA Error QA_fetch_index_transaction parameter frequence=%s is none of tick Tick transaction" % frequence)

    _data = []
    # code checking
    code = QA_util_code_tolist(code)

    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    }, {"_id": 0}, batch_size=10000)

    res = pd.DataFrame([item for item in cursor])
    try:
        res = res.assign(volume=res.vol, datetime=pd.to_datetime(
            res.datetime)).query('volume>1').drop_duplicates(['datetime', 'code']).set_index('datetime', drop=False)
        # return res
    except:
        res = None
    if format in ['P', 'p', 'pandas', 'pd']:
        return res
    elif format in ['json', 'dict']:
        return QA_util_to_json_from_pandas(res)
    # 多种数据格式
    elif format in ['n', 'N', 'numpy']:
        return numpy.asarray(res)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(res).tolist()
    else:
        print("QA Error QA_fetch_index_transaction format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
        return None


def QA_fetch_trade_date():
    '获取交易日期'
    return trade_date_sse


def QA_fetch_stock_list(collections=DATABASE.stock_list):
    '获取股票列表'

    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False).set_index('code', drop=False)


def QA_fetch_etf_list(collections=DATABASE.etf_list):
    '获取ETF列表'

    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False).set_index('code', drop=False)


def QA_fetch_index_list(collections=DATABASE.index_list):
    '获取指数列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False).set_index('code', drop=False)


def QA_fetch_stock_terminated(collections=DATABASE.stock_terminated):
    '获取股票基本信息 , 已经退市的股票列表'
    # 🛠todo  转变成 dataframe 类型数据
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False).set_index('code', drop=False)


def QA_fetch_stock_basic_info_tushare(collections=DATABASE.stock_info_tushare):
    '''
    purpose:
        tushare 股票列表数据库

        code,代码
        name,名称
        industry,所属行业
        area,地区
        pe,市盈率
        outstanding,流通股本(亿)
        totals,总股本(亿)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        esp,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
        undp,未分利润
        perundp, 每股未分配
        rev,收入同比(%)
        profit,利润同比(%)
        gpr,毛利率(%)
        npr,净利润率(%)
        holders,股东人数

        add by tauruswang,

    :param collections: stock_info_tushare 集合
    :return:
    '''
    '获取股票基本信息'
    items = [item for item in collections.find()]
    # 🛠todo  转变成 dataframe 类型数据
    return items


def QA_fetch_stock_to_market_date(stock_code):
    '''
    根据tushare 的数据库查找上市的日期
    :param stock_code: '600001'
    :return: string 上市日期 eg： '2018-05-15'
    '''
    items = QA_fetch_stock_basic_info_tushare()
    for row in items:
        if row['code'] == stock_code:
            return row['timeToMarket']


def QA_fetch_stock_full(date, format='numpy', collections=DATABASE.stock_day):
    '获取全市场的某一日的数据'
    Date = str(date)[0:10]
    if QA_util_date_valid(Date) is True:

        _data = []
        for item in collections.find({
                "date_stamp": QA_util_date_stamp(Date)}, batch_size=10000):
            _data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['vol']), item['date']])
        # 多种数据格式
        if format in ['n', 'N', 'numpy']:
            _data = numpy.asarray(_data)
        elif format in ['list', 'l', 'L']:
            _data = _data
        elif format in ['P', 'p', 'pandas', 'pd']:
            _data = DataFrame(_data, columns=[
                'code', 'open', 'high', 'low', 'close', 'volume', 'date'])
            _data['date'] = pd.to_datetime(_data['date'])
            _data = _data.set_index('date', drop=False)
        else:
            print("QA Error QA_fetch_stock_full format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)

        return _data
    else:
        QA_util_log_info(
            'QA Error QA_fetch_stock_full data parameter date=%s not right' % date)


def QA_fetch_index_day(code, start, end, format='numpy', collections=DATABASE.index_day):
    '获取指数日线'
    start = str(start)[0:10]
    end = str(end)[0:10]
    code = QA_util_code_tolist(code)
    if QA_util_date_valid(end) == True:

        cursor = collections.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0}, batch_size=10000)

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.assign(volume=res.vol, date=pd.to_datetime(
                res.date)).drop_duplicates((['date', 'code'])).set_index('date', drop=False)
        except:
            res = None

        if format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif format in ['json', 'dict']:
            return QA_util_to_json_from_pandas(res)
        # 多种数据格式
        elif format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print("QA Error QA_fetch_index_day format parameter %s is none of  \"P, p, pandas, pd , n, N, numpy !\" " % format)
            return None
    else:
        QA_util_log_info(
            'QA Error QA_fetch_index_day data parameter start=%s end=%s is not right' % (start, end))


def QA_fetch_index_min(
        code,
        start, end,
        format='numpy',
        frequence='1min',
        collections=DATABASE.index_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    _data = []
    code = QA_util_code_tolist(code)
    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    }, {"_id": 0}, batch_size=10000)
    if format in ['dict', 'json']:
        return [data for data in cursor]
    # for item in cursor:
    _data = pd.DataFrame([item for item in cursor])
    _data = _data.assign(datetime=pd.to_datetime(_data['datetime']))
    # _data.append([str(item['code']), float(item['open']), float(item['high']), float(
    #     item['low']), float(item['close']), int(item['up_count']), int(item['down_count']), float(item['vol']), float(item['amount']), item['datetime'], item['time_stamp'], item['date'], item['type']])

    # _data = DataFrame(_data, columns=[
    #     'code', 'open', 'high', 'low', 'close', 'up_count', 'down_count', 'volume', 'amount', 'datetime', 'time_stamp', 'date', 'type'])

    # _data['datetime'] = pd.to_datetime(_data['datetime'])
    _data = _data.set_index('datetime', drop=False)
    if format in ['numpy', 'np', 'n']:
        return numpy.asarray(_data)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(_data).tolist()
    elif format in ['P', 'p', 'pandas', 'pd']:
        return _data


def QA_fetch_future_day(code, start, end, format='numpy', collections=DATABASE.future_day):
    start = str(start)[0:10]
    end = str(end)[0:10]
    code = QA_util_code_tolist(code, auto_fill=False)

    if QA_util_date_valid(end) == True:

        _data = []
        cursor = collections.find({
            'code': {'$in': code}, "date_stamp": {
                "$lte": QA_util_date_stamp(end),
                "$gte": QA_util_date_stamp(start)}}, {"_id": 0}, batch_size=10000)
        if format in ['dict', 'json']:
            return [data for data in cursor]
        for item in cursor:

            _data.append([str(item['code']), float(item['open']), float(item['high']), float(
                item['low']), float(item['close']), float(item['position']), float(item['price']), float(item['trade']), item['date']])

        # 多种数据格式
        if format in ['n', 'N', 'numpy']:
            _data = numpy.asarray(_data)
        elif format in ['list', 'l', 'L']:
            _data = _data
        elif format in ['P', 'p', 'pandas', 'pd']:
            _data = DataFrame(
                _data, columns=['code', 'open', 'high', 'low', 'close', 'position', 'price', 'trade', 'date']).drop_duplicates()
            _data['date'] = pd.to_datetime(_data['date'])
            _data = _data.set_index('date', drop=False)
        else:
            print("QA Error QA_fetch_future_day format parameter %s is none of  \"P, p, pandas, pd , n, N, numpy !\" " % format)
        return _data
    else:
        QA_util_log_info('QA something wrong with date')


def QA_fetch_future_min(
        code,
        start, end,
        format='numpy',
        frequence='1min',
        collections=DATABASE.future_min):
    '获取股票分钟线'
    if frequence in ['1min', '1m']:
        frequence = '1min'
    elif frequence in ['5min', '5m']:
        frequence = '5min'
    elif frequence in ['15min', '15m']:
        frequence = '15min'
    elif frequence in ['30min', '30m']:
        frequence = '30min'
    elif frequence in ['60min', '60m']:
        frequence = '60min'
    _data = []
    code = QA_util_code_tolist(code, auto_fill=False)
    cursor = collections.find({
        'code': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    }, batch_size=10000)
    if format in ['dict', 'json']:
        return [data for data in cursor]
    for item in cursor:

        _data.append([str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item.get('position', 0)), float(item.get('price', 0)), float(item.get('trade', item.get('volume', 0))),
            item['datetime'], item['tradetime'], item['time_stamp'], item['date'], item['type']])

    _data = DataFrame(_data, columns=[
        'code', 'open', 'high', 'low', 'close',  'position', 'price', 'trade', 'datetime', 'tradetime', 'time_stamp', 'date', 'type'])
    _data = _data.assign(datetime=pd.to_datetime(_data['datetime'])).drop_duplicates(
        (['datetime', 'code'])).set_index('datetime', drop=False)

    if format in ['numpy', 'np', 'n']:
        return numpy.asarray(_data)
    elif format in ['list', 'l', 'L']:
        return numpy.asarray(_data).tolist()
    elif format in ['P', 'p', 'pandas', 'pd']:
        return _data


def QA_fetch_future_list(collections=DATABASE.future_list):
    '获取期货列表'
    return pd.DataFrame([item for item in collections.find()]).drop('_id', axis=1, inplace=False).set_index('code', drop=False)


def QA_fetch_future_tick():
    raise NotImplementedError


def QA_fetch_ctp_tick(code, start, end, frequence, format='pd', collections=DATABASE.ctp_tick):
    """仅供存储的ctp tick使用

    Arguments:
        code {[type]} -- [description]

    Keyword Arguments:
        format {str} -- [description] (default: {'pd'})
        collections {[type]} -- [description] (default: {DATABASE.ctp_tick})

    Returns:
        [type] -- [description]
    """

    code = QA_util_code_tolist(code, auto_fill=False)
    cursor = collections.find({
        'InstrumentID': {'$in': code}, "time_stamp": {
            "$gte": QA_util_time_stamp(start),
            "$lte": QA_util_time_stamp(end)
        }, 'type': frequence
    }, {"_id": 0}, batch_size=10000)

    hq = pd.DataFrame([data for data in cursor]).replace(1.7976931348623157e+308,
                                                         numpy.nan).replace('', numpy.nan).dropna(axis=1)
    p1 = hq.loc[:, ['ActionDay', 'AskPrice1', 'AskVolume1', 'AveragePrice', 'BidPrice1',
                    'BidVolume1', 'HighestPrice', 'InstrumentID', 'LastPrice',
                    'OpenInterest', 'TradingDay', 'UpdateMillisec',
                    'UpdateTime', 'Volume']]
    p1 = p1.assign(datetime=p1.ActionDay.apply(QA_util_date_int2str)+' '+p1.UpdateTime + (p1.UpdateMillisec/1000000).apply(lambda x: str('%.6f' % x)[1:]),
                   code=p1.InstrumentID)
    p1.datetime = pd.to_datetime(p1.datetime)
    return p1.set_index(p1.datetime)


def QA_fetch_stock_xdxr(code, format='pd', collections=DATABASE.stock_xdxr):
    '获取股票除权信息/数据库'
    code = QA_util_code_tolist(code)
    data = pd.DataFrame([item for item in collections.find(
        {'code':  {'$in': code}}, batch_size=10000)]).drop(['_id'], axis=1)
    data['date'] = pd.to_datetime(data['date'])
    return data.set_index('date', drop=False)


def QA_fetch_backtest_info(user=None, account_cookie=None, strategy=None, stock_list=None, collections=DATABASE.backtest_info):

    return QA_util_to_json_from_pandas(pd.DataFrame([item for item in collections.find(QA_util_to_json_from_pandas(pd.DataFrame([user, account_cookie, strategy, stock_list], index=['user', 'account_cookie', 'strategy', 'stock_list']).dropna().T)[0])]).drop(['_id'], axis=1))


def QA_fetch_backtest_history(cookie=None, collections=DATABASE.backtest_history):
    return QA_util_to_json_from_pandas(pd.DataFrame([item for item in collections.find(QA_util_to_json_from_pandas(pd.DataFrame([cookie], index=['cookie']).dropna().T)[0])]).drop(['_id'], axis=1))


def QA_fetch_stock_block(code=None, format='pd', collections=DATABASE.stock_block):
    if code is not None:
        code = QA_util_code_tolist(code)
        data = pd.DataFrame([item for item in collections.find(
            {'code': {'$in': code}}, batch_size=10000)]).drop(['_id'], axis=1)
        return data.set_index('code', drop=False)
    else:
        data = pd.DataFrame(
            [item for item in collections.find()]).drop(['_id'], axis=1)
        return data.set_index('code', drop=False)


def QA_fetch_stock_info(code, format='pd', collections=DATABASE.stock_info):
    code = QA_util_code_tolist(code)
    try:
        data = pd.DataFrame([item for item in collections.find(
            {'code':  {'$in': code}}, {"_id": 0}, batch_size=10000)])
        #data['date'] = pd.to_datetime(data['date'])
        return data.set_index('code', drop=False)
    except Exception as e:
        QA_util_log_info(e)
        return None


def QA_fetch_stock_name(code, collections=DATABASE.stock_list):
    try:
        return collections.find_one({'code': code})['name']
    except Exception as e:
        QA_util_log_info(e)


def QA_fetch_quotation(code, date=datetime.date.today(), db=DATABASE):
    '获取某一只实时5档行情的存储结果'
    try:
        collections = db.get_collection(
            'realtime_{}'.format(date))
        data = pd.DataFrame([item for item in collections.find(
            {'code': code}, {"_id": 0}, batch_size=10000)])
        return data.assign(date=pd.to_datetime(data.datetime.apply(lambda x: str(x)[0:10])), datetime=pd.to_datetime(data.datetime)) \
            .set_index('datetime', drop=False).sort_index()
    except Exception as e:
        raise e


def QA_fetch_quotations(date=datetime.date.today(), db=DATABASE):
    '获取全部实时5档行情的存储结果'
    try:
        collections = db.get_collection(
            'realtime_{}'.format(date))
        data = pd.DataFrame([item for item in collections.find(
            {}, {"_id": 0}, batch_size=10000)])
        return data.assign(date=pd.to_datetime(data.datetime.apply(lambda x: str(x)[0:10]))).assign(datetime=pd.to_datetime(data.datetime)).set_index(['datetime', 'code'], drop=False).sort_index()
    except Exception as e:
        raise e


def QA_fetch_account(message={}, db=DATABASE):
    """get the account

    Arguments:
        query_mes {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})

    Returns:
        [type] -- [description]
    """
    collection = DATABASE.account
    return [res for res in collection.find(message, {"_id": 0})]


def QA_fetch_risk(message={}, params={"_id": 0, 'assets': 0, 'timeindex': 0, 'totaltimeindex': 0, 'benchmark_assets': 0, 'month_profit': 0}, db=DATABASE):
    """get the risk message

    Arguments:
        query_mes {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})

    Returns:
        [type] -- [description]
    """
    collection = DATABASE.risk
    return [res for res in collection.find(message, params)]


def QA_fetch_user(user_cookie, db=DATABASE):
    """
    get the user

    Arguments:
        user_cookie : str the unique cookie_id for a user
    Keyword Arguments:
        db: database for query

    Returns:
        list ---  [ACCOUNT]
    """
    collection = DATABASE.account

    return [res for res in collection.find({'user_cookie': user_cookie}, {"_id": 0})]


def QA_fetch_strategy(message={}, db=DATABASE):
    """get the account

    Arguments:
        query_mes {[type]} -- [description]

    Keyword Arguments:
        collection {[type]} -- [description] (default: {DATABASE})

    Returns:
        [type] -- [description]
    """
    collection = DATABASE.strategy
    return [res for res in collection.find(message, {"_id": 0})]


def QA_fetch_lhb(date, db=DATABASE):
    '获取某一天龙虎榜数据'
    try:
        collections = db.lhb
        return pd.DataFrame([item for item in collections.find(
            {'date': date}, {"_id": 0})]).set_index('code', drop=False).sort_index()
    except Exception as e:
        raise e


# def QA_fetch_financial_report(code, report_date, type ='report', ltype='EN', db=DATABASE):
#     """获取专业财务报表

#     Arguments:
#         code {[type]} -- [description]
#         report_date {[type]} -- [description]

#     Keyword Arguments:
#         ltype {str} -- [description] (default: {'EN'})
#         db {[type]} -- [description] (default: {DATABASE})

#     Raises:
#         e -- [description]

#     Returns:
#         pd.DataFrame -- [description]
#     """

#     if isinstance(code, str):
#         code = [code]
#     if isinstance(report_date, str):
#         report_date = [QA_util_date_str2int(report_date)]
#     elif isinstance(report_date, int):
#         report_date = [report_date]
#     elif isinstance(report_date, list):
#         report_date = [QA_util_date_str2int(item) for item in report_date]

#     collection = db.financial
#     num_columns = [item[:3] for item in list(financial_dict.keys())]
#     CH_columns = [item[3:] for item in list(financial_dict.keys())]
#     EN_columns = list(financial_dict.values())
#     #num_columns.extend(['283', '_id', 'code', 'report_date'])
#    # CH_columns.extend(['283', '_id', 'code', 'report_date'])
#     #CH_columns = pd.Index(CH_columns)
#     #EN_columns = list(financial_dict.values())
#     #EN_columns.extend(['283', '_id', 'code', 'report_date'])
#     #EN_columns = pd.Index(EN_columns)


#     try:
#         if type == 'report':
#             if code is not None and report_date is not None:
#                 data = [item for item in collection.find(
#                     {'code': {'$in': code}, 'report_date': {'$in': report_date}}, batch_size=10000)]
#             elif code is None and report_date is not None:
#                 data = [item for item in collection.find(
#                     {'report_date': {'$in': report_date}}, batch_size=10000)]
#             elif code is not None and report_date is None:
#                 data = [item for item in collection.find(
#                     {'code': {'$in': code}}, batch_size=10000)]
#             else:
#                 data = [item for item in collection.find()]

#         elif type == 'date':
#             if code is not None and report_date is not None:
#                 data = [item for item in collection.find(
#                     {'code': {'$in': code}, 'crawl_date': {'$in': report_date}}, batch_size=10000)]
#             elif code is None and report_date is not None:
#                 data = [item for item in collection.find(
#                     {'crawl_date': {'$in': report_date}}, batch_size=10000)]
#             elif code is not None and report_date is None:
#                 data = [item for item in collection.find(
#                     {'code': {'$in': code}}, batch_size=10000)]
#             else:
#                 data = [item for item in collection.find()]
#         else:
#             print("type must be date or report")

#         if len(data) > 0:
#             res_pd = pd.DataFrame(data)

#             if ltype in ['CH', 'CN']:

#                 cndict = dict(zip(num_columns, CH_columns))
#                 cndict['283']='283'
#                 cndict['_id']='_id'
#                 cndict['code']='code'
#                 cndict['report_date']='report_date'

#                 res_pd.columns = res_pd.columns.map(lambda x: cndict[x])
#             elif ltype is 'EN':
#                 endict=dict(zip(num_columns,EN_columns))
#                 endict['283']='283'
#                 endict['_id']='_id'
#                 endict['code']='code'
#                 endict['report_date']='report_date'

#                 res_pd.columns = res_pd.columns.map(lambda x: endict[x])

#             if res_pd.report_date.dtype == numpy.int64:
#                 res_pd.report_date = pd.to_datetime(
#                     res_pd.report_date.apply(QA_util_date_int2str))
#             else:
#                 res_pd.report_date = pd.to_datetime(res_pd.report_date)

#             return res_pd.replace(-4.039810335e+34, numpy.nan).set_index(['report_date', 'code'], drop=False)
#         else:
#             return None
#     except Exception as e:
#         raise e


def QA_fetch_financial_report(code, report_date, ltype='EN', db=DATABASE):
    """获取专业财务报表
    Arguments:
        code {[type]} -- [description]
        report_date {[type]} -- [description]
    Keyword Arguments:
        ltype {str} -- [description] (default: {'EN'})
        db {[type]} -- [description] (default: {DATABASE})
    Raises:
        e -- [description]
    Returns:
        pd.DataFrame -- [description]
    """

    if isinstance(code, str):
        code = [code]
    if isinstance(report_date, str):
        report_date = [QA_util_date_str2int(report_date)]
    elif isinstance(report_date, int):
        report_date = [report_date]
    elif isinstance(report_date, list):
        report_date = [QA_util_date_str2int(item) for item in report_date]

    collection = db.financial
    num_columns = [item[:3] for item in list(financial_dict.keys())]
    CH_columns = [item[3:] for item in list(financial_dict.keys())]
    EN_columns = list(financial_dict.values())
    #num_columns.extend(['283', '_id', 'code', 'report_date'])
   # CH_columns.extend(['283', '_id', 'code', 'report_date'])
    #CH_columns = pd.Index(CH_columns)
    #EN_columns = list(financial_dict.values())
    #EN_columns.extend(['283', '_id', 'code', 'report_date'])
    #EN_columns = pd.Index(EN_columns)

    try:
        if code is not None and report_date is not None:
            data = [item for item in collection.find(
                {'code': {'$in': code}, 'report_date': {'$in': report_date}}, {"_id": 0}, batch_size=10000)]
        elif code is None and report_date is not None:
            data = [item for item in collection.find(
                {'report_date': {'$in': report_date}}, {"_id": 0}, batch_size=10000)]
        elif code is not None and report_date is None:
            data = [item for item in collection.find(
                {'code': {'$in': code}}, {"_id": 0}, batch_size=10000)]
        else:
            data = [item for item in collection.find({}, {"_id": 0})]
        if len(data) > 0:
            res_pd = pd.DataFrame(data)

            if ltype in ['CH', 'CN']:

                cndict = dict(zip(num_columns, CH_columns))



                cndict['code'] = 'code'
                cndict['report_date'] = 'report_date'
                res_pd.columns = res_pd.columns.map(lambda x: cndict[x])
            elif ltype is 'EN':
                endict = dict(zip(num_columns, EN_columns))


                endict['code'] = 'code'
                endict['report_date'] = 'report_date'
                res_pd.columns = res_pd.columns.map(lambda x: endict[x])

            if res_pd.report_date.dtype == numpy.int64:
                res_pd.report_date = pd.to_datetime(
                    res_pd.report_date.apply(QA_util_date_int2str))
            else:
                res_pd.report_date = pd.to_datetime(res_pd.report_date)

            return res_pd.replace(-4.039810335e+34, numpy.nan).set_index(['report_date', 'code'], drop=False)
        else:
            return None
    except Exception as e:
        raise e


def QA_fetch_stock_financial_calendar(code, start, end=None, format='pd', collections=DATABASE.report_calendar):
    '获取股票日线'
    #code= [code] if isinstance(code,str) else code
    # code checking
    code = QA_util_code_tolist(code)

    if QA_util_date_valid(end):

        _data = []
        cursor = collections.find({
            'code': {'$in': code}, "real_date": {
                "$lte": end,
                "$gte": start}}, {"_id": 0}, batch_size=10000)
        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.drop_duplicates(
                (['report_date', 'code']))
            res = res.loc[:, ['code', 'name', 'pre_date', 'first_date', 'second_date',
                             'third_date', 'real_date', 'codes', 'report_date', 'crawl_date']]
        except:
            res = None
        if format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif format in ['json', 'dict']:
            return QA_util_to_json_from_pandas(res)
        # 多种数据格式
        elif format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print("QA Error QA_fetch_stock_financial_calendar format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        QA_util_log_info(
            'QA Error QA_fetch_stock_financial_calendar data parameter start=%s end=%s is not right' % (start, end))


def QA_fetch_stock_divyield(code, start, end=None, format='pd', collections=DATABASE.stock_divyield):
    '获取股票日线'
    #code= [code] if isinstance(code,str) else code
    # code checking
    code = QA_util_code_tolist(code)

    if QA_util_date_valid(end):

        _data = []
        cursor = collections.find({
            'a_stockcode': {'$in': code}, "dir_dcl_date": {
                "$lte": end,
                "$gte": start}}, {"_id": 0}, batch_size=10000)
        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.drop_duplicates(
                (['dir_dcl_date', 'a_stockcode']))
            res = res.loc[:, ['a_stockcode', 'a_stocksname', 'div_info', 'div_type_code', 'bonus_shr',
                             'cash_bt', 'cap_shr', 'epsp', 'ps_cr', 'ps_up', 'reg_date', 'dir_dcl_date',
                             'a_stockcode1', 'ex_divi_date', 'prg']]
        except:
            res = None
        if format in ['P', 'p', 'pandas', 'pd']:
            return res
        elif format in ['json', 'dict']:
            return QA_util_to_json_from_pandas(res)
        # 多种数据格式
        elif format in ['n', 'N', 'numpy']:
            return numpy.asarray(res)
        elif format in ['list', 'l', 'L']:
            return numpy.asarray(res).tolist()
        else:
            print("QA Error QA_fetch_stock_divyield format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        QA_util_log_info(
            'QA Error QA_fetch_stock_divyield data parameter start=%s end=%s is not right' % (start, end))


if __name__ == '__main__':
    print(QA_fetch_lhb('2006-07-03'))
