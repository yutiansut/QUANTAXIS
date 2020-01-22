# coding:utf-8
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

# from QUANTAXIS.QAData.data_fq import QA_data_make_qfq, QA_data_make_hfq

# 基于Pytdx的数据接口,好处是可以在linux/mac上联入通达信行情
# 具体参见rainx的pytdx(https://github.com/rainx/pytdx)
#


import datetime

import numpy as np
import pandas as pd
from pytdx.exhq import TdxExHq_API
from pytdx.hq import TdxHq_API
from retrying import retry

from QUANTAXIS.QAFetch.base import _select_market_code, _select_index_code, _select_type, _select_bond_market_code
from QUANTAXIS.QAUtil import (QA_Setting, QA_util_date_stamp,
                              QA_util_date_str2int, QA_util_date_valid,
                              QA_util_get_real_date, QA_util_get_real_datelist,
                              QA_util_future_to_realdatetime, QA_util_tdxtimestamp,
                              QA_util_future_to_tradedatetime,
                              QA_util_get_trade_gap, QA_util_log_info,
                              QA_util_time_stamp, QA_util_web_ping,
                              exclude_from_stock_ip_list, future_ip_list,
                              stock_ip_list, trade_date_sse)
from QUANTAXIS.QAUtil.QASetting import QASETTING
from QUANTAXIS.QASetting.QALocalize import log_path
from QUANTAXIS.QAUtil import Parallelism
from QUANTAXIS.QAUtil.QACache import QA_util_cache


def init_fetcher():
    """初始化获取
    """

    pass


def ping(ip, port=7709, type_='stock'):
    api = TdxHq_API()
    apix = TdxExHq_API()
    __time1 = datetime.datetime.now()
    try:
        if type_ in ['stock']:
            with api.connect(ip, port, time_out=0.7):
                res = api.get_security_list(0, 1)

                if res is not None:
                    if len(api.get_security_list(0, 1)) > 800:
                        return datetime.datetime.now() - __time1
                    else:
                        print('BAD RESPONSE {}'.format(ip))
                        return datetime.timedelta(9, 9, 0)
                else:

                    print('BAD RESPONSE {}'.format(ip))
                    return datetime.timedelta(9, 9, 0)
        elif type_ in ['future']:
            with apix.connect(ip, port, time_out=0.7):
                res = apix.get_instrument_count()
                if res is not None:
                    if res > 20000:
                        return datetime.datetime.now() - __time1
                    else:
                        print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                        return datetime.timedelta(9, 9, 0)
                else:
                    print('️Bad FUTUREIP REPSONSE {}'.format(ip))
                    return datetime.timedelta(9, 9, 0)
    except Exception as e:
        if isinstance(e, TypeError):
            print(e)
            print('Tushare内置的pytdx版本和QUANTAXIS使用的pytdx 版本不同, 请重新安装pytdx以解决此问题')
            print('pip uninstall pytdx')
            print('pip install pytdx')

        else:
            print('BAD RESPONSE {}'.format(ip))
        return datetime.timedelta(9, 9, 0)


def select_best_ip():
    QA_util_log_info('Selecting the Best Server IP of TDX')

    # 删除exclude ip
    import json
    null = None
    qasetting = QASETTING
    exclude_ip = {'ip': '1.1.1.1', 'port': 7709}
    default_ip = {'stock': {'ip': None, 'port': None},
                  'future': {'ip': None, 'port': None}}
    alist = []
    alist.append(exclude_ip)

    ipexclude = qasetting.get_config(
        section='IPLIST', option='exclude', default_value=alist)

    exclude_from_stock_ip_list(ipexclude)

    ipdefault = qasetting.get_config(
        section='IPLIST', option='default', default_value=default_ip)

    ipdefault = eval(ipdefault) if isinstance(ipdefault, str) else ipdefault
    assert isinstance(ipdefault, dict)
    if ipdefault['stock']['ip'] == None:

        best_stock_ip = get_ip_list_by_ping(stock_ip_list)
    else:
        if ping(ipdefault['stock']['ip'], ipdefault['stock']['port'],
                'stock') < datetime.timedelta(0, 1):
            print('USING DEFAULT STOCK IP')
            best_stock_ip = ipdefault['stock']
        else:
            print('DEFAULT STOCK IP is BAD, RETESTING')
            best_stock_ip = get_ip_list_by_ping(stock_ip_list)
    if ipdefault['future']['ip'] == None:
        best_future_ip = get_ip_list_by_ping(future_ip_list, _type='future')
    else:
        if ping(ipdefault['future']['ip'], ipdefault['future']['port'],
                'future') < datetime.timedelta(0, 1):
            print('USING DEFAULT FUTURE IP')
            best_future_ip = ipdefault['future']
        else:
            print('DEFAULT FUTURE IP {} is BAD, RETESTING'.format(ipdefault))
            best_future_ip = get_ip_list_by_ping(future_ip_list,
                                                 _type='future')
    ipbest = {'stock': best_stock_ip, 'future': best_future_ip}
    qasetting.set_config(
        section='IPLIST', option='default', default_value=ipbest)

    QA_util_log_info(
        '=== The BEST SERVER ===\n stock_ip {} future_ip {}'.format(
            best_stock_ip['ip'], best_future_ip['ip']))
    return ipbest


def get_ip_list_by_ping(ip_list=[], _type='stock'):
    best_ip = get_ip_list_by_multi_process_ping(ip_list, 1, _type)
    return best_ip[0]


def get_ip_list_by_multi_process_ping(ip_list=[], n=0, _type='stock',
                                      cache_age=86400):
    ''' 根据ping排序返回可用的ip列表
    2019 04 09  增加_type缓存时间cache_age
    2019 03 31 取消参数filename
    :param ip_list: ip列表
    :param n: 最多返回的ip数量， 当可用ip数量小于n，返回所有可用的ip；n=0时，返回所有可用ip
    :param _type: ip类型
    :param cache_age: ip类型缓存时间（秒），默认为一天（86400秒）
    :return: 可以ping通的ip列表
    '''
    cache = QA_util_cache()
    results = cache.get(_type)
    if results:
        # read the data from cache
        print('loading ip list from {} cache.'.format(_type))
    else:
        ips = [(x['ip'], x['port'], _type) for x in ip_list]
        ps = Parallelism()
        ps.run(ping, ips)
        data = list(ps.get_results())
        results = []
        for i in range(len(data)):
            # 删除ping不通的数据
            if data[i] < datetime.timedelta(0, 9, 0):
                results.append((data[i], ip_list[i]))
        # 按照ping值从小大大排序
        results = [x[1] for x in sorted(results, key=lambda x: x[0])]
        if _type:
            # store the data as binary data stream
            cache.set(_type, results, age=cache_age)
            print('saving ip list to {} cache {}'.format(_type, len(results)))
    if len(results) > 0:
        if n == 0 and len(results) > 0:
            return results
        else:
            return results[:n]
    else:
        print('ALL IP PING TIMEOUT!')
        return [{'ip': None, 'port': None}]


global best_ip
best_ip = {
    'stock': {
        'ip': None, 'port': None
    },
    'future': {
        'ip': None, 'port': None
    }
}


# return 1 if sh, 0 if sz


def get_extensionmarket_ip(ip, port):
    global best_ip
    if ip is None and port is None and best_ip['future']['ip'] is None and \
            best_ip['future']['port'] is None:
        best_ip = select_best_ip()
        ip = best_ip['future']['ip']
        port = best_ip['future']['port']
    elif ip is None and port is None and \
            best_ip['future']['ip'] is not None and \
            best_ip['future']['port'] is not None:
        ip = best_ip['future']['ip']
        port = best_ip['future']['port']
    else:
        pass
    return ip, port


def get_mainmarket_ip(ip, port):
    """[summary]
    Arguments:
        ip {[type]} -- [description]
        port {[type]} -- [description]
    Returns:
        [type] -- [description]
    """

    global best_ip
    if ip is None and port is None and best_ip['stock']['ip'] is None and \
            best_ip['stock']['port'] is None:
        best_ip = select_best_ip()
        ip = best_ip['stock']['ip']
        port = best_ip['stock']['port']
    elif ip is None and port is None and \
            best_ip['stock']['ip'] is not None and \
            best_ip['stock']['port'] is not None:
        ip = best_ip['stock']['ip']
        port = best_ip['stock']['port']
    else:
        pass
    return ip, port


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_security_bars(code, _type, lens, ip=None, port=None):
    """按bar长度推算数据
    Arguments:
        code {[type]} -- [description]
        _type {[type]} -- [description]
        lens {[type]} -- [description]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {best_ip})
        port {[type]} -- [description] (default: {7709})
    Returns:
        [type] -- [description]
    """
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat([api.to_df(
            api.get_security_bars(_select_type(_type), _select_market_code(
                code), code, (i - 1) * 800, 800)) for i in
            range(1, int(lens / 800) + 2)], axis=0, sort=False)
        data = data \
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                  inplace=False) \
            .assign(datetime=pd.to_datetime(data['datetime']),
                    date=data['datetime'].apply(lambda x: str(x)[0:10]),
                    date_stamp=data['datetime'].apply(
                        lambda x: QA_util_date_stamp(x)),
                    time_stamp=data['datetime'].apply(
                        lambda x: QA_util_time_stamp(x)),
                    type=_type, code=str(code)) \
            .set_index('datetime', drop=False, inplace=False).tail(lens)
        if data is not None:
            return data
        else:
            return None


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_day(code, start_date, end_date, if_fq='00',
                           frequence='day', ip=None, port=None):
    """获取日线及以上级别的数据
    Arguments:
        code {str:6} -- code 是一个单独的code 6位长度的str
        start_date {str:10} -- 10位长度的日期 比如'2017-01-01'
        end_date {str:10} -- 10位长度的日期 比如'2018-01-01'
    Keyword Arguments:
        if_fq {str} -- '00'/'bfq' -- 不复权 '01'/'qfq' -- 前复权 '02'/'hfq' -- 后复权 '03'/'ddqfq' -- 定点前复权 '04'/'ddhfq' --定点后复权
        frequency {str} -- day/week/month/quarter/year 也可以是简写 D/W/M/Q/Y
        ip {str} -- [description] (default: None) ip可以通过select_best_ip()函数重新获取
        port {int} -- [description] (default: {None})
    Returns:
        pd.DataFrame/None -- 返回的是dataframe,如果出错比如只获取了一天,而当天停牌,返回None
    Exception:
        如果出现网络问题/服务器拒绝, 会出现socket:time out 尝试再次获取/更换ip即可, 本函数不做处理
    """
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    try:
        with api.connect(ip, port, time_out=0.7):

            if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
                frequence = 9
            elif frequence in ['w', 'W', 'Week', 'week']:
                frequence = 5
            elif frequence in ['month', 'M', 'm', 'Month']:
                frequence = 6
            elif frequence in ['quarter', 'Q', 'Quarter', 'q']:
                frequence = 10
            elif frequence in ['y', 'Y', 'year', 'Year']:
                frequence = 11
            start_date = str(start_date)[0:10]
            today_ = datetime.date.today()
            lens = QA_util_get_trade_gap(start_date, today_)

            data = pd.concat([api.to_df(
                api.get_security_bars(frequence, _select_market_code(
                    code), code, (int(lens / 800) - i) * 800, 800)) for i in
                range(int(lens / 800) + 1)], axis=0, sort=False)

            # 这里的问题是: 如果只取了一天的股票,而当天停牌, 那么就直接返回None了
            if len(data) < 1:
                return None
            data = data[data['open'] != 0]

            data = data.assign(
                date=data['datetime'].apply(lambda x: str(x[0:10])),
                code=str(code),
                date_stamp=data['datetime'].apply(
                    lambda x: QA_util_date_stamp(str(x)[0:10]))) \
                .set_index('date', drop=False, inplace=False)

            end_date = str(end_date)[0:10]
            data = data.drop(
                ['year', 'month', 'day', 'hour', 'minute', 'datetime'],
                axis=1)[
                start_date:end_date]
            if if_fq in ['00', 'bfq']:
                return data
            else:
                print('CURRENTLY NOT SUPPORT REALTIME FUQUAN')
                return None
                # xdxr = QA_fetch_get_stock_xdxr(code)
                # if if_fq in ['01','qfq']:
                #     return QA_data_make_qfq(data,xdxr)
                # elif if_fq in ['02','hfq']:
                #     return QA_data_make_hfq(data,xdxr)
    except Exception as e:
        if isinstance(e, TypeError):
            print('Tushare内置的pytdx版本和QUANTAXIS使用的pytdx 版本不同, 请重新安装pytdx以解决此问题')
            print('pip uninstall pytdx')
            print('pip install pytdx')
        else:
            print(e)


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_min(code, start, end, frequence='1min', ip=None,
                           port=None):
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    type_ = ''
    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    if str(frequence) in ['5', '5m', '5min', 'five']:
        frequence, type_ = 0, '5min'
        lens = 48 * lens
    elif str(frequence) in ['1', '1m', '1min', 'one']:
        frequence, type_ = 8, '1min'
        lens = 240 * lens
    elif str(frequence) in ['15', '15m', '15min', 'fifteen']:
        frequence, type_ = 1, '15min'
        lens = 16 * lens
    elif str(frequence) in ['30', '30m', '30min', 'half']:
        frequence, type_ = 2, '30min'
        lens = 8 * lens
    elif str(frequence) in ['60', '60m', '60min', '1h']:
        frequence, type_ = 3, '60min'
        lens = 4 * lens
    if lens > 20800:
        lens = 20800
    with api.connect(ip, port):

        data = pd.concat(
            [api.to_df(
                api.get_security_bars(
                    frequence, _select_market_code(
                        str(code)),
                    str(code),
                    (int(lens / 800) - i) * 800, 800)) for i
             in range(int(lens / 800) + 1)], axis=0, sort=False)
        data = data \
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                  inplace=False) \
            .assign(datetime=pd.to_datetime(data['datetime']),
                    code=str(code),
                    date=data['datetime'].apply(lambda x: str(x)[0:10]),
                    date_stamp=data['datetime'].apply(
                lambda x: QA_util_date_stamp(x)),
                time_stamp=data['datetime'].apply(
                lambda x: QA_util_time_stamp(x)),
                type=type_).set_index('datetime', drop=False,
                                      inplace=False)[start:end]
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_latest(code, frequence='day', ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    code = [code] if isinstance(code, str) else code
    api = TdxHq_API(multithread=True)

    if frequence in ['w', 'W', 'Week', 'week']:
        frequence = 5
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = 6
    elif frequence in ['Q', 'Quarter', 'q']:
        frequence = 10
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = 11
    elif frequence in ['5', '5m', '5min', 'five']:
        frequence = 0
    elif frequence in ['1', '1m', '1min', 'one']:
        frequence = 8
    elif frequence in ['15', '15m', '15min', 'fifteen']:
        frequence = 1
    elif frequence in ['30', '30m', '30min', 'half']:
        frequence = 2
    elif frequence in ['60', '60m', '60min', '1h']:
        frequence = 3
    else:
        frequence = 9

    with api.connect(ip, port):
        data = pd.concat([api.to_df(api.get_security_bars(
            frequence, _select_market_code(item), item, 0, 1)).assign(
            code=item) for item in code], axis=0, sort=False)
        return data \
            .assign(date=pd.to_datetime(data['datetime']
                                        .apply(lambda x: x[0:10])),
                    date_stamp=data['datetime']
                    .apply(lambda x: QA_util_date_stamp(str(x[0:10])))) \
            .set_index('date', drop=False) \
            .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'],
                  axis=1)


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_realtime(code=['000001', '000002'], ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    # reversed_bytes9 --> 涨速
    # active1,active2 --> 活跃度
    # reversed_bytes1 --> -价格*100
    # vol 总量 cur_vol 现量
    # amount 总金额
    # s_vol 内盘 b_vol 外盘
    # reversed_bytes2 市场
    # # reversed_bytes0 时间

    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if isinstance(code, str) else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(_select_market_code(x), x) for x in
                 code[80 * id_:80 * (id_ + 1)]])))
            __data = __data.assign(datetime=datetime.datetime.now(
            ), servertime=__data['reversed_bytes0'].apply(QA_util_tdxtimestamp))
            # __data['rev']
        data = __data[
            ['datetime', 'servertime', 'active1', 'active2', 'last_close', 'code', 'open',
             'high', 'low', 'price', 'cur_vol',
             's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1',
             'ask2', 'ask_vol2',
             'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3',
             'ask4',
             'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5',
             'bid_vol5']]
        return data.set_index(['datetime', 'code'])

@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_index_realtime(code=['000001'], ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    # reversed_bytes9 --> 涨速
    # active1,active2 --> 活跃度
    # reversed_bytes1 --> -价格*100
    # vol 总量 cur_vol 现量
    # amount 总金额
    # s_vol 内盘 b_vol 外盘
    # reversed_bytes2 市场
    # # reversed_bytes0 时间

    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if isinstance(code, str) else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(_select_index_code(x), x) for x in
                 code[80 * id_:80 * (id_ + 1)]])))
            __data = __data.assign(datetime=datetime.datetime.now(
            ), servertime=__data['reversed_bytes0'].apply(QA_util_tdxtimestamp))
            # __data['rev']
        data = __data[
            ['datetime', 'servertime', 'active1', 'active2', 'last_close', 'code', 'open',
             'high', 'low', 'price', 'cur_vol',
             's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1',
             'ask2', 'ask_vol2',
             'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3',
             'ask4',
             'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5',
             'bid_vol5']]
        return data.set_index(['datetime', 'code'])

@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_bond_realtime(code=['010107'], ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    # reversed_bytes9 --> 涨速
    # active1,active2 --> 活跃度
    # reversed_bytes1 --> -价格*100
    # vol 总量 cur_vol 现量
    # amount 总金额
    # s_vol 内盘 b_vol 外盘
    # reversed_bytes2 市场
    # # reversed_bytes0 时间

    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if isinstance(code, str) else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(_select_bond_market_code(x), x) for x in
                 code[80 * id_:80 * (id_ + 1)]])))
            __data = __data.assign(datetime=datetime.datetime.now(
            ), servertime=__data['reversed_bytes0'].apply(QA_util_tdxtimestamp))
            # __data['rev']
        data = __data[
            ['datetime', 'servertime', 'active1', 'active2', 'last_close', 'code', 'open',
             'high', 'low', 'price', 'cur_vol',
             's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1',
             'ask2', 'ask_vol2',
             'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3',
             'ask4',
             'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5',
             'bid_vol5']]
        data = data.assign(last_close=data.last_close/10, open=data.open/10, high=data.high/10, low=data.low/10,
                        price= data.price/10,  
                        ask1=data.ask1/10, ask2=data.ask2/10, ask3=data.ask3/10, ask4=data.ask4/10, ask5=data.ask5/10,
                        bid1=data.bid1/10, bid2=data.bid2/10, bid3=data.bid3/10, bid4=data.bid4/10, bid5=data.bid5/10)

        return data.set_index(['datetime', 'code'])
@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_depth_market_data(code=['000001', '000002'], ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    __data = pd.DataFrame()
    with api.connect(ip, port):
        code = [code] if isinstance(code, str) else code
        for id_ in range(int(len(code) / 80) + 1):
            __data = __data.append(api.to_df(api.get_security_quotes(
                [(_select_market_code(x), x) for x in
                 code[80 * id_:80 * (id_ + 1)]])))
            __data['datetime'] = datetime.datetime.now()
        data = __data
        # data = __data[['datetime', 'active1', 'active2', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
        #                's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
        #                'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
        #                'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]
        return data.set_index(['datetime', 'code'], drop=False, inplace=False)


'''
沪市
010xxx 国债
001×××国债现货；
110×××120×××企业债券；
129×××100×××可转换债券；
201×××国债回购；
310×××国债期货；
500×××550×××基金；
600×××A股；
700×××配股；
710×××转配股；
701×××转配股再配股；
711×××转配股再转配股；
720×××红利；
730×××新股申购；
735×××新基金申购；
737×××新股配售；
900×××B股。
深市
第1位	第二位	第3-6位	含义
0	0	XXXX	A股证券
0	3	XXXX	A股A2权证
0	7	XXXX	A股增发
0	8	XXXX	A股A1权证
0	9	XXXX	A股转配
1	0	XXXX	国债现货
1	1	XXXX	债券
1	2	XXXX	可转换债券
1	3	XXXX	国债回购
1	7	XXXX	原有投资基金
1	8	XXXX	证券投资基金
2	0	XXXX	B股证券
2	7	XXXX	B股增发
2	8	XXXX	B股权证
3	0	XXXX	创业板证券
3	7	XXXX	创业板增发
3	8	XXXX	创业板权证
3	9	XXXX	综合指数/成份指数
深市A股票买卖的代码是以000打头，如：顺鑫农业：股票代码是000860。
B股买卖的代码是以200打头，如：深中冠B股，代码是200018。
中小板股票代码以002打头，如：东华合创股票代码是002065。
创业板股票代码以300打头，如：探路者股票代码是：300005
更多参见 issue https://github.com/QUANTAXIS/QUANTAXIS/issues/158
@yutiansut
'''


def for_sz(code):
    """深市代码分类
    Arguments:
        code {[type]} -- [description]
    Returns:
        [type] -- [description]
    """

    if str(code)[0:2] in ['00', '30', '02']:
        return 'stock_cn'
    elif str(code)[0:2] in ['39']:
        return 'index_cn'
    elif str(code)[0:2] in ['15']:
        return 'etf_cn'
    elif str(code)[0:3] in ['101', '104', '105', '106', '107', '108', '109',
                            '111', '112', '114', '115', '116', '117', '118', '119',
                            '123', '127', '128',
                            '131', '139', ]:
        # 10xxxx 国债现货
        # 11xxxx 债券
        # 12xxxx 可转换债券

            # 123
            # 127
        # 12xxxx 国债回购
        return 'bond_cn'

    elif str(code)[0:2] in ['20']:
        return 'stockB_cn'
    else:
        return 'undefined'


def for_sh(code):
    if str(code)[0] == '6':
        return 'stock_cn'
    elif str(code)[0:3] in ['000', '880']:
        return 'index_cn'
    elif str(code)[0:2] == '51':
        return 'etf_cn'
    # 110×××120×××企业债券；
    # 129×××100×××可转换债券；
    # 113A股对应可转债 132
    elif str(code)[0:3] in ['102', '110', '113', '120', '122', '124',
                            '130', '132', '133', '134', '135', '136',
                            '140', '141', '143', '144', '147', '148']:
        return 'bond_cn'
    else:
        return 'undefined'


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_list(type_='stock', ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat(
            [pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(
                sse='sz' if j == 0 else 'sh').set_index(
                ['code', 'sse'], drop=False) for i in
                range(int(api.get_security_count(j) / 1000) + 1)], axis=0, sort=False) for
                j
                in range(2)], axis=0, sort=False)
        # data.code = data.code.apply(int)
        sz = data.query('sse=="sz"')
        sh = data.query('sse=="sh"')

        sz = sz.assign(sec=sz.code.apply(for_sz))
        sh = sh.assign(sec=sh.code.apply(for_sh))

        if type_ in ['stock', 'gp']:

            return pd.concat([sz, sh], sort=False).query(
                'sec=="stock_cn"').sort_index().assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))

        elif type_ in ['index', 'zs']:

            return pd.concat([sz, sh], sort=False).query(
                'sec=="index_cn"').sort_index().assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))
            # .assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            # .assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))
        elif type_ in ['etf', 'ETF']:
            return pd.concat([sz, sh], sort=False).query(
                'sec=="etf_cn"').sort_index().assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))

        else:
            return data.assign(
                code=data['code'].apply(lambda x: str(x))).assign(
                name=data['name'].apply(lambda x: str(x)[0:6]))
            # .assign(szm=data['name'].apply(lambda x: ''.join([y[0] for y in lazy_pinyin(x)])))\
            #    .assign(quanpin=data['name'].apply(lambda x: ''.join(lazy_pinyin(x))))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_index_list(ip=None, port=None):
    """获取指数列表
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    Returns:
        [type] -- [description]
    """

    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat(
            [pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(
                sse='sz' if j == 0 else 'sh').set_index(
                ['code', 'sse'], drop=False) for i in
                range(int(api.get_security_count(j) / 1000) + 1)], axis=0, sort=False) for
                j
                in range(2)], axis=0, sort=False)
        # data.code = data.code.apply(int)
        sz = data.query('sse=="sz"')
        sh = data.query('sse=="sh"')

        sz = sz.assign(sec=sz.code.apply(for_sz))
        sh = sh.assign(sec=sh.code.apply(for_sh))
        return pd.concat([sz, sh], sort=False).query(
            'sec=="index_cn"').sort_index().assign(
            name=data['name'].apply(lambda x: str(x)[0:6]))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_bond_list(ip=None, port=None):
    """bond
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    """
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    with api.connect(ip, port):
        data = pd.concat(
            [pd.concat([api.to_df(api.get_security_list(j, i * 1000)).assign(
                sse='sz' if j == 0 else 'sh').set_index(
                ['code', 'sse'], drop=False) for i in
                range(int(api.get_security_count(j) / 1000) + 1)], axis=0, sort=False) for
                j
                in range(2)], axis=0, sort=False)
        # data.code = data.code.apply(int)
        sz = data.query('sse=="sz"')
        sh = data.query('sse=="sh"')
        sz = sz.assign(sec=sz.code.apply(for_sz))
        sh = sh.assign(sec=sh.code.apply(for_sh))
        return pd.concat([sz, sh], sort=False).query('sec=="bond_cn"').sort_index().assign(
            name=data['name'].apply(lambda x: str(x)[0:6]))

@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_bond_day(code, start_date, end_date, frequence='day', ip=None,
                          port=None):
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
        frequence = 9
    elif frequence in ['w', 'W', 'Week', 'week']:
        frequence = 5
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = 6
    elif frequence in ['Q', 'Quarter', 'q']:
        frequence = 10
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = 11

    with api.connect(ip, port):

        start_date = str(start_date)[0:10]
        today_ = datetime.date.today()
        lens = QA_util_get_trade_gap(start_date, today_)

        code = str(code)
        data = pd.concat([api.to_df(api.get_security_bars(
            frequence, _select_bond_market_code(code),
            code, (int(lens / 800) - i) * 800, 800))
            for i in range(int(lens / 800) + 1)], axis=0, sort=False)
        data = data.assign(
            date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(
            code=str(code)) \
            .assign(date_stamp=data['datetime'].apply(
                lambda x: QA_util_date_stamp(str(x)[0:10]))) \
            .set_index('date', drop=False, inplace=False) \
            .assign(code=code) \
            .drop(['year', 'month', 'day', 'hour',
                   'minute', 'datetime'], axis=1)[start_date:end_date]
        return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_bond_min(code, start, end, frequence='1min', ip=None,
                          port=None):
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    if str(frequence) in ['5', '5m', '5min', 'five']:
        frequence, type_ = 0, '5min'
        lens = 48 * lens
    elif str(frequence) in ['1', '1m', '1min', 'one']:
        frequence, type_ = 8, '1min'
        lens = 240 * lens
    elif str(frequence) in ['15', '15m', '15min', 'fifteen']:
        frequence, type_ = 1, '15min'
        lens = 16 * lens
    elif str(frequence) in ['30', '30m', '30min', 'half']:
        frequence, type_ = 2, '30min'
        lens = 8 * lens
    elif str(frequence) in ['60', '60m', '60min', '1h']:
        frequence, type_ = 3, '60min'
        lens = 4 * lens

    if lens > 20800:
        lens = 20800#u
    code = str(code)
    with api.connect(ip, port):

        data = pd.concat(
            [api.to_df(
                api.get_security_bars(
                    frequence, _select_bond_market_code(
                        str(code)),
                    str(code),
                    (int(lens / 800) - i) * 800, 800)) for i
             in range(int(lens / 800) + 1)], axis=0, sort=False)
        #print(data)
        data = data \
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                  inplace=False) \
            .assign(datetime=pd.to_datetime(data['datetime']),
                    code=str(code),
                    date=data['datetime'].apply(lambda x: str(x)[0:10]),
                    date_stamp=data['datetime'].apply(
                lambda x: QA_util_date_stamp(x)),
                time_stamp=data['datetime'].apply(
                lambda x: QA_util_time_stamp(x)),
                type=type_).set_index('datetime', drop=False,
                                      inplace=False)[start:end]
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_index_day(code, start_date, end_date, frequence='day',
                           ip=None, port=None):
    """指数日线
    1- sh
    0 -sz
    Arguments:
        code {[type]} -- [description]
        start_date {[type]} -- [description]
        end_date {[type]} -- [description]
    Keyword Arguments:
        frequence {str} -- [description] (default: {'day'})
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    Returns:
        [type] -- [description]
    """

    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    if frequence in ['day', 'd', 'D', 'DAY', 'Day']:
        frequence = 9
    elif frequence in ['w', 'W', 'Week', 'week']:
        frequence = 5
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = 6
    elif frequence in ['Q', 'Quarter', 'q']:
        frequence = 10
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = 11

    with api.connect(ip, port):

        start_date = str(start_date)[0:10]
        today_ = datetime.date.today()
        lens = QA_util_get_trade_gap(start_date, today_)

        if str(code)[0] in ['5', '1']:  # ETF
            data = pd.concat([api.to_df(api.get_security_bars(
                frequence, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0,
                code, (int(lens / 800) - i) * 800, 800))
                for i in range(int(lens / 800) + 1)], axis=0, sort=False)
        else:
            data = pd.concat([api.to_df(api.get_index_bars(
                frequence, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0,
                code, (int(lens / 800) - i) * 800, 800))
                for i in range(int(lens / 800) + 1)], axis=0, sort=False)
        data = data.assign(
            date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(
            code=str(code)) \
            .assign(date_stamp=data['datetime'].apply(
                lambda x: QA_util_date_stamp(str(x)[0:10]))) \
            .set_index('date', drop=False, inplace=False) \
            .assign(code=code) \
            .drop(['year', 'month', 'day', 'hour',
                   'minute', 'datetime'], axis=1)[start_date:end_date]
        return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_index_min(code, start, end, frequence='1min', ip=None,
                           port=None):
    '指数分钟线'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    type_ = ''

    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    if str(frequence) in ['5', '5m', '5min', 'five']:
        frequence, type_ = 0, '5min'
        lens = 48 * lens
    elif str(frequence) in ['1', '1m', '1min', 'one']:
        frequence, type_ = 8, '1min'
        lens = 240 * lens
    elif str(frequence) in ['15', '15m', '15min', 'fifteen']:
        frequence, type_ = 1, '15min'
        lens = 16 * lens
    elif str(frequence) in ['30', '30m', '30min', 'half']:
        frequence, type_ = 2, '30min'
        lens = 8 * lens
    elif str(frequence) in ['60', '60m', '60min', '1h']:
        frequence, type_ = 3, '60min'
        lens = 4 * lens

    if lens > 20800:
        lens = 20800
    with api.connect(ip, port):

        if str(code)[0] in ['5', '1']:  # ETF
            data = pd.concat([api.to_df(api.get_security_bars(
                frequence, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0,
                code, (int(lens / 800) - i) * 800, 800))
                for i in range(int(lens / 800) + 1)], axis=0, sort=False)
        else:
            data = pd.concat([api.to_df(api.get_index_bars(
                frequence, 1 if str(code)[0] in ['0', '8', '9', '5'] else 0,
                code, (int(lens / 800) - i) * 800, 800))
                for i in range(int(lens / 800) + 1)], axis=0, sort=False)
        data = data \
            .assign(datetime=pd.to_datetime(data['datetime']),
                    code=str(code)) \
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                  inplace=False) \
            .assign(code=code,
                    date=data['datetime'].apply(lambda x: str(x)[0:10]),
                    date_stamp=data['datetime'].apply(
                        lambda x: QA_util_date_stamp(x)),
                    time_stamp=data['datetime'].apply(
                        lambda x: QA_util_time_stamp(x)),
                    type=type_).set_index('datetime', drop=False,
                                          inplace=False)[start:end]
        # data
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_index_latest(code, frequence='day', ip=None, port=None):
    ip, port = get_mainmarket_ip(ip, port)
    code = [code] if isinstance(code, str) else code
    api = TdxHq_API(multithread=True)

    if frequence in ['w', 'W', 'Week', 'week']:
        frequence = 5
    elif frequence in ['month', 'M', 'm', 'Month']:
        frequence = 6
    elif frequence in ['Q', 'Quarter', 'q']:
        frequence = 10
    elif frequence in ['y', 'Y', 'year', 'Year']:
        frequence = 11
    elif frequence in ['5', '5m', '5min', 'five']:
        frequence = 0
    elif frequence in ['1', '1m', '1min', 'one']:
        frequence = 8
    elif frequence in ['15', '15m', '15min', 'fifteen']:
        frequence = 1
    elif frequence in ['30', '30m', '30min', 'half']:
        frequence = 2
    elif frequence in ['60', '60m', '60min', '1h']:
        frequence = 3
    else:
        frequence = 9

    with api.connect(ip, port):
        data = []
        for item in code:
            if str(item)[0] in ['5', '1']:  # ETF
                data.append(api.to_df(api.get_security_bars(frequence,
                                                            1 if str(item)[
                                                                0] in [
                                                                '0', '8',
                                                                     '9',
                                                                     '5'] else 0,
                                                            item, 0,
                                                            1)).assign(
                    code=item))
            else:
                data.append(api.to_df(api.get_index_bars(frequence,
                                                         1 if str(item)[0] in [
                                                             '0', '8', '9',
                                                             '5'] else 0, item,
                                                         0, 1)).assign(
                    code=item))
        data = pd.concat(data, axis=0, sort=False)
        return data \
            .assign(date=pd.to_datetime(data['datetime']
                                        .apply(lambda x: x[0:10])),
                    date_stamp=data['datetime']
                    .apply(lambda x: QA_util_date_stamp(str(x[0:10])))) \
            .set_index('date', drop=False) \
            .drop(['year', 'month', 'day', 'hour', 'minute', 'datetime'],
                  axis=1)


def __QA_fetch_get_stock_transaction(code, day, retry, api):
    batch_size = 2000  # 800 or 2000 ? 2000 maybe also works
    data_arr = []
    max_offset = 21
    cur_offset = 0
    type_ = 'tick'
    while cur_offset <= max_offset:
        one_chunk = api.get_history_transaction_data(
            _select_market_code(str(code)), str(code), cur_offset * batch_size,
            batch_size, QA_util_date_str2int(day))
        if one_chunk is None or one_chunk == []:
            break
        data_arr = one_chunk + data_arr
        cur_offset += 1
    data_ = api.to_df(data_arr)

    for _ in range(retry):
        if len(data_) < 2:
            return __QA_fetch_get_stock_transaction(code, day, 0, api)
        else:
            data_ = data_.assign(
                date=day,
                datetime=pd.to_datetime(data_['time'].apply(
                    lambda x: str(day) + ' ' + x)),
                code=str(code))
            data_ = data_.assign(date_stamp=data_['datetime'].apply(lambda x: QA_util_date_stamp(x)),
                                 time_stamp=data_['datetime'].apply(
                                     lambda x: QA_util_time_stamp(x)),
                                 type=type_,
                                 order=range(len(data_.index))).set_index('datetime', drop=False)
            data_['datetime'] = data_['datetime'].apply(lambda x: str(x)[0:19])
            return data_


def __QA_fetch_get_index_transaction(code, day, retry, api):
    batch_size = 2000  # 800 or 2000 ? 2000 maybe also works
    data_arr = []
    max_offset = 21
    cur_offset = 0
    type_ = 'tick'
    while cur_offset <= max_offset:
        one_chunk = api.get_history_transaction_data(
            _select_index_code(str(code)), str(code), cur_offset * batch_size,
            batch_size, QA_util_date_str2int(day))
        if one_chunk is None or one_chunk == []:
            break
        data_arr = one_chunk + data_arr
        cur_offset += 1
    data_ = api.to_df(data_arr)

    for _ in range(retry):
        if len(data_) < 2:
            return __QA_fetch_get_index_transaction(code, day, 0, api)
        else:
            data_ = data_.assign(
                date=day,
                datetime=pd.to_datetime(data_['time'].apply(
                    lambda x: str(day) + ' ' + x)),
                code=str(code))
            data_ = data_.assign(date_stamp=data_['datetime'].apply(lambda x: QA_util_date_stamp(x)),
                                 time_stamp=data_['datetime'].apply(
                                     lambda x: QA_util_time_stamp(x)),
                                 type=type_,
                                 order=range(len(data_.index))).set_index('datetime', drop=False)
            data_['datetime'] = data_['datetime'].apply(lambda x: str(x)[0:19])
            return data_


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_transaction(code, start, end, retry=2, ip=None,
                                   port=None):
    '''
    :param code: 股票代码
    :param start: 开始日期
    :param end:  结束日期
    :param retry: 重新尝试次数
    :param ip: 地址
    :param port: 端口
    :return:
    '''
    '历史分笔成交 buyorsell 1--sell 0--buy 2--盘前'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()

    real_start, real_end = QA_util_get_real_datelist(start, end)
    if real_start is None:
        return None
    real_id_range = []
    with api.connect(ip, port):
        data = pd.DataFrame()
        for index_ in range(trade_date_sse.index(real_start),
                            trade_date_sse.index(real_end) + 1):

            try:
                data_ = __QA_fetch_get_stock_transaction(
                    code, trade_date_sse[index_], retry, api)
                if len(data_) < 1:
                    return None
            except:
                QA_util_log_info(
                    'Wrong in Getting {} history transaction data in day {}'.format(
                        code, trade_date_sse[index_]))
            else:
                QA_util_log_info(
                    'Successfully Getting {} history transaction data in day {}'.format(
                        code, trade_date_sse[index_]))
                data = data.append(data_)
        if len(data) > 0:

            return data.assign(
                datetime=data['datetime'].apply(lambda x: str(x)[0:19]))
        else:
            return None


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_index_transaction(code, start, end, retry=2, ip=None,
                                   port=None):
    '''
    :param code: 指数代码
    :param start: 开始日期
    :param end:  结束日期
    :param retry: 重新尝试次数
    :param ip: 地址
    :param port: 端口
    :return:
    '''
    '历史分笔成交 buyorsell 1--sell 0--buy 2--盘前'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()

    real_start, real_end = QA_util_get_real_datelist(start, end)
    if real_start is None:
        return None
    real_id_range = []
    with api.connect(ip, port):
        data = pd.DataFrame()
        for index_ in range(trade_date_sse.index(real_start),
                            trade_date_sse.index(real_end) + 1):

            try:
                data_ = __QA_fetch_get_index_transaction(
                    code, trade_date_sse[index_], retry, api)
                if len(data_) < 1:
                    return None
            except:
                QA_util_log_info(
                    'Wrong in Getting {} history transaction data in day {}'.format(
                        code, trade_date_sse[index_]))
            else:
                QA_util_log_info(
                    'Successfully Getting {} history transaction data in day {}'.format(
                        code, trade_date_sse[index_]))
                data = data.append(data_)
        if len(data) > 0:

            return data.assign(
                datetime=data['datetime'].apply(lambda x: str(x)[0:19]))
        else:
            return None


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_transaction_realtime(code, ip=None, port=None):
    '实时分笔成交 包含集合竞价 buyorsell 1--sell 0--buy 2--盘前'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    try:
        with api.connect(ip, port):
            data = pd.DataFrame()
            data = pd.concat([api.to_df(api.get_transaction_data(
                _select_market_code(str(code)), code, (2 - i) * 2000, 2000))
                for i in range(3)], axis=0, sort=False)
            if 'value' in data.columns:
                data = data.drop(['value'], axis=1)
            data = data.dropna()
            day = datetime.date.today()
            return data.assign(
                date=str(day),
                datetime=pd.to_datetime(data['time'].apply(
                    lambda x: str(day) + ' ' + str(x))),
                code=str(code),
                order=range(len(data.index))).set_index('datetime', drop=False,
                                                        inplace=False)
    except:
        return None


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_xdxr(code, ip=None, port=None):
    '除权除息'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    market_code = _select_market_code(code)
    with api.connect(ip, port):
        category = {
            '1': '除权除息', '2': '送配股上市', '3': '非流通股上市', '4': '未知股本变动',
            '5': '股本变化',
            '6': '增发新股', '7': '股份回购', '8': '增发新股上市', '9': '转配股上市',
            '10': '可转债上市',
            '11': '扩缩股', '12': '非流通股缩股', '13': '送认购权证', '14': '送认沽权证'}
        data = api.to_df(api.get_xdxr_info(market_code, code))
        if len(data) >= 1:
            data = data \
                .assign(date=pd.to_datetime(data[['year', 'month', 'day']])) \
                .drop(['year', 'month', 'day'], axis=1) \
                .assign(category_meaning=data['category'].apply(
                    lambda x: category[str(x)])) \
                .assign(code=str(code)) \
                .rename(index=str, columns={'panhouliutong': 'liquidity_after',
                                            'panqianliutong': 'liquidity_before',
                                            'houzongguben': 'shares_after',
                                            'qianzongguben': 'shares_before'}) \
                .set_index('date', drop=False, inplace=False)
            return data.assign(date=data['date'].apply(lambda x: str(x)[0:10]))
        else:
            return None


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_info(code, ip=None, port=None):
    '股票基本信息'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    market_code = _select_market_code(code)
    with api.connect(ip, port):
        return api.to_df(api.get_finance_info(market_code, code))


@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_get_stock_block(ip=None, port=None):
    '板块数据'
    ip, port = get_mainmarket_ip(ip, port)
    api = TdxHq_API()
    with api.connect(ip, port):

        data = pd.concat([api.to_df(
            api.get_and_parse_block_info("block_gn.dat")).assign(type='gn'),
            api.to_df(api.get_and_parse_block_info(
                "block.dat")).assign(type='yb'),
            api.to_df(api.get_and_parse_block_info(
                "block_zs.dat")).assign(type='zs'),
            api.to_df(api.get_and_parse_block_info(
                "block_fg.dat")).assign(type='fg')], sort=False)

        if len(data) > 10:
            return data.assign(source='tdx').drop(['block_type', 'code_index'],
                                                  axis=1).set_index('code',
                                                                    drop=False,
                                                                    inplace=False).drop_duplicates()
        else:
            QA_util_log_info('Wrong with fetch block ')


"""
http://www.tdx.com.cn/page_46.html
    market  category      name short_name
        1         1       临时股         TP
## 期权 OPTION
        4        12    郑州商品期权         OZ
        5        12    大连商品期权         OD
        6        12    上海商品期权         OS
        7        12     中金所期权         OJ
        8        12    上海股票期权         QQ
        9        12    深圳股票期权      (推测)
## 汇率 EXCHANGERATE
       10         4      基本汇率         FE
       11         4      交叉汇率         FX
## 全球 GLOBALMARKET
       37        11  全球指数(静态)         FW
       12         5      国际指数         WI
       13         3     国际贵金属         GO
       14         3      伦敦金属         LM
       15         3      伦敦石油         IP
       16         3      纽约商品         CO
       17         3      纽约石油         NY
       18         3      芝加哥谷         CB
       19         3     东京工业品         TO
       20         3      纽约期货         NB
       77         3     新加坡期货         SX
       39         3      马来期货         ML
# 港股 HKMARKET
       27         5      香港指数         FH
       31         2      香港主板         KH
       48         2     香港创业板         KG
       49         2      香港基金         KT
       43         1     B股转H股         HB
# 期货现货
       42         3      商品指数         TI
       60         3    主力期货合约         MA
       28         3      郑州商品         QZ
       29         3      大连商品         QD
       30         3      上海期货         QS
       46        11      上海黄金         SG
       47         3     中金所期货         CZ
       50         3      渤海商品         BH
       76         3      齐鲁商品         QL
## 基金 
       33         8     开放式基金         FU
       34         9     货币型基金         FB
       35         8  招商理财产品         LC
       36         9  招商货币产品         LB
       56         8    阳光私募基金         TA
       57         8    券商集合理财         TB
       58         9    券商货币理财         TC
## 美股 USA STOCK
       74        13      美国股票         US
       40        11     中国概念股         CH
       41        11    美股知名公司         MG
## 其他
       38        10      宏观指标         HG
       44         1      股转系统         SB
       54         6     国债预发行         GY
       62         5      中证指数         ZZ
       70         5    扩展板块指数         UZ
       71         2     港股通             GH
"""

"""
扩展行情
首先会初始化/存储一个
市场状况  extension_market_info
代码对应表 extension_market_list
"""

global extension_market_info
extension_market_info = None

global extension_market_list
extension_market_list = None


def QA_fetch_get_extensionmarket_count(ip=None, port=None):
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    with apix.connect(ip, port):
        global extension_market_info
        extension_market_info = apix.to_df(apix.get_markets())
        return extension_market_info


def QA_fetch_get_extensionmarket_info(ip=None, port=None):
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    with apix.connect(ip, port):
        global extension_market_info
        extension_market_info = apix.to_df(apix.get_markets())
        return extension_market_info


def QA_fetch_get_extensionmarket_list(ip=None, port=None):
    '期货代码list'
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    with apix.connect(ip, port):
        num = apix.get_instrument_count()
        return pd.concat([apix.to_df(
            apix.get_instrument_info((int(num / 500) - i) * 500, 500))
            for i in range(int(num / 500) + 1)], axis=0, sort=False).set_index('code',
                                                                               drop=False)


def QA_fetch_get_future_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    42         3      商品指数         TI
    60         3    主力期货合约         MA
    28         3      郑州商品         QZ
    29         3      大连商品         QD
    30         3      上海期货(原油+贵金属)  QS
    47         3     中金所期货         CZ
    50         3      渤海商品         BH
    76         3      齐鲁商品         QL
    46        11      上海黄金(伦敦金T+D)         SG
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query(
        'market==42 or market==28 or market==29 or market==30 or market==47')


def QA_fetch_get_globalindex_list(ip=None, port=None):
    """全球指数列表
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
       37        11  全球指数(静态)         FW
       12         5      国际指数         WI
    """
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('market==12 or market==37')


def QA_fetch_get_goods_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    42         3      商品指数         TI
    60         3    主力期货合约         MA
    28         3      郑州商品         QZ
    29         3      大连商品         QD
    30         3      上海期货(原油+贵金属)  QS
    47         3     中金所期货         CZ
    50         3      渤海商品         BH
    76         3      齐鲁商品         QL
    46        11      上海黄金(伦敦金T+D)         SG
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query(
        'market==50 or market==76 or market==46')


def QA_fetch_get_globalfuture_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
       14         3      伦敦金属         LM
       15         3      伦敦石油         IP
       16         3      纽约商品         CO
       17         3      纽约石油         NY
       18         3      芝加哥谷         CB
       19         3     东京工业品         TO
       20         3      纽约期货         NB
       77         3     新加坡期货         SX
       39         3      马来期货         ML
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query(
        'market==14 or market==15 or market==16 or market==17 or market==18 or market==19 or market==20 or market==77 or market==39')


def QA_fetch_get_hkstock_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
# 港股 HKMARKET
       27         5      香港指数         FH
       31         2      香港主板         KH
       48         2     香港创业板         KG
       49         2      香港基金         KT
       43         1     B股转H股         HB
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('market==31 or market==48')


def QA_fetch_get_hkindex_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
# 港股 HKMARKET
       27         5      香港指数         FH
       31         2      香港主板         KH
       48         2     香港创业板         KG
       49         2      香港基金         KT
       43         1     B股转H股         HB
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('market==27')


def QA_fetch_get_hkfund_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    # 港股 HKMARKET
        27         5      香港指数         FH
        31         2      香港主板         KH
        48         2     香港创业板         KG
        49         2      香港基金         KT
        43         1     B股转H股         HB
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('market==49')


def QA_fetch_get_usstock_list(ip=None, port=None):
    """[summary]
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    ## 美股 USA STOCK
        74        13      美国股票         US
        40        11     中国概念股         CH
        41        11    美股知名公司         MG
    """

    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query(
        'market==74 or market==40 or market==41')


def QA_fetch_get_macroindex_list(ip=None, port=None):
    """宏观指标列表
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
        38        10      宏观指标         HG
    """
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('market==38')


def QA_fetch_get_option_all_contract_time_to_market():
    '''
    #🛠todo 获取期权合约的上市日期 ？ 暂时没有。
    :return: list Series
    '''
    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code
    '''
    fix here : 
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    result['meaningful_name'] = None
    C:\work_new\QUANTAXIS\QUANTAXIS\QAFetch\QATdx.py:1468: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    '''
    # df = pd.DataFrame()
    rows = []

    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  # 10001215
        strName = result.loc[idx, 'name']  # 510050C9M03200
        strDesc = result.loc[idx, 'desc']  # 10001215

        # 50etf
        if strName.startswith("510050"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )

            if strName.startswith("510050C"):
                putcall = '50ETF,认购期权'
            elif strName.startswith("510050P"):
                putcall = '50ETF,认沽期权'
            else:
                putcall = "Unkown code name ： " + strName

            expireMonth = strName[7:8]
            if expireMonth == 'A':
                expireMonth = "10月"
            elif expireMonth == 'B':
                expireMonth = "11月"
            elif expireMonth == 'C':
                expireMonth = "12月"
            else:
                expireMonth = expireMonth + '月'

            # 第12位期初设为“M”，并根据合约调整次数按照“A”至“Z”依序变更，如变更为“A”表示期权合约发生首次调整，变更为“B”表示期权合约发生第二次调整，依此类推；
            # fix here : M ??
            if strName[8:9] == "M":
                adjust = "未调整"
            elif strName[8:9] == 'A':
                adjust = " 第1次调整"
            elif strName[8:9] == 'B':
                adjust = " 第2调整"
            elif strName[8:9] == 'C':
                adjust = " 第3次调整"
            elif strName[8:9] == 'D':
                adjust = " 第4次调整"
            elif strName[8:9] == 'E':
                adjust = " 第5次调整"
            elif strName[8:9] == 'F':
                adjust = " 第6次调整"
            elif strName[8:9] == 'G':
                adjust = " 第7次调整"
            elif strName[8:9] == 'H':
                adjust = " 第8次调整"
            elif strName[8:9] == 'I':
                adjust = " 第9次调整"
            elif strName[8:9] == 'J':
                adjust = " 第10次调整"
            else:
                adjust = " 第10次以上的调整，调整代码 %s" + strName[8:9]

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期月份:%s,%s,行权价:%s' % (
                putcall, expireMonth, adjust, executePrice)

            row = result.loc[idx]
            rows.append(row)

        # 300etf
        if strName.startswith("510300"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )

            if strName.startswith("510300C"):
                putcall = '300ETF,认购期权'
            elif strName.startswith("510300P"):
                putcall = '300ETF,认沽期权'
            else:
                putcall = "Unkown code name ： " + strName

            expireMonth = strName[7:8]
            if expireMonth == 'A':
                expireMonth = "10月"
            elif expireMonth == 'B':
                expireMonth = "11月"
            elif expireMonth == 'C':
                expireMonth = "12月"
            else:
                expireMonth = expireMonth + '月'

            # 第12位期初设为“M”，并根据合约调整次数按照“A”至“Z”依序变更，如变更为“A”表示期权合约发生首次调整，变更为“B”表示期权合约发生第二次调整，依此类推；
            # fix here : M ??
            if strName[8:9] == "M":
                adjust = "未调整"
            elif strName[8:9] == 'A':
                adjust = " 第1次调整"
            elif strName[8:9] == 'B':
                adjust = " 第2调整"
            elif strName[8:9] == 'C':
                adjust = " 第3次调整"
            elif strName[8:9] == 'D':
                adjust = " 第4次调整"
            elif strName[8:9] == 'E':
                adjust = " 第5次调整"
            elif strName[8:9] == 'F':
                adjust = " 第6次调整"
            elif strName[8:9] == 'G':
                adjust = " 第7次调整"
            elif strName[8:9] == 'H':
                adjust = " 第8次调整"
            elif strName[8:9] == 'I':
                adjust = " 第9次调整"
            elif strName[8:9] == 'J':
                adjust = " 第10次调整"
            else:
                adjust = " 第10次以上的调整，调整代码 %s" + strName[8:9]

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期月份:%s,%s,行权价:%s' % (
                putcall, expireMonth, adjust, executePrice)

            row = result.loc[idx]
            rows.append(row)

        elif strName.startswith("SR"):
            # print("SR")
            # SR1903-P-6500
            expireYear = strName[2:4]
            expireMonth = strName[4:6]

            put_or_call = strName[7:8]
            if put_or_call == "P":
                putcall = "白糖,认沽期权"
            elif put_or_call == "C":
                putcall = "白糖,认购期权"
            else:
                putcall = "Unkown code name ： " + strName

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期年月份:%s%s,行权价:%s' % (
                putcall, expireYear, expireMonth, executePrice)

            row = result.loc[idx]
            rows.append(row)

            pass
        elif strName.startswith("CU"):
            # print("CU")

            # print("SR")
            # SR1903-P-6500
            expireYear = strName[2:4]
            expireMonth = strName[4:6]

            put_or_call = strName[7:8]
            if put_or_call == "P":
                putcall = "铜,认沽期权"
            elif put_or_call == "C":
                putcall = "铜,认购期权"
            else:
                putcall = "Unkown code name ： " + strName

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期年月份:%s%s,行权价:%s' % (
                putcall, expireYear, expireMonth, executePrice)

            row = result.loc[idx]
            rows.append(row)

            pass
        # todo 新增期权品种 棉花，玉米， 天然橡胶
        elif strName.startswith("RU"):
            # print("M")
            # print(strName)
            ##
            expireYear = strName[2:4]
            expireMonth = strName[4:6]

            put_or_call = strName[7:8]
            if put_or_call == "P":
                putcall = "天然橡胶,认沽期权"
            elif put_or_call == "C":
                putcall = "天然橡胶,认购期权"
            else:
                putcall = "Unkown code name ： " + strName

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期年月份:%s%s,行权价:%s' % (
                putcall, expireYear, expireMonth, executePrice)

            row = result.loc[idx]
            rows.append(row)

            pass

        elif strName.startswith("CF"):
            # print("M")
            # print(strName)
            ##
            expireYear = strName[2:4]
            expireMonth = strName[4:6]

            put_or_call = strName[7:8]
            if put_or_call == "P":
                putcall = "棉花,认沽期权"
            elif put_or_call == "C":
                putcall = "棉花,认购期权"
            else:
                putcall = "Unkown code name ： " + strName

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期年月份:%s%s,行权价:%s' % (
                putcall, expireYear, expireMonth, executePrice)

            row = result.loc[idx]
            rows.append(row)

            pass

        elif strName.startswith("M"):
            # print("M")
            # print(strName)
            ##
            expireYear = strName[1:3]
            expireMonth = strName[3:5]

            put_or_call = strName[6:7]
            if put_or_call == "P":
                putcall = "豆粕,认沽期权"
            elif put_or_call == "C":
                putcall = "豆粕,认购期权"
            else:
                putcall = "Unkown code name ： " + strName

            executePrice = strName[8:]
            result.loc[idx, 'meaningful_name'] = '%s,到期年月份:%s%s,行权价:%s' % (
                putcall, expireYear, expireMonth, executePrice)

            row = result.loc[idx]
            rows.append(row)

            pass
        elif strName.startswith("C") and strName[1] != 'F' and strName[
                1] != 'U':
            # print("M")
            # print(strName)
            ##
            expireYear = strName[1:3]
            expireMonth = strName[3:5]

            put_or_call = strName[6:7]
            if put_or_call == "P":
                putcall = "玉米,认沽期权"
            elif put_or_call == "C":
                putcall = "玉米,认购期权"
            else:
                putcall = "Unkown code name ： " + strName

            executePrice = strName[8:]
            result.loc[idx, 'meaningful_name'] = '%s,到期年月份:%s%s,行权价:%s' % (
                putcall, expireYear, expireMonth, executePrice)

            row = result.loc[idx]
            rows.append(row)

            pass
        else:

            result.loc[idx, 'meaningful_name'] = "未知类型合约"
            row = result.loc[idx]
            rows.append(row)

    return rows


###############################################################
# 期权合约分类
###############################################################


def QA_fetch_get_option_list(ip=None, port=None):
    """期权列表
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    ## 期权 OPTION
            1        12    临时期权(主要是50ETF)
            4        12    郑州商品期权         OZ
            5        12    大连商品期权         OD
            6        12    上海商品期权         OS
            7        12     中金所期权         OJ
            8        12    上海股票期权         QQ
            9        12    深圳股票期权      (推测)
    """
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('category==12 and market!=1')


###############################################################
# 期权合约分类
# 50ETF
# 棉花
# 天然橡胶
# 铜
# 玉米
# 豆粕
# 白糖
# 红枣
###############################################################
# 50ETF
###############################################################
def QA_fetch_get_option_50etf_contract_time_to_market():
    '''
        #🛠todo 获取期权合约的上市日期 ？ 暂时没有。
        :return: list Series
        '''
    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code
    '''
    fix here : 
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    result['meaningful_name'] = None
    C:\work_new\QUANTAXIS\QUANTAXIS\QAFetch\QATdx.py:1468: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    '''
    # df = pd.DataFrame()
    rows = []

    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  # 10001215
        strName = result.loc[idx, 'name']  # 510050C9M03200
        strDesc = result.loc[idx, 'desc']  # 10001215

        if strName.startswith("510050"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )

            if strName.startswith("510050C"):
                putcall = '50ETF,认购期权'
            elif strName.startswith("510050P"):
                putcall = '50ETF,认沽期权'
            else:
                putcall = "Unkown code name ： " + strName

            expireMonth = strName[7:8]
            if expireMonth == 'A':
                expireMonth = "10月"
            elif expireMonth == 'B':
                expireMonth = "11月"
            elif expireMonth == 'C':
                expireMonth = "12月"
            else:
                expireMonth = expireMonth + '月'

            # 第12位期初设为“M”，并根据合约调整次数按照“A”至“Z”依序变更，如变更为“A”表示期权合约发生首次调整，变更为“B”表示期权合约发生第二次调整，依此类推；
            # fix here : M ??
            if strName[8:9] == "M":
                adjust = "未调整"
            elif strName[8:9] == 'A':
                adjust = " 第1次调整"
            elif strName[8:9] == 'B':
                adjust = " 第2调整"
            elif strName[8:9] == 'C':
                adjust = " 第3次调整"
            elif strName[8:9] == 'D':
                adjust = " 第4次调整"
            elif strName[8:9] == 'E':
                adjust = " 第5次调整"
            elif strName[8:9] == 'F':
                adjust = " 第6次调整"
            elif strName[8:9] == 'G':
                adjust = " 第7次调整"
            elif strName[8:9] == 'H':
                adjust = " 第8次调整"
            elif strName[8:9] == 'I':
                adjust = " 第9次调整"
            elif strName[8:9] == 'J':
                adjust = " 第10次调整"
            else:
                adjust = " 第10次以上的调整，调整代码 %s" + strName[8:9]

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期月份:%s,%s,行权价:%s' % (
                putcall, expireMonth, adjust, executePrice)

            row = result.loc[idx]
            rows.append(row)
    return rows


def QA_fetch_get_option_300etf_contract_time_to_market():
    '''
        #🛠todo 获取期权合约的上市日期 ？ 暂时没有。
        :return: list Series
        '''
    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code
    '''
    fix here : 
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
    result['meaningful_name'] = None
    C:\work_new\QUANTAXIS\QUANTAXIS\QAFetch\QATdx.py:1468: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    '''
    # df = pd.DataFrame()
    rows = []

    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  # 10001215
        strName = result.loc[idx, 'name']  # 510300C9M03200
        strDesc = result.loc[idx, 'desc']  # 10001215

        if strName.startswith("510300"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )

            if strName.startswith("510050C"):
                putcall = '300ETF,认购期权'
            elif strName.startswith("510050P"):
                putcall = '300ETF,认沽期权'
            else:
                putcall = "Unkown code name ： " + strName

            expireMonth = strName[7:8]
            if expireMonth == 'A':
                expireMonth = "10月"
            elif expireMonth == 'B':
                expireMonth = "11月"
            elif expireMonth == 'C':
                expireMonth = "12月"
            else:
                expireMonth = expireMonth + '月'

            # 第12位期初设为“M”，并根据合约调整次数按照“A”至“Z”依序变更，如变更为“A”表示期权合约发生首次调整，变更为“B”表示期权合约发生第二次调整，依此类推；
            # fix here : M ??
            if strName[8:9] == "M":
                adjust = "未调整"
            elif strName[8:9] == 'A':
                adjust = " 第1次调整"
            elif strName[8:9] == 'B':
                adjust = " 第2调整"
            elif strName[8:9] == 'C':
                adjust = " 第3次调整"
            elif strName[8:9] == 'D':
                adjust = " 第4次调整"
            elif strName[8:9] == 'E':
                adjust = " 第5次调整"
            elif strName[8:9] == 'F':
                adjust = " 第6次调整"
            elif strName[8:9] == 'G':
                adjust = " 第7次调整"
            elif strName[8:9] == 'H':
                adjust = " 第8次调整"
            elif strName[8:9] == 'I':
                adjust = " 第9次调整"
            elif strName[8:9] == 'J':
                adjust = " 第10次调整"
            else:
                adjust = " 第10次以上的调整，调整代码 %s" + strName[8:9]

            executePrice = strName[9:]
            result.loc[idx, 'meaningful_name'] = '%s,到期月份:%s,%s,行权价:%s' % (
                putcall, expireMonth, adjust, executePrice)

            row = result.loc[idx]
            rows.append(row)
    return rows


###############################################################
# 棉花
###############################################################
def QA_fetch_get_commodity_option_CF_contract_time_to_market():
    '''
    铜期权  CU 开头   上期证
    豆粕    M开头     大商所
    白糖    SR开头    郑商所
    测试中发现，行情不太稳定 ？ 是 通达信 IP 的问题 ？
    '''

    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code

    # df = pd.DataFrame()
    rows = []
    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  #
        strName = result.loc[idx, 'name']  #
        strDesc = result.loc[idx, 'desc']  #

        # 如果同时获取， 不同的 期货交易所数据， pytdx会 connection close 连接中断？
        # if strName.startswith("CU") or strName.startswith("M") or strName.startswith('SR'):
        if strName.startswith("CF"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )
            row = result.loc[idx]
            rows.append(row)

    return rows

    pass

###############################################################
# 天然橡胶
###############################################################


def QA_fetch_get_commodity_option_RU_contract_time_to_market():
    '''
    铜期权  CU 开头   上期证
    豆粕    M开头     大商所
    白糖    SR开头    郑商所
    测试中发现，行情不太稳定 ？ 是 通达信 IP 的问题 ？
    '''

    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code

    # df = pd.DataFrame()
    rows = []
    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  #
        strName = result.loc[idx, 'name']  #
        strDesc = result.loc[idx, 'desc']  #

        # 如果同时获取， 不同的 期货交易所数据， pytdx会 connection close 连接中断？
        # if strName.startswith("CU") or strName.startswith("M") or strName.startswith('SR'):
        if strName.startswith("RU"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )
            row = result.loc[idx]
            rows.append(row)

    return rows

    pass

###############################################################
# 玉米
###############################################################


def QA_fetch_get_commodity_option_C_contract_time_to_market():
    '''
    铜期权  CU 开头   上期证
    豆粕    M开头     大商所
    白糖    SR开头    郑商所
    测试中发现，行情不太稳定 ？ 是 通达信 IP 的问题 ？
    '''

    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code

    # df = pd.DataFrame()
    rows = []
    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  #
        strName = result.loc[idx, 'name']  #
        strDesc = result.loc[idx, 'desc']  #

        # 如果同时获取， 不同的 期货交易所数据， pytdx会 connection close 连接中断？
        # if strName.startswith("CU") or strName.startswith("M") or strName.startswith('SR'):
        if strName.startswith("C") and strName[1] != 'F' and strName[1] != 'U':
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )
            row = result.loc[idx]
            rows.append(row)

    return rows

    pass

###############################################################
# 铜
###############################################################


def QA_fetch_get_commodity_option_CU_contract_time_to_market():
    '''
    #🛠todo 获取期权合约的上市日期 ？ 暂时没有。
    :return: list Series
    '''
    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code

    # df = pd.DataFrame()
    rows = []
    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  #
        strName = result.loc[idx, 'name']  #
        strDesc = result.loc[idx, 'desc']  #

        # 如果同时获取， 不同的 期货交易所数据， pytdx会 connection close 连接中断？
        # if strName.startswith("CU") or strName.startswith("M") or strName.startswith('SR'):
        if strName.startswith("CU"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )
            row = result.loc[idx]
            rows.append(row)

    return rows


###############################################################
# 豆粕
###############################################################
def QA_fetch_get_commodity_option_M_contract_time_to_market():
    '''
    #🛠todo 获取期权合约的上市日期 ？ 暂时没有。
    :return: list Series
    '''
    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code
    '''
    铜期权  CU 开头   上期证
    豆粕    M开头     大商所
    白糖    SR开头    郑商所
    '''
    # df = pd.DataFrame()
    rows = []
    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  #
        strName = result.loc[idx, 'name']  #
        strDesc = result.loc[idx, 'desc']  #

        # 如果同时获取， 不同的 期货交易所数据， pytdx connection close 连接中断？
        # if strName.startswith("CU") or strName.startswith("M") or strName.startswith('SR'):
        if strName.startswith("M"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )
            row = result.loc[idx]
            rows.append(row)

    return rows


###############################################################
# 白糖
###############################################################
def QA_fetch_get_commodity_option_SR_contract_time_to_market():
    '''
    #🛠todo 获取期权合约的上市日期 ？ 暂时没有。
    :return: list Series
    '''
    result = QA_fetch_get_option_list('tdx')
    # pprint.pprint(result)
    #  category  market code name desc  code
    '''
    铜期权  CU 开头   上期证
    豆粕    M开头     大商所
    白糖    SR开头    郑商所
    '''
    # df = pd.DataFrame()
    rows = []
    result['meaningful_name'] = None
    for idx in result.index:
        # pprint.pprint((idx))
        strCategory = result.loc[idx, "category"]
        strMarket = result.loc[idx, "market"]
        strCode = result.loc[idx, "code"]  #
        strName = result.loc[idx, 'name']  #
        strDesc = result.loc[idx, 'desc']  #

        # 如果同时获取， 不同的 期货交易所数据， pytdx connection close 连接中断？
        # if strName.startswith("CU") or strName.startswith("M") or strName.startswith('SR'):
        if strName.startswith("SR"):
            # print(strCategory,' ', strMarket, ' ', strCode, ' ', strName, ' ', strDesc, )
            row = result.loc[idx]
            rows.append(row)

    return rows

#########################################################################################


def QA_fetch_get_exchangerate_list(ip=None, port=None):
    """汇率列表
    Keyword Arguments:
        ip {[type]} -- [description] (default: {None})
        port {[type]} -- [description] (default: {None})
    ## 汇率 EXCHANGERATE
        10         4      基本汇率         FE
        11         4      交叉汇率         FX
    """
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    return extension_market_list.query('market==10 or market==11').query(
        'category==4')


def QA_fetch_get_future_day(code, start_date, end_date, frequence='day',
                            ip=None, port=None):
    '期货数据 日线'
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    start_date = str(start_date)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    with apix.connect(ip, port):
        code_market = extension_market_list.query(
            'code=="{}"'.format(code)).iloc[0]

        data = pd.concat(
            [apix.to_df(apix.get_instrument_bars(
                _select_type(frequence),
                int(code_market.market),
                str(code),
                (int(lens / 700) - i) * 700, 700)) for i in
                range(int(lens / 700) + 1)],
            axis=0, sort=False)

        try:

            # 获取商品期货会报None
            data = data.assign(
                date=data['datetime'].apply(lambda x: str(x[0:10]))).assign(
                code=str(code), date_stamp=data['datetime'].apply(
                    lambda x: QA_util_date_stamp(str(x)[0:10]))).set_index('date',
                                                                           drop=False,
                                                                           inplace=False)

        except Exception as exp:
            print("code is ", code)
            print(exp.__str__)
            return None

        return data.drop(
            ['year', 'month', 'day', 'hour', 'minute', 'datetime'], axis=1)[
            start_date:end_date].assign(
            date=data['date'].apply(lambda x: str(x)[0:10]))


def QA_fetch_get_future_min(code, start, end, frequence='1min', ip=None,
                            port=None):
    '期货数据 分钟线'
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    type_ = ''
    start_date = str(start)[0:10]
    today_ = datetime.date.today()
    lens = QA_util_get_trade_gap(start_date, today_)
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    if str(frequence) in ['5', '5m', '5min', 'five']:
        frequence, type_ = 0, '5min'
        lens = 48 * lens * 2.5
    elif str(frequence) in ['1', '1m', '1min', 'one']:
        frequence, type_ = 8, '1min'
        lens = 240 * lens * 2.5
    elif str(frequence) in ['15', '15m', '15min', 'fifteen']:
        frequence, type_ = 1, '15min'
        lens = 16 * lens * 2.5
    elif str(frequence) in ['30', '30m', '30min', 'half']:
        frequence, type_ = 2, '30min'
        lens = 8 * lens * 2.5
    elif str(frequence) in ['60', '60m', '60min', '1h']:
        frequence, type_ = 3, '60min'
        lens = 4 * lens * 2.5
    if lens > 20800:
        lens = 20800

    # print(lens)
    with apix.connect(ip, port):

        code_market = extension_market_list.query(
            'code=="{}"'.format(code)).iloc[0]
        data = pd.concat([apix.to_df(
            apix.get_instrument_bars(frequence, int(code_market.market), str(
                code), (int(lens / 700) - i) * 700, 700)) for i in
            range(int(lens / 700) + 1)], axis=0, sort=False)
        # print(data)
        # print(data.datetime)
        data = data \
            .assign(tradetime=data['datetime'].apply(str), code=str(code),
                    datetime=pd.to_datetime(
                data['datetime'].apply(QA_util_future_to_realdatetime, 1))) \
            .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                  inplace=False) \
            .assign(date=data['datetime'].apply(lambda x: str(x)[0:10]),
                    date_stamp=data['datetime'].apply(
                        lambda x: QA_util_date_stamp(x)),
                    time_stamp=data['datetime'].apply(
                        lambda x: QA_util_time_stamp(x)),
                    type=type_).set_index('datetime', drop=False,
                                          inplace=False)
        return data.assign(datetime=data['datetime'].apply(lambda x: str(x)))[
            start:end].sort_index()


def __QA_fetch_get_future_transaction(code, day, retry, code_market, apix):
    batch_size = 1800  # 800 or 2000 ? 2000 maybe also works
    data_arr = []
    max_offset = 40
    cur_offset = 0

    while cur_offset <= max_offset:
        one_chunk = apix.get_history_transaction_data(
            code_market, str(code), QA_util_date_str2int(day),
            cur_offset * batch_size)

        if one_chunk is None or one_chunk == []:
            break
        data_arr = one_chunk + data_arr
        cur_offset += 1
    data_ = apix.to_df(data_arr)

    for _ in range(retry):
        if len(data_) < 2:
            import time
            time.sleep(1)
            return __QA_fetch_get_stock_transaction(code, day, 0, apix)
        else:
            return data_.assign(datetime=pd.to_datetime(data_['date'])).assign(
                date=str(day)) \
                .assign(code=str(code)).assign(
                order=range(len(data_.index))).set_index('datetime',
                                                         drop=False,
                                                         inplace=False)


def QA_fetch_get_future_transaction(code, start, end, retry=4, ip=None,
                                    port=None):
    '期货历史成交分笔'
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list
    real_start, real_end = QA_util_get_real_datelist(start, end)
    if real_start is None:
        return None
    real_id_range = []
    with apix.connect(ip, port):
        code_market = extension_market_list.query(
            'code=="{}"'.format(code)).iloc[0]
        data = pd.DataFrame()
        for index_ in range(trade_date_sse.index(real_start),
                            trade_date_sse.index(real_end) + 1):

            try:
                data_ = __QA_fetch_get_future_transaction(
                    code, trade_date_sse[index_], retry,
                    int(code_market.market), apix)
                if len(data_) < 1:
                    return None
            except Exception as e:
                print(e)
                QA_util_log_info(
                    'Wrong in Getting {} history transaction data in day {}'.format(
                        code, trade_date_sse[index_]))
            else:
                QA_util_log_info(
                    'Successfully Getting {} history transaction data in day {}'.format(
                        code, trade_date_sse[index_]))
                data = data.append(data_)
        if len(data) > 0:

            return data.assign(
                datetime=data['datetime'].apply(lambda x: str(x)[0:19]))
        else:
            return None


def QA_fetch_get_future_transaction_realtime(code, ip=None, port=None):
    '期货历史成交分笔'
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list

    code_market = extension_market_list.query(
        'code=="{}"'.format(code)).iloc[0]
    with apix.connect(ip, port):
        data = pd.DataFrame()
        data = pd.concat([apix.to_df(apix.get_transaction_data(
            int(code_market.market), code, (30 - i) * 1800), ) for i in
            range(31)], axis=0,sort=True)
        return data.assign(datetime=pd.to_datetime(data['date'])).assign(
            date=lambda x: str(x)[0:10]) \
            .assign(code=str(code)).assign(
            order=range(len(data.index))).set_index('datetime', drop=False,
                                                    inplace=False)


def QA_fetch_get_future_realtime(code, ip=None, port=None):
    '期货实时价格'
    ip, port = get_extensionmarket_ip(ip, port)
    apix = TdxExHq_API()
    global extension_market_list
    extension_market_list = QA_fetch_get_extensionmarket_list(
    ) if extension_market_list is None else extension_market_list
    __data = pd.DataFrame()
    code_market = extension_market_list.query(
        'code=="{}"'.format(code)).iloc[0]
    with apix.connect(ip, port):
        __data = apix.to_df(apix.get_instrument_quote(
            int(code_market.market), code))
        __data['datetime'] = datetime.datetime.now()

        # data = __data[['datetime', 'active1', 'active2', 'last_close', 'code', 'open', 'high', 'low', 'price', 'cur_vol',
        #                's_vol', 'b_vol', 'vol', 'ask1', 'ask_vol1', 'bid1', 'bid_vol1', 'ask2', 'ask_vol2',
        #                'bid2', 'bid_vol2', 'ask3', 'ask_vol3', 'bid3', 'bid_vol3', 'ask4',
        #                'ask_vol4', 'bid4', 'bid_vol4', 'ask5', 'ask_vol5', 'bid5', 'bid_vol5']]
        return __data.set_index(['datetime', 'code'])


QA_fetch_get_option_day = QA_fetch_get_future_day
QA_fetch_get_option_min = QA_fetch_get_future_min

QA_fetch_get_hkstock_day = QA_fetch_get_future_day
QA_fetch_get_hkstock_min = QA_fetch_get_future_min

QA_fetch_get_hkfund_day = QA_fetch_get_future_day
QA_fetch_get_hkfund_min = QA_fetch_get_future_min

QA_fetch_get_hkindex_day = QA_fetch_get_future_day
QA_fetch_get_hkindex_min = QA_fetch_get_future_min

QA_fetch_get_usstock_day = QA_fetch_get_future_day
QA_fetch_get_usstock_min = QA_fetch_get_future_min

QA_fetch_get_globalfuture_day = QA_fetch_get_future_day
QA_fetch_get_globalfuture_min = QA_fetch_get_future_min

QA_fetch_get_exchangerate_day = QA_fetch_get_future_day
QA_fetch_get_exchangerate_min = QA_fetch_get_future_min

QA_fetch_get_macroindex_day = QA_fetch_get_future_day
QA_fetch_get_macroindex_min = QA_fetch_get_future_min

QA_fetch_get_globalindex_day = QA_fetch_get_future_day
QA_fetch_get_globalindex_min = QA_fetch_get_future_min


def QA_fetch_get_wholemarket_list():
    hq_codelist = QA_fetch_get_stock_list(
        type_='all').loc[:, ['code', 'name']].set_index(['code', 'name'],
                                                        drop=False)
    kz_codelist = QA_fetch_get_extensionmarket_list().loc[:,
                                                          ['code', 'name']].set_index([
                                                              'code', 'name'], drop=False)

    return pd.concat([hq_codelist, kz_codelist], sort=False).sort_index()


if __name__ == '__main__':
    rows = QA_fetch_get_commodity_option_CU_contract_time_to_market()
    print(rows)

    print(QA_fetch_get_stock_day('000001', '2017-07-03', '2017-07-10'))
    print(QA_fetch_get_stock_day('000001', '2013-07-01', '2013-07-09'))
    # print(QA_fetch_get_stock_realtime('000001'))
    # print(QA_fetch_get_index_day('000001', '2017-01-01', '2017-07-01'))
    # print(QA_fetch_get_stock_transaction('000001', '2017-07-03', '2017-07-10'))

    # print(QA_fetch_get_stock_info('600116'))
