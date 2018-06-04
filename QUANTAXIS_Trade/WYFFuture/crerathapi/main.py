import ctypes
import os
import sys
import threading
import time
from multiprocessing import Pool

import numpy as np

from tradeapi import *

lock = threading.Lock()

# lock.acquire()
# return_list.append(close_return)
# lock.release()


def strategy_triup_down(instrument):

    p1, p2, p3 = 0, 0, 0
    times = 0
    api.getdealstatus.restype = c_double
    api.getorderstatus.restype = c_double
    global orderid
    innerid = ''
    print("beginning...................")
    while (1):

        try:
            price = instrument_price[instrument]
            p1 = p2
            p2 = p3
            p3 = price

            direction = 0
            time.sleep(1)
            times = times + 1
            # 调整的价格必须是期货品种的跳数
            if p3 > p2 and p2 > p1:

                lock.acquire()
                orderid = get_orderid()
                innerid = orderid
                lock.release()

                print(instrument, ':', orderid)
                api.tradeorder(c_char_p(bytes(instrument, 'utf-8')), c_int(1), c_int(2), c_int(0), c_double(price),
                               c_char_p(bytes(orderid, 'utf-8')))
                direction = -1

            elif p3 < p2 and p2 < p1:

                lock.acquire()
                orderid = get_orderid()
                lock.release()

                api.tradeorder(c_char_p(bytes(instrument, 'utf-8')), c_int(-1), c_int(2), c_int(0), c_double(price),
                               c_char_p(bytes(orderid, 'utf-8')))
                direction = 1

            # 撤掉上一笔没有成交的报单
            time.sleep(1)

            deal_num = -11.0
            status = -11.0

            try:
                deal_num = api.getdealstatus(c_char_p(bytes(innerid, 'utf-8')))
                status = api.getorderstatus(c_char_p(bytes(innerid, 'utf-8')))
            except Exception as e:
                # print(e)
                pass

            if deal_num < 5 and status != 5.0 and status != -1.0:

                try:
                    api.cancelorder(
                        c_char_p(bytes(instrument, 'utf-8')), c_char_p(bytes(innerid, 'utf-8')))
                except Exception as e:
                    pass

            # 平仓
            deal_num = -1.0
            status = -1.0
            try:
                deal_num = api.getdealstatus(c_char_p(bytes(innerid, 'utf-8')))
                status = api.getorderstatus(c_char_p(bytes(innerid, 'utf-8')))
                innerid = ''
            except Exception as e:
                pass
                # print(e)

            time.sleep(1)
            # 有成交
            if deal_num > 0:

                try:

                    lock.acquire()
                    orderid = get_orderid()
                    lock.release()

                    api.tradeorder(c_char_p(bytes(instrument, 'utf-8')), c_int(int(direction)), c_int(int(deal_num)), c_int(3), c_double(instrument_price[instrument]),
                                   c_char_p(bytes(orderid, 'utf-8')))
                except Exception as e:
                    print(e)
                    pass

        except Exception as e:
            print(e)
            print("error")


if __name__ == "__main__":

    # 启动行情服务
    hq_service_start = False
    while(1):
        hq_service_start = start_hq(instrument_list, account_info)
        if hq_service_start:
            break

    # 启动获取实时价格服务
    if hq_service_start:
        getprice = threading.Thread(
            target=get_instrument_timingprice, args=(instrument_list,))
        getprice.start()

    # 生成唯一的下单orderid
    getorderid = threading.Thread(target=get_orderid, args=(8,))
    getorderid.start()

    # 启动交易服务
    jy_service_start = False
    while(1):
        jy_service_start = start_jy()
        if jy_service_start:
            break

    orderid = ''
    # 策略逻辑
    for instrument in instrument_list:
        time.sleep(0.2)
        strtegy = threading.Thread(
            target=strategy_triup_down, args=(instrument,))
        strtegy.start()

    # with Pool(2) as p:
    #     retult = p.map(strategy_triup_down, instrument_list)
