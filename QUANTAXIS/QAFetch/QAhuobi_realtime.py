# coding: utf-8
# Author: 阿财（Rgveda@github）（11652964@qq.com）
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
"""
火币api
具体api文档参考:https://github.com/huobiapi/API_Docs/wiki
"""
from websocket import create_connection
import gzip
import time
import json
import threading

import pprint
import websocket
import sys

from QUANTAXIS.QAUtil.QAParameter import (FREQUENCE, MARKET_TYPE)
from QUANTAXIS.QAUtil.QALogs import (
    QA_util_log_info,
    QA_util_log_expection,
    QA_util_log_debug
)
from QUANTAXIS.QAUtil.QASetting import (QA_Setting, DATABASE)
from QUANTAXIS.QAUtil.QADate_Adv import (
    QA_util_str_to_Unix_timestamp,
    QA_util_datetime_to_Unix_timestamp,
    QA_util_timestamp_to_str
)
from QUANTAXIS.QAUtil.QAcrypto import QA_util_find_missing_kline

from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
from random import random

"""
huobi Python官方客户端文档参考: https://github.com/HuobiRDCenter/huobi_Python/blob/master/Readme.md
pip install huobi-client 的不是最新版(v0.32)，需要自己去 git 下载安装，测试基于
本模块开发为了更好的解耦合，移除 huobi-client 依赖，使用我最早裸写的原生代码版本实现，直接导入CandlestickInterval类
"""
class CandlestickInterval:
    MIN1 = "1min"
    MIN5 = "5min"
    MIN15 = "15min"
    MIN30 = "30min"
    MIN60 = "60min"
    HOUR4 = "4hour"
    DAY1 = "1day"
    MON1 = "1mon"
    WEEK1 = "1week"
    YEAR1 = "1year"
    INVALID = None

"""
QUANTAXIS 和 Huobi.pro 的 frequency 常量映射关系
"""
Huobi2QA_FREQUENCY_DICT = {
    CandlestickInterval.MIN1: FREQUENCE.ONE_MIN,
    CandlestickInterval.MIN5: FREQUENCE.FIVE_MIN,
    CandlestickInterval.MIN15: FREQUENCE.FIFTEEN_MIN,
    CandlestickInterval.MIN30: FREQUENCE.THIRTY_MIN,
    CandlestickInterval.MIN60: FREQUENCE.SIXTY_MIN,
    CandlestickInterval.DAY1: FREQUENCE.DAY
}

"""
Huobi WebSocket 接口只允许一次获取 300bar，日线只返回150bar，时间请求超过范围则不返回数据，Rest接口返回最新 2000bar（不可选择时间段）
"""
FREQUENCY_SHIFTING = {
    CandlestickInterval.MIN1: 14400,
    CandlestickInterval.MIN5: 72000,
    CandlestickInterval.MIN15: 216000,
    CandlestickInterval.MIN30: 432000,
    CandlestickInterval.MIN60: 864000,
    CandlestickInterval.DAY1: 12960000,
}
huobi_SYMBOL = 'HUOBI.{}'

class QA_Fetch_Job_Status(object):
    """
    行情数据获取批处理任务状态
    """
    INITIAL = 'STATUS_INIT'
    READY = 'STATUS_READY'
    FINISHED = 'STATUS_FINISHED'
    RUNNING = 'STATUS_RUNNING'
    ERROR = 'STATUS_ERROR'


def format_huobi_data_fields(datas, symbol, frequency):
    """
    # 归一化数据字段，转换填充必须字段，删除多余字段
    字段名称 	数据类型 	描述
    id 	long 	调整为新加坡时间的时间戳，单位秒，并以此作为此K线柱的id
    amount 	float 	以基础币种计量的交易量
    count 	integer 	交易次数
    open 	float 	本阶段开盘价
    close 	float 	本阶段收盘价
    low 	float 	本阶段最低价
    high 	float 	本阶段最高价
    vol 	float 	以报价币种计量的交易量
    """
    # 归一化数据字段，转换填充必须字段，删除多余字段
    frame = pd.DataFrame(datas)
    frame['id'] = frame.apply(lambda x: int(x.loc['id']), axis=1)
    frame['symbol'] = 'HUOBI.{}'.format(symbol)
    # UTC时间转换为北京时间
    frame['date'] = pd.to_datetime(
        frame['id'],
        unit='s'
    ).dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
    frame['date'] = frame['date'].dt.strftime('%Y-%m-%d')
    frame['datetime'] = pd.to_datetime(
        frame['id'],
        unit='s'
    ).dt.tz_localize('UTC').dt.tz_convert('Asia/Shanghai')
    frame['datetime'] = frame['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # 北京时间转换为 UTC Timestamp
    frame['date_stamp'] = pd.to_datetime(
        frame['date']
    ).dt.tz_localize('Asia/Shanghai').astype(np.int64) // 10**9
    frame['created_at'] = time.mktime(datetime.now().utctimetuple())
    frame['updated_at'] = time.mktime(datetime.now().utctimetuple())
    frame.rename({'count': 'trade', 'id': 'time_stamp', 'vol': 'volume'}, axis=1, inplace=True)
    if (frequency not in [CandlestickInterval.DAY1, Huobi2QA_FREQUENCY_DICT[CandlestickInterval.DAY1], '1d']):
        frame['type'] = Huobi2QA_FREQUENCY_DICT[frequency]
    return frame


class QA_Fetch_Job_Type(object):
    """
    行情数据获取批处理任务类型
    """
    REQUEST = 'REQUEST'
    SUBSCRIBE = 'SUBSCRIBE'


class QA_Fetch_Job(object):
    """
    行情数据获取批处理任务，此为公共抽象类
    """
    FREQUENCE_PERIOD_TIME = {
        CandlestickInterval.MIN1: 60,
        CandlestickInterval.MIN5: 300,
        CandlestickInterval.MIN15: 900,
        CandlestickInterval.MIN30: 1800,
        CandlestickInterval.MIN60: 3600,
        CandlestickInterval.DAY1: 86400,
    }

    __request = None

    def __init__(self, symbol, period=CandlestickInterval.MIN1):
        """
        初始化的时候 会初始化
        """
        self.__symbol = symbol
        self.__period = period
        self.__status = QA_Fetch_Job_Status.INITIAL
        self.__type = QA_Fetch_Job_Type.REQUEST
        self.__params = {}
        self.__period_time = self.FREQUENCE_PERIOD_TIME[period]
        self.__request = []

    def withParams(
        self,
        jobParams,
        jobSymbol,
        jobShiftingTime,
        jobType=QA_Fetch_Job_Type.REQUEST
    ):
        """
        填充批处理任务参数
        """
        self.__params = jobParams
        self.__symbol = jobSymbol
        self.__shifting_time = jobShiftingTime
        self.__type = jobType

    @property
    def Status(self):
        """
        任务运行状态
        """
        return self.__status

    def setStatus(self, value):
        """
        标记任务运行状态
        """
        self.__status = value

    @property
    def Request(self):
        """
        已发送请求
        """
        return self.__request

    @property
    def Params(self):
        """
        任务运行参数
        """
        return self.__params

    @property
    def Type(self):
        """
        任务运行状态
        """
        return self.__type

    @property
    def Symbol(self):
        """
        任务标识符/数据表
        """
        return self.__symbol

    @property
    def Shifting_Time(self):
        """
        任务请求数据的时间窗口间隔
        return int:
        """
        return self.__shifting_time

    @property
    def Period(self):
        """
        任务对象的分时时间周期
        return str:
        """
        return self.__period

    @property
    def Period_Time(self):
        """
        任务对象的分时时间周期（秒）
        return int:
        """
        return self.__period_time


class QA_Tick_Summary(object):
    """
    行情数据获取统计类，负责统计和输出日志
    """

    def __init__(self, countdown=30):
        """
        初始化的时候 会初始化
        """
        self.__countdown = countdown
        self.__next = datetime.now() + timedelta(seconds=self.__countdown)
        self.__summary = {}

    def Tick(self, symbol):
        """
        Tick 计数器
        """

        if symbol in self.__summary:
            self.__summary[symbol] = self.__summary[symbol] + 1
        else:
            self.__summary[symbol] = 1

        if (datetime.now() - self.__next).total_seconds() > 0:
            QA_util_log_info(
                "Tick message counter @ %s" %
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            for symbol in self.__summary:
                QA_util_log_info(
                    "on %s got %d ticks" % (symbol,
                                            self.__summary[symbol])
                )

            self.__summary.clear()
            self.__next = datetime.now() + timedelta(seconds=self.__countdown)


class QA_Fetch_Huobi(object):
    """
    火币Pro行情数据 WebSocket 接口，基础类
    """
    HUOBIPRO_WEBSOCKET_URL = "wss://api.huobi.pro/ws"

    def __init__(
        self,
        market='huobi',
        callback_save_data_func=None,
        find_missing_kline_func=None
    ):
        """
        初始化的时候 会初始化
        """
        self.client = DATABASE
        self.__interval = 20
        self.__locked = False
        self.__batchSubJobs = {}
        self.__batchReqJobs = {}
        self.__request_awaiting = False
        self._crypto_asset_info = pd.DataFrame(
            columns=['symbol',
                     'market',
                     'FREQUENCE',
                     'STATE']
        )
        self.__ws = None
        self.callback_save_data_func = callback_save_data_func
        self.find_missing_kline_func = find_missing_kline_func
        self.__tick_summary = QA_Tick_Summary(5)

    def Shifting_Time(self, period):
        """
        设定每次获取K线数据的时间区间长度（单位秒），超过300条数据将会获取失败，此处设定每次获取240条数据
        """
        if period == FREQUENCE.ONE_MIN:
            return 3600 * 4    # 4 hours
        elif period == FREQUENCE.FIVE_MIN:
            return 3600 * 20   # 20 hours
        elif period == FREQUENCE.FIFTEEN_MIN:
            return 3600 * 60   # 60 hours
        elif period == FREQUENCE.THIRTY_MIN:
            return 3600 * 120  # 120 hours
        elif (period == FREQUENCE.HOUR) or (period == FREQUENCE.SIXTY_MIN):
            return 3600 * 240  # 240 hours
        elif period == FREQUENCE.DAY:
            return 3600 * 5760 # 5760 hours
        else:
            return 3600 * 4    # 4 hours

    def gen_ws_id(self, symbol, period):
        """
        生成id标识符，用来匹配数据块
        """
        req_id = """%s.%s""" % (symbol, period)
        return req_id

    def send_message(self, message_dict, message_txt=''):
        """
        发送消息请求
        """
        data = json.dumps(message_dict).encode()
        QA_util_log_info("Sending Message: {:s}".format(message_txt))

        self.__ws.send(data)

    def on_message(self, message):
        """
        接收 WebSocket 数据，响应“心跳”
        """
        unzipped_data = gzip.decompress(message).decode()
        msg_dict = json.loads(unzipped_data)

        if 'ping' in msg_dict:
            # 回应“心跳”
            QA_util_log_info("Recieved Message: ping")
            data = {"pong": msg_dict['ping']}
            self.send_message(data, 'Responded heart-bit(ping).')
        elif (('status' in msg_dict) and (msg_dict['status'] == 'ok')
              and ('data' in msg_dict)):
            if ((msg_dict['rep'] in self.__batchReqJobs)
                    and ('req' in self.__batchReqJobs[msg_dict['rep']].Params)):
                QA_util_log_info(
                    'Data message match! Save symbol：{:s} with freq {:s}'
                    .format(
                        self.__batchReqJobs[msg_dict['rep']].Symbol,
                        msg_dict['rep']
                    )
                )
                self.__batchReqJobs[msg_dict['rep']].setStatus(
                    QA_Fetch_Job_Status.READY
                )

                # 处理返回的行情数据
                if (len(msg_dict['data']) == 0):
                    # 没有缺漏数据，神完气足，当前时间分段的K线数据全部获取完毕，转入实时K线数据获取模式。
                    QA_util_log_info(
                        "'%s' 时间的K线数据全部获取完毕，转入实时K线数据获取模式。" %
                        self.__batchReqJobs[msg_dict['rep']].Params['req']
                    )
                    self.__batchReqJobs[msg_dict['rep']].setStatus(
                        QA_Fetch_Job_Status.FINISHED
                    )
                else:
                    # 归一化数据字段，转换填充必须字段，删除多余字段 GMT+8
                    ohlcvData = format_huobi_data_fields(msg_dict['data'], symbol=self.__batchReqJobs[msg_dict['rep']].Symbol, frequency=self.__batchReqJobs[msg_dict['rep']].Period)

                    QA_util_log_info(
                        "rep: %s, id: %s, return %d records." %
                        (msg_dict['rep'],
                         msg_dict['id'],
                         len(ohlcvData))
                    )
                    self.callback_save_data_func(
                        ohlcvData,
                        freq=Huobi2QA_FREQUENCY_DICT[self.__batchSubJobs[
                            msg_dict['rep']].Period]
                    )
            else:
                QA_util_log_expection(
                    'No Match Found! Unhandle this messgae:',
                    self.__batchSubJobs[msg_dict['rep']].Params
                )
                QA_util_log_expection(pprint.pformat(msg_dict, indent=4))
        elif (('ch' in msg_dict) and ('tick' in msg_dict)):
            if ((msg_dict['ch'] in self.__batchSubJobs)
                    and ('sub' in self.__batchSubJobs[msg_dict['ch']].Params)):
                # 合并显示每5秒内接收到的 Tick 数据
                self.__tick_summary.Tick(msg_dict['ch'])

                # 处理返回的行情数据
                if (len(msg_dict['tick']) > 0):
                    # 归一化数据字段，转换填充必须字段，删除多余字段 GMT+8
                    ohlcvData = format_huobi_data_fields(pd.DataFrame.from_dict(msg_dict['tick'],orient='index').T, symbol=self.__batchSubJobs[msg_dict['ch']].Symbol, frequency=self.__batchSubJobs[msg_dict['ch']].Period)

                self.callback_save_data_func(
                    ohlcvData,
                    freq=Huobi2QA_FREQUENCY_DICT[self.__batchSubJobs[msg_dict['ch']
                                                                ].Period]
                )
                if ((msg_dict['ch'] in self.__batchReqJobs)
                        and (self.__batchReqJobs[msg_dict['ch']].Status
                             == QA_Fetch_Job_Status.INITIAL)):
                    # 异步延迟加载，避免阻塞，避免被 Ban IP
                    self.run_request_kline(msg_dict['ch'])
            else:
                QA_util_log_expection('No Match Found! Unhandle this messgae:')
                QA_util_log_expection(pprint.pformat(msg_dict, indent=4))
        elif (('subbed' in msg_dict) and (msg_dict['status'] == 'ok')):
            QA_util_log_info('订阅 Tick 数据成功 %s' % msg_dict['subbed'])
        else:
            # 不知道如何处理的返回数据
            QA_util_log_expection('Unhandle this messgae:')
            QA_util_log_expection(pprint.pformat(msg_dict, indent=4))

    def on_error(self, error):
        """
        处理错误信息
        """
        QA_util_log_info("Error: " + str(error))
        error = gzip.decompress(error).decode()
        QA_util_log_info(error)

    def on_close(self):
        """
        关闭连接
        """
        QA_util_log_info("### closed ###")

    def on_open(self):
        """
        开启轮询线程，do nothing
        """
        # 批处理任务的调试信息
        QA_util_log_info(
            'Batch job added. Please make sure your Internet connection had jump-over-the-GFW...'
        )

        # 启动实时行情订阅
        for key in self.__batchSubJobs:
            currentJob = self.__batchSubJobs[key]
            currentJob.setStatus(QA_Fetch_Job_Status.RUNNING)

            # 实时数据订阅模式，不需要多线程频繁请求，但是需要开启个守护进程检查当前实时K线数据的订阅情况。
            subParams = currentJob.Params
            self.send_message(subParams, key)

            time.sleep(0.2)
            # end for self.__batchJobs

        # 启动历史行情查询线程
        #for key in self.__batchReqJobs:
        #    自动转入处理下一个批次任务
        #    continue
        #end for self.__batchReqJobs

    def run_request_kline(self, req):
        """
        # 启动历史行情查询线程，为了避免Ban IP采用延迟加载
        """

        def run(initalParams):
            """
            运行于多线程的ws 请求发送，每3秒请求一次K线图数据，一次请求240条（的时间段），从参数设定的开始时间，请求到终止时间段为止
            """
            # missing data key indexes
            expected = 0
            between = 1
            missing = 2

            requested_counter = 1
            reqParams = {
                'req': initalParams['req'],
            }

            # 采用时间倒序抓取，huobi WebSocket api 非常有个性，基本上遵循2个规则：
            # 'from' 'to' 范围内没交易数据（交易对未上架）——返回 0 数据，
            # 'from' 'to' 范围内超过300个bar，——返回 0 数据，一个交易对最早是什么时候上架的——无法查询到
            # 所以选择倒序算法，从最近的时间开始补历史数据，'from' 'to' 请求范围一直向前递减到请求不到数据为止。
            missing_data_list = initalParams['missing'][::-1]
            for i in range(len(missing_data_list)):
                reqParams['from'] = int(missing_data_list[i][
                    between] - initalParams['shifting_time'])
                reqParams['to'] =  int(missing_data_list[i][between])
                if (reqParams['to'] >
                    (QA_util_datetime_to_Unix_timestamp() + 120)):
                    # 出现“未来”时间，一般是默认时区设置错误造成的
                    QA_util_log_info(
                        'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                        .format(
                            reqParams['req'],
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
                    'Fetch %s missing kline：%s 到 %s' % (
                        initalParams['req'],
                        QA_util_timestamp_to_str(
                            missing_data_list[i][expected]
                        )[2:16],
                        QA_util_timestamp_to_str(missing_data_list[i][between]
                                                )[2:16]
                    )
                )
                while (reqParams['to'] > missing_data_list[i][expected]):
                    if (self.__batchReqJobs[initalParams['req']].Status ==
                            QA_Fetch_Job_Status.FINISHED):
                        # 抓取已经结束了
                        return True

                    if (self.__batchReqJobs[initalParams['req']].Status ==
                            QA_Fetch_Job_Status.READY):
                        reqParams['id'] = "%s_#%d" % (
                            initalParams['id'],
                            requested_counter
                        )
                        if (reqParams['from'] >
                            (QA_util_datetime_to_Unix_timestamp() + 120)):
                            # 出现“未来”时间，一般是默认时区设置错误造成的
                            QA_util_log_info(
                                'A unexpected \'Future\' timestamp got, Please check self.missing_data_list_func param \'tzlocalize\' set. More info: {:s}@{:s} at {:s} but current time is {}'
                                .format(
                                    reqParams['req'],
                                    frequency,
                                    QA_util_print_timestamp(reqParams['from']),
                                    QA_util_print_timestamp(
                                        QA_util_datetime_to_Unix_timestamp()
                                    )
                                )
                            )
                            # 跳到下一个时间段
                            reqParams['to'] = int(reqParams['from'] - 1)
                            reqParams['from'] = int(reqParams['from'] - initalParams['shifting_time'])
                            continue
                        self.__batchReqJobs[initalParams['req']
                                           ].Request.append(reqParams)
                        self.send_message(
                            reqParams,
                            'request kline {:s} part#{:d} {:s} to {:s}'.format(
                                initalParams['req'],
                                requested_counter,
                                QA_util_timestamp_to_str(reqParams['from']
                                                        )[2:16],
                                QA_util_timestamp_to_str(reqParams['to'])[2:16]
                            )
                        )

                        # 等待3秒，请求下一个时间段的批量K线数据
                        reqParams['to'] = int(reqParams['from'] - 1)
                        reqParams['from'] = int(reqParams['from'] - initalParams[
                            'shifting_time'])
                        requested_counter = requested_counter + 1

                        # 锁定线程，等待回复，避免快速频繁重复请求，会被ban IP的
                        self.__batchReqJobs[initalParams['req']].setStatus(
                            QA_Fetch_Job_Status.RUNNING
                        )
                    else:
                        # WebSocket请求发出后等待没有回复无需特别处理，一般是SSR/SSL断线，会自动重连，继续补缺失数据
                        time.sleep(10)
                        self.send_message(
                            reqParams,
                            'request kline {:s} part#{:d} {:s} to {:s}'.format(
                                initalParams['req'],
                                requested_counter,
                                QA_util_timestamp_to_str(reqParams['from']
                                                        )[2:16],
                                QA_util_timestamp_to_str(reqParams['to'])[2:16]
                            )
                        )
                        pass

                    time.sleep(3)

            # 当前时间分段的K线数据全部获取完毕
        def start_thread(key, reqParams):
            """
            发起抓取线程，代码复用
            """
            # 开启抓取线程，抓取指定时间切片分时数据
            t = threading.Thread(target=run, args=(reqParams,))
            t.start()

        currentJob = self.__batchReqJobs[req]
        currentJob.setStatus(QA_Fetch_Job_Status.READY)
        if (currentJob.Type == QA_Fetch_Job_Type.REQUEST):
            # 查询到 Kline 缺漏，点抓取模式，按缺失的时间段精确请求K线数据
            missing_data_list = self.find_missing_kline_func(
                huobi_SYMBOL.format(currentJob.Symbol),
                Huobi2QA_FREQUENCY_DICT[currentJob.Period],
            )
            if len(missing_data_list) > 0:
                # 查询确定中断的K线数据起止时间，缺分时数据，补分时数据
                reqParams = {
                    'req': currentJob.Params['req'],
                    'id': currentJob.Params['id'],
                    'missing': missing_data_list,
                    'period_time': currentJob.Period_Time,
                    'shifting_time': currentJob.Shifting_Time,
                }
                start_thread(req, reqParams)
                time.sleep(0.5)
            else:
                # 没有缺漏数据，神完气足，当前时间分段的K线数据全部获取完毕，转入实时K线数据获取模式。
                QA_util_log_info(
                    "'%s' 时间的K线数据全部获取完毕，转入实时K线数据获取模式。" %
                    currentJob.Params['req']
                )

    def add_subscription(
        self,
        candleline=pd.Series(),
        start_epoch=datetime.now()
    ):
        """
        添加批处理任务队列，顺便进行订阅
        """
        start_epoch = QA_util_str_to_Unix_timestamp(start_epoch)
        symbol = candleline['symbol']
        period = candleline['FREQUENCE']
        requestIdx = self.gen_ws_id(symbol, period)

        # QUANTAXIS 系统定义的时间跟火币网WebSocket 接口的有一点偏差 day 火币叫 1day，hour 火币定义为
        # 60min，需要查表映射转换。
        requestStr = "market.%s.kline.%s" % (
            symbol,
            period
        )

        # 订阅K线记录
        self.__batchSubJobs[requestStr] = QA_Fetch_Job(symbol, period)
        self.__batchSubJobs[requestStr].withParams(
            {
                "sub": requestStr,
                "id": requestIdx,
            },
            symbol,
            self.Shifting_Time(period),
            QA_Fetch_Job_Type.SUBSCRIBE
        )

        # 补全历史K线数据
        self.__batchReqJobs[requestStr] = QA_Fetch_Job(symbol, period)
        self.__batchReqJobs[requestStr].withParams(
            {
                "req": requestStr,
                "id": requestIdx,
                "from": int(start_epoch),
            },
            symbol,
            self.Shifting_Time(period),
            QA_Fetch_Job_Type.REQUEST
        )

        return self

    def add_subscription_batch_jobs(
        self,
        symbols=[],
        periods=[FREQUENCE.ONE_MIN],
        start_epoch=datetime.now()
    ):
        """
        批量添加交易对的批处理任务队列，顺便进行订阅
        """
        if (isinstance(symbols, str)):
            symbols = [symbols]

        for symbol in symbols:
            for freq in periods:
                self._crypto_asset_info = self._crypto_asset_info.append(
                    {
                        'symbol': symbol,
                        'market': 'huobi',
                        'FREQUENCE': freq,
                        'STATE': QA_Fetch_Job_Type.SUBSCRIBE,
                    },
                    ignore_index=True
                )

        self._crypto_asset_info.set_index(
            ['symbol',
             'FREQUENCE'],
            drop=False,
            inplace=True
        )
        for index, row in self._crypto_asset_info.iterrows():
            self.add_subscription(self._crypto_asset_info.loc[index,:], start_epoch)

        return self

    def run_subscription_batch_jobs(self):
        """
        请求 KLine 实时数据
        """
        websocket.enableTrace(False)
        self.__ws = websocket.WebSocketApp(
            self.HUOBIPRO_WEBSOCKET_URL,
            on_message=self.on_message,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.__locked = True

        # 如果意外退出，等待10秒重新运行
        while (True):
            self.__ws.run_forever()
            QA_util_log_expection("FTW! it quit! Retry 10 seconds later...")
            time.sleep(10)

    def run_request_historical_kline(
        self,
        symbol,
        period,
        start_epoch,
        end_epoch,
        requested_counter=1
    ):
        """
        请求 KLine 历史数据，直到数据完结 Get the symbol‘s candlestick data by subscription
        """
        websocket.enableTrace(False)
        ws = websocket.create_connection(
            self.HUOBIPRO_WEBSOCKET_URL,
            timeout=10
        )

        # QUANTAXIS 系统定义的时间跟火币网WebSocket 接口的有一点偏差 day 火币叫 1day，hour 火币定义为
        # 60min，需要查表映射转换。
        reqParams = {}
        reqParams['req'] = requestStr = "market.%s.kline.%s" % (
            symbol,
            period
        )
        reqParams['from'] = int(start_epoch)
        reqParams['to'] = int(end_epoch)
        reqParams['id'] = requestIdx = "%s_#%d" % (
            self.gen_ws_id(symbol,
                           period),
            int(random() * 100)
        )

        self.__batchReqJobs[requestStr] = QA_Fetch_Job(symbol, period)
        self.__batchReqJobs[requestStr].withParams(
            {
                "req": requestStr,
                "id": requestIdx,
                "from": int(start_epoch),
            },
            symbol,
            self.Shifting_Time(period),
            QA_Fetch_Job_Type.REQUEST
        )

        data = json.dumps(reqParams).encode()
        QA_util_log_info(
            'Sending Message: request kline {:s} part#{} {:s} to {:s}'.format(
                symbol,
                requested_counter,
                QA_util_timestamp_to_str(reqParams['from'])[2:16],
                QA_util_timestamp_to_str(reqParams['to'])[2:16]
            )
        )
        ws.send(data)

        message = ws.recv()
        unzipped_data = gzip.decompress(message).decode()
        msg_dict = json.loads(unzipped_data)
        ws.close()
        if (('status' in msg_dict) and (msg_dict['status'] == 'ok')
                and ('data' in msg_dict)):
            QA_util_log_info(
                'Data message match! Save symbol：{:s} with freq {:s}'.format(
                    symbol,
                    msg_dict['rep']
                )
            )

            # 处理返回的行情数据
            if (len(msg_dict['data']) == 0):
                # 火币网的 WebSocket 接口机制很奇特，返回len(data)==0
                # 就说明已经超越这个交易对的上架时间，不再有更多数据了。
                # 当前 Symbol Klines 抓取已经结束了
                #print(QA_util_timestamp_to_str(reqParams['from'])[2:16], 'Return None')
                return None
            else:
                # 归一化数据字段，转换填充必须字段，删除多余字段 GMT+8
                ohlcvData = format_huobi_data_fields(msg_dict['data'], symbol=symbol, frequency=period)

                QA_util_log_info(
                    "rep: %s, id: %s, return %d kiline bar(s)." %
                    (msg_dict['rep'],
                     msg_dict['id'],
                     len(ohlcvData))
                )
                return ohlcvData


if __name__ == "__main__":
    from QUANTAXIS.QASU.save_huobi import (QA_SU_save_data_huobi_callback)

    fetch_huobi_history = QA_Fetch_Huobi(callback_save_data_func=QA_SU_save_data_huobi_callback, find_missing_kline_func=QA_util_find_missing_kline)

    # 添加抓取行情数据任务，将会开启多线程抓取。
    fetch_huobi_history.add_subscription_batch_jobs(['hb10usdt'], [CandlestickInterval.MIN1,
            CandlestickInterval.MIN5,
            CandlestickInterval.MIN15,
            CandlestickInterval.MIN30,
            CandlestickInterval.MIN60,
            CandlestickInterval.DAY1], '2017-10-26 02:00:00')

    fetch_huobi_history.run_subscription_batch_jobs()
    pass
