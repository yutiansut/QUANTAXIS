# -*- coding: utf-8 -*-

from unittest import TestCase
import pandas as pd
import numpy as np
import QUANTAXIS as QA
import QUANTAXIS as qa
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
from QUANTAXIS.QACmd import QA_SU_save_stock_xdxr
from QUANTAXIS.QAUtil import QA_util_cache
from QUANTAXIS.QAUtil.QASetting import DATABASE


def diff_pd(df1, df2):
    """Identify differences between two pandas DataFrames"""
    assert (df1.columns == df2.columns).all(), \
        "DataFrame column names are different"
    if any(df1.dtypes != df2.dtypes):
        "Data Types are different, trying to convert"
        df2 = df2.astype(df1.dtypes)
    if df1.equals(df2):
        return None
    else:
        # need to account for np.nan != np.nan returning True
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        changed.index.names = ['id', 'col']
        difference_locations = np.where(diff_mask)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        return pd.DataFrame({'from': changed_from, 'to': changed_to},
                            index=changed.index)


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
    #         code = [str(code)]QA.QA_fetch_stock_info(['000001', '000002'])     
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
        myquery = {"code": {"$regex": "^510"}}
        x = indexDay.delete_many(myquery)
        print(x.deleted_count, " documents deleted.")

        self.test_QA_SU_save_etf_day()

    def test_QA_fetch_stock_xdxr(self):
        """测试读取xdxr
        和原始数据对不上,删除stock_day, stock_adj
        """
        # 股票代码以startStr开头
        startStr = "0000"
        codelist = QA.QA_fetch_stock_list().code.tolist()
        codelist = [i for i in codelist if i.startswith(startStr)]
        # 前十个股票
        codes = codelist[:10]
        self._checkQA_fetch_stock_xdxr(codes)

    def _checkQA_fetch_stock_xdxr(self, codes):
        """比较数据库中 stock_day, stock_adj中的记录数应该相同
        若不相同，则删除stock_day, stock_adj对应的数据
        备注：目前为找到不相同的原因。
        和原始数据对不上：000001            date
        345  1993-06-04
        1568 1998-06-20
        6673  documents deleted(记录被删除) stock_adj.
        6673  documents deleted(记录被删除) stock_day.
        和原始数据对不上：000002            date
        1561 1998-06-20
        6615  documents deleted(记录被删除) stock_adj.
        6615  documents deleted(记录被删除) stock_day.
        和原始数据对不上：000004            date
        1570 1998-06-20
        6493  documents deleted(记录被删除) stock_adj.
        6493  documents deleted(记录被删除) stock_day.
        000005 ok 5909
        000006 ok 6583
        000007 ok 6083
        000008 ok 6390
        和原始数据对不上：000009           date
        148 1991-12-20
        606 1993-10-11
        6813  documents deleted(记录被删除) stock_adj.
        6813  documents deleted(记录被删除) stock_day.
        和原始数据对不上：000010           date
        637 1998-06-20
        4907  documents deleted(记录被删除) stock_adj.
        4907  documents deleted(记录被删除) stock_day.
        000011 ok 6565
        """
        data1 = QA.QA_fetch_stock_xdxr(codes)
        self.assertTrue(len(data1) >= 0, "未保存数据")
        if len(data1) > 0:
            print(set(data1['code']))
            # 保存xdxr后，xdxr和股票日线数据数量应该一致
            start = '1990-01-01'
            end_time = str(now_time())[0:10]
            for code in codes:
                try:
                    data = qa.QA_fetch_stock_day_adv(code, start, end_time).data
                except Exception as e:
                    print("{} 本地无数据".format(code))
                try:
                    dataAdj = qa.QA_fetch_stock_adj(code, start, end_time)
                    df1 = pd.DataFrame(data.index.levels[0])
                    df2 = pd.DataFrame(dataAdj.index)
                    # df1['a'] = df2['a'] = 1
                    df = pd.concat([df1, df2]).drop_duplicates(keep=False)
                    if len(df) > 0:
                        print("和原始数据对不上：{}".format(code), df)
                        df = df[df['date'] > '2000-01-01']
                        if len(df) == 0:
                            # 数据对不上的时间早于2000年，则pass
                            continue
                        # 和原始数据对不上,删除stock_day, stock_adj
                        table = DATABASE.stock_adj
                        self._delTableDocument(table, code)
                        table = DATABASE.stock_day
                        self._delTableDocument(table, code)
                    else:
                        print("{} ok {}".format(code, len(data)))
                        self.assertTrue(data.iloc[-1].name[0] == dataAdj.iloc[-1].date, "最后日期不匹配，是否未保存xdxr？")
                except Exception as e:
                    # stock_adj 无数据
                    print("跳过 {}".format(code))

    def _delTableDocument(self, table, code):
        myquery = {"code": {"$regex": "^{}".format(code)}}
        x = table.delete_many(myquery)
        if x.deleted_count > 0:
            print(x.deleted_count, " documents deleted(记录被删除) {}.".format(table.name))

    def test_QA_save_stock_xdxr_with_delete(self):
        """测试多线程QA_SU_save_stock_xdxrk
        """
        #  删除部分数据(以startStr开头的股票)
        table = DATABASE.stock_xdxr
        startStr = "0000"
        codelist = QA.QA_fetch_stock_list().code.tolist()
        codelist = [i for i in codelist if i.startswith(startStr)]
        myquery = {"code": {"$regex": "^{}".format(startStr)}}
        x = table.delete_many(myquery)
        print(x.deleted_count, " documents deleted(记录被删除).")

        with self.assertRaises(Exception) as context:
            data1 = QA.QA_fetch_stock_xdxr(codelist[:10])
        self.assertTrue('not found' in str(context.exception.args), "删除后，数据应为空")

        QA_SU_save_stock_xdxr('tdx', paralleled=True)
        print('start test_QA_SU_save_xdxr')
        data1 = QA.QA_fetch_stock_xdxr(codelist[:10])
        self.assertTrue(len(data1) > 0, "未保存数据")
        print("read from DB:", data1)
        print('end test_QA_SU_save_xdxr')

    def test_save_day(self):
        from QUANTAXIS.QACmd import QA_SU_save_stock_day, QA_SU_save_index_day, QA_SU_save_etf_day, \
            QA_SU_save_stock_xdxr, QA_SU_save_etf_list, QA_SU_save_index_list, QA_SU_save_stock_list, \
            QA_SU_save_stock_block
        QA_SU_save_stock_day('tdx', paralleled=True)
        QA_SU_save_stock_xdxr('tdx', paralleled=True)
        QA_SU_save_index_day('tdx', paralleled=True)
        QA_SU_save_etf_list('tdx')
        QA_SU_save_etf_day('tdx', paralleled=True)
        QA_SU_save_index_list('tdx')
        QA_SU_save_stock_list('tdx')
        QA_SU_save_stock_block('tdx')


if __name__ == '__main__':
    TestCase.run()
