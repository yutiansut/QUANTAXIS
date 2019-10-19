# -*- coding: utf-8 -*-
"""
-------------------------------------------------

@File    : test_qa_setting.py

Description :

@Author :       pchaos

date：          18-6-20
-------------------------------------------------
Change Activity:
               18-6-20:
@Contact : p19992003#gmail.com                   
-------------------------------------------------
"""
from unittest import TestCase
import json
from QUANTAXIS.QAUtil import QA_Setting
from QUANTAXIS.QAUtil.QASetting import exclude_from_stock_ip_list, stock_ip_list
import QUANTAXIS as QA


class Testqa_setting(TestCase):
    def test_get_config(self):
        qasetting = QA_Setting()
        # default = qasetting.get_config()
        # self.assertTrue('mongodb://' in default, '不是mongodb：{}'.format(default))

        excludejson = {'ip': '1.1.1.1', 'port': 7709}
        alist = []
        alist.append(excludejson)
        ipexclude = qasetting.get_config(section='IPLIST', option='exclude', default_value=alist)
        print(ipexclude)
        self.assertTrue(excludejson in json.loads(ipexclude), '原始数据：{}， 读取数据：{}'.format(excludejson, ipexclude))

    def test_exclude_from_stock_ip_list(self):
        excludejson = {'ip': '161.153.144.179', 'port': 7709}
        stock_ip_list.append(excludejson)
        self.assertTrue(excludejson in stock_ip_list, '此ip {} 不在 stock_ip_list中'.format(excludejson))
        alist = []
        alist.append(excludejson)
        exclude_from_stock_ip_list(alist)
        self.assertFalse(excludejson in stock_ip_list, '此ip {} 在 stock_ip_list中'.format(excludejson))

        alist = []
        exclude_from_stock_ip_list(alist)

        excludejson = {'ip': '161.153.144.179', 'port': 7709}
        stock_ip_list.append(excludejson)
        alist.append(excludejson)
        excludejson = {'ip': '162.153.144.179', 'port': 7709}
        alist.append(excludejson)
        stock_ip_list.append(excludejson)
        for exc in alist:
            self.assertTrue(exc in stock_ip_list)
        exclude_from_stock_ip_list(alist)
        self.assertFalse(excludejson in stock_ip_list, '此ip {} 在 stock_ip_list中'.format(excludejson))

        data = QA.QAFetch.QATdx.QA_fetch_get_stock_day('00001', '2017-01-01', '2017-01-31')
        self.assertTrue(len(data) > 15)