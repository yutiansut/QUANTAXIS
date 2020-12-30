# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2018-2020 azai/Rgveda/GolemQuant
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
#
import datetime
import time
import numpy as np
import pandas as pd
import pymongo

try:
    import QUANTAXIS as QA
    from QUANTAXIS.QAUtil import (QASETTING, 
                                  DATABASE, 
                                  QA_util_log_info, 
                                  QA_util_to_json_from_pandas,)
    from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION
    from QUANTAXIS.QAData.QADataStruct import (QA_DataStruct_Index_min, 
                                               QA_DataStruct_Index_day, 
                                               QA_DataStruct_Stock_day, 
                                               QA_DataStruct_Stock_min)
    from QUANTAXIS.QAUtil.QADate_Adv import (
        QA_util_timestamp_to_str,
        QA_util_datetime_to_Unix_timestamp,
        QA_util_print_timestamp
    )
except:
    print('PLEASE run "pip install QUANTAXIS" to call these modules')
    pass

try:
    from GolemQ.GQUtil.parameter import (
        AKA,
        INDICATOR_FIELD as FLD,
        TREND_STATUS as ST, 
    )
except:
    class AKA():
        """
        趋势状态常量，专有名称指标，定义成常量可以避免直接打字符串造成的拼写错误。
        """

        # 蜡烛线指标
        CODE = 'code'
        NAME = 'name'
        OPEN = 'open'
        HIGH = 'high'
        LOW = 'low'
        CLOSE = 'close'
        VOLUME = 'volume'
        VOL = 'vol'
        DATETIME = 'datetime'
        LAST_CLOSE = 'last_close'
        PRICE = 'price'

        SYSTEM_NAME = 'myQuant'

        def __setattr__(self, name, value):
            raise Exception(u'Const Class can\'t allow to change property\' value.')
            return super().__setattr__(name, value)


    class ST():
        """
        趋势状态常量，专有名称指标，定义成常量可以避免直接打字符串造成的拼写错误。
        """
    
        # 状态
        POSITION_R5 = 'POS_R5'
        TRIGGER_R5 = 'TRG_R5'
        CANDIDATE = 'CANDIDATE'

        def __setattr__(self, name, value):
            raise Exception(u'Const Class can\'t allow to change property\' value.')
            return super().__setattr__(name, value)


    class FLD():
        DATETIME = 'datetime'
        ML_FLU_TREND = 'ML_FLU_TREND'
        FLU_POSITIVE = 'FLU_POSITIVE'
        FLU_NEGATIVE = 'FLU_NEGATIVE'

        def __setattr__(self, name, value):
            raise Exception(u'Const Class can\'t allow to change property\' value.')
            return super().__setattr__(name, value)


def GQSignal_util_save_indices_day(code, 
                                   indices, 
                                   market_type=QA.MARKET_TYPE.STOCK_CN,
                                   portfolio='myportfolio', 
                                   ui_log=None, 
                                   ui_progress=None):
    """
    在数据库中保存所有计算出来的股票日线指标，用于汇总评估和筛选数据——日线
    save stock_indices, state

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    def _check_index(coll_indices):
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    (FLD.DATETIME,
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("date",
                     pymongo.ASCENDING),
                    (ST.TRIGGER_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("date",
                     pymongo.ASCENDING),
                    (ST.POSITION_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([('date_stamp',
                     pymongo.ASCENDING),
                    (ST.TRIGGER_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([('date_stamp',
                     pymongo.ASCENDING),
                    (ST.POSITION_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("date",
                     pymongo.ASCENDING),
                    (FLD.FLU_POSITIVE,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([('date_stamp',
                     pymongo.ASCENDING),
                    (FLD.FLU_POSITIVE,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ('date_stamp',
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ("date",
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    (FLD.DATETIME,
                     pymongo.ASCENDING),
                     (ST.CANDIDATE,
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ('date_stamp',
                     pymongo.ASCENDING),
                     (ST.CANDIDATE,
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ("date",
                     pymongo.ASCENDING),
                     (ST.CANDIDATE,
                     pymongo.ASCENDING),],
                unique=True)

    def _formatter_data(indices):
        frame = indices.reset_index(1, drop=False)
        # UTC时间转换为北京时间
        frame['date'] = pd.to_datetime(frame.index,).tz_localize('Asia/Shanghai')
        frame['date'] = frame['date'].dt.strftime('%Y-%m-%d')
        frame['datetime'] = pd.to_datetime(frame.index,).tz_localize('Asia/Shanghai')
        frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        # GMT+0 String 转换为 UTC Timestamp
        frame['date_stamp'] = pd.to_datetime(frame['date']).astype(np.int64) // 10 ** 9
        frame['created_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
        frame = frame.tail(len(frame) - 150)
        return frame

    client = QASETTING.client[AKA.SYSTEM_NAME]

    # 同时写入横表和纵表，减少查询困扰
    #coll_day = client.get_collection(
    #        'indices_{}'.format(datetime.date.today()))
    try:
        if (market_type == QA.MARKET_TYPE.STOCK_CN):
            #coll_indices = client.stock_cn_indices_day
            coll_indices = client.get_collection('stock_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.INDEX_CN):
            #coll_indices = client.index_cn_indices_day
            coll_indices = client.get_collection('index_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUND_CN):
            #coll_indices = client.fund_cn_indices_day
            coll_indices = client.get_collection('fund_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUTURE_CN):
            #coll_indices = client.future_cn_indices_day
            coll_indices = client.get_collection('future_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
            #coll_indices = client.cryptocurrency_indices_day
            coll_indices = client.get_collection('cryptocurrency_indices_{}'.format(portfolio))
        else:
            QA_util_log_info('WTF IS THIS! {} \n '.format(market_type), ui_log=ui_log)
            return False
    except Exception as e:
        QA_util_log_info(e)
        QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
        return False      

    _check_index(coll_indices)
    data = _formatter_data(indices)
    err = []

    # 查询是否新 tick
    query_id = {
        "code": code,
        'date_stamp': {
            '$in': data['date_stamp'].tolist()
        }
    }
    refcount = coll_indices.count_documents(query_id)
    if refcount > 0:
        if (len(data) > 1):
            # 删掉重复数据
            coll_indices.delete_many(query_id)
            data = QA_util_to_json_from_pandas(data)
            coll_indices.insert_many(data)
        else:
            # 持续更新模式，更新单条记录
            data.drop('created_at', axis=1, inplace=True)
            data = QA_util_to_json_from_pandas(data)
            coll_indices.replace_one(query_id, data[0])
    else:
        # 新 tick，插入记录
        data = QA_util_to_json_from_pandas(data)
        coll_indices.insert_many(data)
    return True


def GQSignal_util_save_indices_min(code, 
                                   indices, 
                                   frequence, 
                                   market_type=QA.MARKET_TYPE.STOCK_CN,
                                   portfolio='myportfolio',
                                   ui_log=None, 
                                   ui_progress=None):
    """
    在数据库中保存所有计算出来的指标信息，用于汇总评估和筛选数据——分钟线
    save stock_indices, state

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    def _check_index(coll_indices):
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    (FLD.DATETIME,
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    ("time_stamp",
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([(FLD.DATETIME,
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    (ST.TRIGGER_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([(FLD.DATETIME,
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    (ST.POSITION_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("type",
                     pymongo.ASCENDING),
                    ("time_stamp",
                     pymongo.ASCENDING),
                    (ST.TRIGGER_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("type",
                     pymongo.ASCENDING),
                    ("time_stamp",
                     pymongo.ASCENDING),
                    (ST.POSITION_R5,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([(FLD.DATETIME,
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    (FLD.FLU_POSITIVE,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("type",
                     pymongo.ASCENDING),
                    ("time_stamp",
                     pymongo.ASCENDING),
                    (FLD.FLU_POSITIVE,
                     pymongo.ASCENDING),],)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    (FLD.DATETIME,
                     pymongo.ASCENDING),
                     (ST.CANDIDATE,
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ("type",
                     pymongo.ASCENDING),
                    ("time_stamp",
                     pymongo.ASCENDING),
                     (ST.CANDIDATE,
                     pymongo.ASCENDING),],
                unique=True)

    def _formatter_data(indices, frequence):
        frame = indices.reset_index(1, drop=False)
        # UTC时间转换为北京时间
        frame['date'] = pd.to_datetime(frame.index,).tz_localize('Asia/Shanghai')
        frame['date'] = frame['date'].dt.strftime('%Y-%m-%d')
        frame['datetime'] = pd.to_datetime(frame.index,).tz_localize('Asia/Shanghai')
        frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        # GMT+0 String 转换为 UTC Timestamp
        frame['time_stamp'] = pd.to_datetime(frame['datetime']).astype(np.int64) // 10 ** 9
        frame['type'] = frequence
        frame['created_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
        frame = frame.tail(len(frame) - 150)
        return frame

    client = QASETTING.client[AKA.SYSTEM_NAME]

    # 同时写入横表和纵表，减少查询困扰
    #coll_day = client.get_collection(
    #        'indices_{}'.format(datetime.date.today()))
    try:
        if (market_type == QA.MARKET_TYPE.STOCK_CN):
            #coll_indices = client.stock_cn_indices_min
            coll_indices = client.get_collection('stock_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.INDEX_CN):
            #coll_indices = client.index_cn_indices_min
            coll_indices = client.get_collection('index_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUND_CN):
            #coll_indices = client.future_cn_indices_min
            coll_indices = client.get_collection('fund_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUTURE_CN):
            #coll_indices = client.future_cn_indices_min
            coll_indices = client.get_collection('future_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
            #coll_indices = client.cryptocurrency_indices_min
            coll_indices = client.get_collection('cryptocurrency_indices_{}'.format(portfolio))
        else:
            QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
            return False
    except Exception as e:
        QA_util_log_info(e)
        QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
        return False      

    _check_index(coll_indices)
    data = _formatter_data(indices, frequence)
    err = []

    # 查询是否新 tick
    query_id = {
        "code": code,
        'type': frequence,
        "time_stamp": {
            '$in': data['time_stamp'].tolist()
        }
    }
    refcount = coll_indices.count_documents(query_id)
    if refcount > 0:
        if (len(data) > 1):
            # 删掉重复数据
            coll_indices.delete_many(query_id)
            data = QA_util_to_json_from_pandas(data)
            coll_indices.insert_many(data)
        else:
            # 持续更新模式，更新单条记录
            data.drop('created_at', axis=1, inplace=True)
            data = QA_util_to_json_from_pandas(data)
            coll_indices.replace_one(query_id, data[0])
    else:
        # 新 tick，插入记录
        data = QA_util_to_json_from_pandas(data)
        coll_indices.insert_many(data)
    return True


def GQSignal_fetch_position_singal_day(start,
                                end,
                                frequence='day',
                                market_type=QA.MARKET_TYPE.STOCK_CN,
                                portfolio='myportfolio', 
                                format='numpy',
                                ui_log=None, 
                                ui_progress=None):
    """
    '获取股票指标日线'

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    start = str(start)[0:10]
    end = str(end)[0:10]
    #code= [code] if isinstance(code,str) else code

    client = QASETTING.client[AKA.SYSTEM_NAME]
    # 同时写入横表和纵表，减少查询困扰
    #coll_day = client.get_collection(
    #        'indices_{}'.format(datetime.date.today()))
    try:
        if (market_type == QA.MARKET_TYPE.STOCK_CN):
            #coll_indices = client.stock_cn_indices_min
            coll_indices = client.get_collection('stock_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.INDEX_CN):
            #coll_indices = client.index_cn_indices_min
            coll_indices = client.get_collection('index_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUND_CN):
            #coll_indices = client.future_cn_indices_min
            coll_indices = client.get_collection('fund_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUTURE_CN):
            #coll_indices = client.future_cn_indices_min
            coll_indices = client.get_collection('future_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
            #coll_indices = client.cryptocurrency_indices_min
            coll_indices = client.get_collection('cryptocurrency_indices_{}'.format(portfolio))
        else:
            QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
            return False
    except Exception as e:
        QA_util_log_info(e)
        QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
        return False

    if QA_util_date_valid(end):
        cursor = coll_indices.find({
                ST.TRIGGER_R5: {
                    '$gt': 0
                },
                "date_stamp":
                    {
                        "$lte": QA_util_date_stamp(end),
                        "$gte": QA_util_date_stamp(start)
                    }
            },
            {"_id": 0},
            batch_size=10000)
        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.assign(date=pd.to_datetime(res.date)).drop_duplicates((['date',
                                'code'])).set_index(['date',
                                'code'],
                                    drop=False)
            codelist = QA.QA_fetch_stock_name(res[AKA.CODE].tolist())
            res['name'] = res.apply(lambda x:codelist.at[x.get(AKA.CODE), 'name'], axis=1)
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
            print("QA Error GQSignal_fetch_position_singal_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        QA_util_log_info('QA Error GQSignal_fetch_position_singal_day data parameter start=%s end=%s is not right' % (start,
               end))


def GQSignal_fetch_singal_day(code,
                              start,
                              end,
                              frequence='day',
                              market_type=QA.MARKET_TYPE.STOCK_CN,
                              portfolio='myportfolio', 
                              format='numpy',
                              ui_log=None, 
                              ui_progress=None):
    """
    获取股票日线指标/策略信号数据

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    start = str(start)[0:10]
    end = str(end)[0:10]
    #code= [code] if isinstance(code,str) else code

    client = QASETTING.client[AKA.SYSTEM_NAME]
    # 同时写入横表和纵表，减少查询困扰
    #coll_day = client.get_collection(
    #        'indices_{}'.format(datetime.date.today()))
    try:
        if (market_type == QA.MARKET_TYPE.STOCK_CN):
            #coll_indices = client.stock_cn_indices_min
            coll_indices = client.get_collection('stock_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.INDEX_CN):
            #coll_indices = client.index_cn_indices_min
            coll_indices = client.get_collection('index_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUND_CN):
            #coll_indices = client.future_cn_indices_min
            coll_indices = client.get_collection('fund_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.FUTURE_CN):
            #coll_indices = client.future_cn_indices_min
            coll_indices = client.get_collection('future_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.CRYPTOCURRENCY):
            #coll_indices = client.cryptocurrency_indices_min
            coll_indices = client.get_collection('cryptocurrency_indices_{}'.format(portfolio))
        else:
            QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
            return False
    except Exception as e:
        QA_util_log_info(e)
        QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
        return False

    # code checking
    code = QA_util_code_tolist(code)

    if QA_util_date_valid(end):
        cursor = coll_indices.find({
                'code': {
                    '$in': code
                },
                "date_stamp":
                    {
                        "$lte": QA_util_date_stamp(end),
                        "$gte": QA_util_date_stamp(start)
                    }
            },
            {"_id": 0},
            batch_size=10000)
        #res=[QA_util_dict_remove_key(data, '_id') for data in cursor]

        res = pd.DataFrame([item for item in cursor])
        try:
            res = res.assign(date=pd.to_datetime(res.date)).drop_duplicates((['date',
                                'code'])).set_index(['date',
                                'code'], drop=False)
            res.sort_index(inplace=True)
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
            print("QA Error GQSignal_fetch_singal_day format parameter %s is none of  \"P, p, pandas, pd , json, dict , n, N, numpy, list, l, L, !\" " % format)
            return None
    else:
        QA_util_log_info('QA Error GQSignal_fetch_singal_day data parameter start=%s end=%s is not right' % (start,
               end))
 

def GQ_save_test(code, 
                indices, 
                market_type=QA.MARKET_TYPE.STOCK_CN,
                portfolio='myportfolio', 
                ui_log=None, 
                ui_progress=None):
    """
    在数据库中保存所有计算出来的股票日线指标，用于汇总评估和筛选数据——日线
    save stock_indices, state

    Keyword Arguments:
        client {[type]} -- [description] (default: {DATABASE})
    """
    def _check_index(coll_indices):
        coll_indices.create_index([("code",
                     pymongo.ASCENDING),
                    ('datetime',
                     pymongo.ASCENDING),],
                unique=True)
        coll_indices.create_index([("date",
                     pymongo.ASCENDING),
                    ('TRG_R5',
                     pymongo.ASCENDING),],)

    def _formatter_data(indices):
        frame = indices.reset_index(1, drop=False)
        # UTC时间转换为北京时间
        frame['date'] = pd.to_datetime(frame.index,).tz_localize('Asia/Shanghai')
        frame['date'] = frame['date'].dt.strftime('%Y-%m-%d')
        frame['datetime'] = pd.to_datetime(frame.index,).tz_localize('Asia/Shanghai')
        frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        # GMT+0 String 转换为 UTC Timestamp
        frame['date_stamp'] = pd.to_datetime(frame['date']).astype(np.int64) // 10 ** 9
        frame['created_at'] = int(time.mktime(datetime.datetime.now().utctimetuple()))
        frame = frame.tail(len(frame) - 150)
        return frame

    client = QASETTING.client['quantaxis']

    # 同时写入横表和纵表，减少查询困扰
    #coll_day = client.get_collection(
    #        'indices_{}'.format(datetime.date.today()))
    try:
        if (market_type == QA.MARKET_TYPE.STOCK_CN):
            #coll_indices = client.stock_cn_indices_day
            coll_indices = client.get_collection('stock_cn_indices_{}'.format(portfolio))
        elif (market_type == QA.MARKET_TYPE.INDEX_CN):
            #coll_indices = client.index_cn_indices_day
            coll_indices = client.get_collection('index_cn_indices_{}'.format(portfolio))
        else:
            QA_util_log_info('WTF IS THIS! {} \n '.format(market_type), ui_log=ui_log)
            return False
    except Exception as e:
        QA_util_log_info(e)
        QA_util_log_info('WTF IS THIS! \n ', ui_log=ui_log)
        return False      

    _check_index(coll_indices)
    data = _formatter_data(indices)
    err = []

    # 查询是否新 tick
    query_id = {
        "code": code,
        'date_stamp': {
            '$in': data['date_stamp'].tolist()
        }
    }
    refcount = coll_indices.count_documents(query_id)
    if refcount > 0:
        if (len(data) > 1):
            # 删掉重复数据
            coll_indices.delete_many(query_id)
            data = QA_util_to_json_from_pandas(data)
            coll_indices.insert_many(data)
        else:
            # 持续更新模式，更新单条记录
            data.drop('created_at', axis=1, inplace=True)
            data = QA_util_to_json_from_pandas(data)
            coll_indices.replace_one(query_id, data[0])
    else:
        # 新 tick，插入记录
        data = QA_util_to_json_from_pandas(data)
        coll_indices.insert_many(data)
    return True

data_day = QA.QA_fetch_stock_day_adv(['000001'], '2018-12-01', '2019-05-20')
data_day = data_day.to_qfq().data

GQ_save_test('000001',data_day)