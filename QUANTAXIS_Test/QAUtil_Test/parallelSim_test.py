# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     parallelSim_test
   Description :
   Author :       pchaos
   date：          19-3-12
-------------------------------------------------
   Change Activity:
                   19-3-12:
-------------------------------------------------
"""
from unittest import TestCase
from QUANTAXIS.QAUtil import ParallelSim

__author__ = 'pchaos'


def add(x, y):
    return x + y


class TestParallelSim(TestCase):
    def test_get_results(self):
        pl = ParallelSim()
        counts = 5000
        aiter = [(x, x + 1) for x in range(counts)]
        pl.add(add, aiter)
        data = list(pl.get_results())
        self.assertTrue(len(data) == counts, '返回结果的数量和原始数据布匹配：{} {}'.format(len(data), counts))
        results = [2 * x + 1 for x in range(counts)]  # 计算结果
        diff = [x for x in results if x not in data]
        self.assertTrue(len(diff) == 0, '计算结果应该与实际结果完全匹配。实际差别为：{}'.format(diff))

