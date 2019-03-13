# -*- coding: utf-8 -*-

from unittest import TestCase
import QUANTAXIS as QA
from QUANTAXIS.QAFetch import QATdx
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_day, select_best_ip, ping
from QUANTAXIS.QAUtil.QASetting import QA_Setting
import datetime


class TestSelect_best_ip(TestCase):
    def test_select_best_ip(self):
        best_ip = select_best_ip()
        ip = best_ip['stock']['ip']
        port = best_ip['stock']['port']
        self.assertTrue(isinstance(ip, str), '未获取到ip')
        self.assertTrue(isinstance(port, int), '未获取到端口号')
        self.assertTrue(ping(ip, port, 'stock') < datetime.timedelta(0, 1, 0), '地址ping不通： {} {} {}'.format(ip, port, ping(ip, port, 'stock')))
        # ip = best_ip['future']['ip']
        # port = best_ip['future']['port']
        # self.assertTrue(ping(ip, port, 'stock') < datetime.timedelta(0, 1, 0), '地址ping不通： {} {} {}'.format(ip, port, ping(ip, port, 'stock')))

        code = '000001'
        days = 300
        start = datetime.datetime.now().date() - datetime.timedelta(days)
        end = datetime.datetime.now().date() - datetime.timedelta(10)
        data = QA_fetch_get_stock_day(code, start_date=start, end_date=end)
        print(data)
        self.assertTrue(len(data) > (end - start).days / 2,
                        '返回数据个数不匹配，数据长度：{},天数（包含节假日）：{}'.format(len(data), (end - start).days / 2))

        default_ip = {'stock': {'ip': None, 'port': None},
                      'future': {'ip': None, 'port': None}}
        qasetting = QA_Setting()
        qasetting.set_config(
            section='IPLIST', option='default', default_value=default_ip)
        best_ip = select_best_ip()
        ip = best_ip['future']['ip']
        port = best_ip['future']['port']
        self.assertTrue(isinstance(ip, str), '未获取到ip')
        self.assertTrue(isinstance(port, int), '未获取到端口号')
        data = QA_fetch_get_stock_day(code, start, end)
        self.assertTrue(len(data) > (end - start).days / 2,
                        '返回数据个数不匹配，数据长度：{},天数（包含节假日）：{}'.format(len(data), (end - start).days / 2))
