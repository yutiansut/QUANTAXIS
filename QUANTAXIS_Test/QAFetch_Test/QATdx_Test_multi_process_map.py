# -*- coding: utf-8 -*-

from unittest import TestCase
import QUANTAXIS as QA
from QUANTAXIS.QAFetch import QATdx
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_day, select_best_ip, \
    ping, get_ip_list_by_multi_process_ping
from QUANTAXIS.QASU.save_tdx import gen_param, now_time
from QUANTAXIS.QAUtil.QASetting import QA_Setting
from QUANTAXIS.QAUtil.QADate_trade import QA_util_if_tradetime
from QUANTAXIS.QAUtil.Parallelism import Parallelism
import datetime, time
import os
from multiprocessing import cpu_count
from QUANTAXIS.QACmd import QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_etf_day
from QUANTAXIS.QAUtil import QA_util_cache
from QUANTAXIS.QAUtil.QASetting import DATABASE


class TestSelect_best_ip(TestCase):
    def test_select_best_ip(self):
        best_ip = select_best_ip()
        ip = best_ip['stock']['ip']
        port = best_ip['stock']['port']
        self.assertTrue(isinstance(ip, str), '未获取到ip')
        self.assertTrue(isinstance(port, int), '未获取到端口号')
        self.assertTrue(ping(ip, port, 'stock') < datetime.timedelta(0, 1, 0),
                        '地址ping不通： {} {} {}'.format(ip, port,
                                                    ping(ip, port, 'stock')))
        type = 'future'
        ip = best_ip[type]['ip']
        port = best_ip[type]['port']
        self.assertTrue(ping(ip, port, type) < datetime.timedelta(0, 1, 0),
                        '地址ping不通： {} {} {}'.format(ip, port,
                                                    ping(ip, port, 'stock')))

        code = '000001'
        days = 300
        start = datetime.datetime.now().date() - datetime.timedelta(days)
        end = datetime.datetime.now().date() - datetime.timedelta(10)
        data = QA_fetch_get_stock_day(code, start_date=start, end_date=end)
        # print(data)
        self.assertTrue(len(data) > (end - start).days / 2,
                        '返回数据个数不匹配，数据长度：{},天数（包含节假日）：{}'.format(
                            len(data), (end - start).days / 2))

        # 恢复初始化ip，重新测试ip
        default_ip = {'stock': {'ip': None, 'port': None},
                      'future': {'ip': None, 'port': None}}
        qasetting = QA_Setting()
        qasetting.set_config(
            section='IPLIST', option='default', default_value=default_ip)
        filenames = ['stock_ip_list', 'stock_ip_list_MP']
        for filename in filenames:
            # 删除保存ip的pickle文件
            filename = '{}{}{}.pickle'.format(qasetting.get_config(
                section='LOG', option='path', default_value=""), os.sep,
                filename)
            if os.path.isfile(filename):
                os.remove(filename)
        best_ip = select_best_ip()
        ip = best_ip['stock']['ip']
        port = best_ip['stock']['port']
        self.assertTrue(isinstance(ip, str), '未获取到ip')
        self.assertTrue(isinstance(port, int), '未获取到端口号')
        ip = best_ip['future']['ip']
        port = best_ip['future']['port']
        self.assertTrue(isinstance(ip, str), '未获取到ip')
        self.assertTrue(isinstance(port, int), '未获取到端口号')
        data = QA_fetch_get_stock_day(code, start, end)
        self.assertTrue(len(data) > (end - start).days / 2,
                        '返回数据个数不匹配，数据长度：{},天数（包含节假日）：{}'.format(
                            len(data), (end - start).days / 2))

    def test_gen_param(self):
        codelist = QA.QA_fetch_stock_list_adv().code.tolist()
        days = 300
        start = datetime.datetime.now().date() - datetime.timedelta(days)
        end = datetime.datetime.now().date() - datetime.timedelta(10)
        codeListCount = 200
        ips = get_ip_list_by_multi_process_ping(QA.QAUtil.stock_ip_list,
                                                _type='stock')
        param = gen_param(codelist[:codeListCount], start, end,
                          IPList=ips[:cpu_count()])
        a = time.time()
        ps = Parallelism(cpu_count())
        ps.run(QA.QAFetch.QATdx.QA_fetch_get_stock_day, param)
        data = ps.get_results()
        b = time.time()
        t1 = b - a
        data = list(data)
        print('返回数据{}条，用时：{}秒'.format(len(data), t1))
        # print(data)
        # print([x.code.unique() for x in data])
        self.assertTrue(len(data) == codeListCount,
                        '返回结果和输入参数个数不匹配： {} {}'.format(len(data),
                                                       codeListCount))
        i, j = 0, 0
        for x in data:
            try:
                # print(x)
                i += 1
                self.assertTrue((x is None) or (len(x) > 0),
                                '返回数据太少：{}'.format(len(x)))
                if not ((x is None) or (len(x) > 0)):
                    print('data is None')
                if i % 10 == 0:
                    print(x)
            except Exception as e:
                j += 1
        print(i, j)

    def test_QA_SU_save_stock_day_lastdate(self):
        # 交易时间QA.QAFetch.QATdx.QA_fetch_get_stock_day返回的数据会实时更新
        codelist = QA.QA_fetch_stock_list_adv().code.tolist()
        days = 300
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now()
        if QA_util_if_tradetime(end):
            end2 = end - datetime.timedelta(1)
        else:
            end2 = end
        codeListCount = 200
        a = time.time()
        # ps = Parallelism(cpu_count())
        data1 = QA.QAFetch.QATdx.QA_fetch_get_stock_day(codelist[0], start,
                                                        end)
        data2 = QA.QAFetch.QATdx.QA_fetch_get_stock_day(codelist[0], start,
                                                        end2)
        # 交易时间段
        self.assertTrue(len(data1) == len(data2),
                        '数据长度：{} {} 日期： {} {}'.format(len(data1), len(data2),
                                                      end, end2))
        print('数据长度：{} {} 日期： {} {}'.format(
            len(data1), len(data2), end, end2))
        print('当前数据： {} {}'.format(data1.close[-1], data2.close[-1]))

        # 设定在交易时间内
        end = datetime.datetime(end.year, end.month, end.day, 10, 0)
        end2 = end
        while not QA_util_if_tradetime(end):
            end = end - datetime.timedelta(1)
        end = end - datetime.timedelta(7)
        codeListCount = 200
        a = time.time()
        # ps = Parallelism(cpu_count())
        data1 = QA.QAFetch.QATdx.QA_fetch_get_stock_day(codelist[0], start,
                                                        end)
        data2 = QA.QAFetch.QATdx.QA_fetch_get_stock_day(codelist[0], start,
                                                        end2)
        # 交易时间段
        self.assertFalse(len(data1) == len(data2),
                         '数据长度应不等：{} {} 日期： {} {}'.format(len(data1),
                                                          len(data2), end,
                                                          end2))
        print('数据长度：{} {} 日期： {} {}'.format(
            len(data1), len(data2), end, end2))
        print('当前数据： {} {}'.format(data1.close[-1], data2.close[-1]))

    def test_QA_SU_save_stock_day(self):
        print('start test_QA_SU_save_stock_day')
        codelist = QA.QA_fetch_stock_list_adv().code.tolist()
        days = 300
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now()
        data1 = QA.QA_fetch_stock_day_adv(codelist[0], start, end)
        QA_SU_save_stock_day('tdx', paralleled=True)
        print('end test_QA_SU_save_stock_day')
        data2 = QA.QA_fetch_stock_day_adv(codelist[0], start, end)
        self.assertTrue(
            len(data2) == len(data1) if data1.datetime[-1] == data2.datetime[
                -1] else len(data2) > len(data1),
            '保存后的数据应该比未保存前长： {} {}'.format(len(data2), len(data1)))

    def test_QA_SU_save_stock_day_with_delete(self):
        stockDay = DATABASE.stock_day
        myquery = {"code": {"$regex": "^300"}}
        x = stockDay.delete_many(myquery)
        print(x.deleted_count, " documents deleted.")

        self.test_QA_SU_save_stock_day()

    # def test_get_index_min_adv(self):
    # 分钟数据测试
    # def __get_index_min_adv(code, start, end, frequence):
    #     if isinstance(code, list) is not True:
    #         code = [str(code)]
    #     df = None
    #
    #     # todo: 启用多服务IP支持
    #     for _code in code:
    #         result = QA.QA_fetch_get_index_min(package='tdx', code=_code,
    #               start=start, end=end, level=frequence)
    #         if result is not None:
    #             df = result if df is None else df.append(result)
    #     if df is None:
    #         return None
    #     else:
    #         df = df.set_index(['datetime', 'code'])
    #         return QA.QA_DataStruct_Index_min(df)

    def test_cache(self):
        # 测试内存缓存变量
        from QUANTAXIS.QAUtil.QASetting import DATABASE, stock_ip_list, \
            future_ip_list
        best_ip = select_best_ip()
        stockips = QATdx.get_ip_list_by_multi_process_ping(stock_ip_list,
                                                           _type='stock')
        stockip = QATdx.get_ip_list_by_ping(stock_ip_list, _type='stock')
        self.assertTrue(stockip == stockips[0],
                        '没有使用缓存： {} {}'.format(stockip, stockips[0]))

        futurips = QATdx.get_ip_list_by_multi_process_ping(future_ip_list,
                                                           _type='future')
        futurip = QATdx.get_ip_list_by_ping(future_ip_list, _type='future')
        self.assertTrue(futurip == futurips[0],
                        '没有使用缓存： {} {}'.format(futurip, futurips[0]))

        stockips = QATdx.get_ip_list_by_multi_process_ping(stock_ip_list,
                                                           _type='stock')
        futurips = QATdx.get_ip_list_by_multi_process_ping(future_ip_list,
                                                           _type='future')
        stockips = QATdx.get_ip_list_by_multi_process_ping(stock_ip_list,
                                                           _type='stock')
        futurips = QATdx.get_ip_list_by_multi_process_ping(future_ip_list,
                                                           _type='future')

    def test_QA_SU_save_index_day(self):
        print('start test_QA_SU_save_index_day')
        codelist = QA.QA_fetch_index_list_adv().code.tolist()
        index__or_etf = 'index'
        self._test_QA_SU_save_index_or_etf_day(codelist, index__or_etf, paralleled=True)

    def _test_QA_SU_save_index_or_etf_day(self, codelist, index__or_etf='index', paralleled=True):
        days = 300
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now()
        data1 = QA.QA_fetch_index_day_adv(codelist[0], start, end)
        # 多线程能提高一倍的速度
        if index__or_etf == 'index':
            QA_SU_save_index_day('tdx', paralleled=paralleled)
        else:
            QA_SU_save_etf_day('tdx', paralleled=paralleled)

        print('end test_QA_SU_save_stock_day')
        data2 = QA.QA_fetch_index_day_adv(codelist[0], start, end)
        if data1:
            cond = len(data2) == len(data1) \
                if data1.datetime[-1] == data2.datetime[-1] else \
                len(data2) > len(data1)
            self.assertTrue(cond,
                            '保存后的数据应该比未保存前长： {} {}'.format(
                                len(data2), len(data1)))
            print('保存前日期： {}， 保存后日期 {}'.format(data1.datetime[-1],
                                               data2.datetime[-1]))
            # import inspect
            # source=inspect.getsource(QA_SU_save_index_day)
            # print(source)

    def test_QA_SU_save_index_day_with_delete(self):
        #  删除部分数据
        indexDay = DATABASE.index_day
        myquery = {"code": {"$regex": "^00"}}
        x = indexDay.delete_many(myquery)
        print(x.deleted_count, " documents deleted.")

        self.test_QA_SU_save_index_day()

    def test_QA_SU_save_etf_day(self):
        print('start test_QA_SU_save_etf_day')
        codelist = QA.QA_fetch_etf_list().code.tolist()
        print(codelist)
        index__or_etf = 'etf'
        self._test_QA_SU_save_index_or_etf_day(codelist, index__or_etf, paralleled=True)

    def test_QA_SU_save_etf_day_with_delete(self):
        #  删除部分数据
        indexDay = DATABASE.index_day
        myquery = {"code": {"$regex": "^51"}}
        x = indexDay.delete_many(myquery)
        print(x.deleted_count, " documents deleted.")

        self.test_QA_SU_save_etf_day()

    def test_save_day(self):
        from QUANTAXIS.QACmd import QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_etf_day, \
            QA_SU_save_stock_xdxr, QA_SU_save_etf_list, QA_SU_save_index_list, QA_SU_save_stock_list, \
            QA_SU_save_stock_block
        QA_SU_save_stock_day('tdx', paralleled=True)
        QA_SU_save_stock_xdxr('tdx')
        QA_SU_save_index_day('tdx', paralleled=True)
        QA_SU_save_etf_list('tdx')
        QA_SU_save_etf_day('tdx', paralleled=True)
        QA_SU_save_index_list('tdx')
        QA_SU_save_stock_list('tdx')
        QA_SU_save_stock_block('tdx')


if __name__ == '__main__':
    TestCase.run()
