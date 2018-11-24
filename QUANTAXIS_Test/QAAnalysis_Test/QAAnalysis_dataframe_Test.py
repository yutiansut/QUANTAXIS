import unittest

import QUANTAXIS as QA


class Test_QAAnalysis_dataframe(unittest.TestCase):
    def test_QAAnalysis_stock(self):
        
        # data = QA.QA_fetch_stock_day_adv(
        #     '600066', '2013-12-01', '2017-10-01')  # [可选to_qfq(),to_hfq()]d
        # s = QA.QAAnalysis_stock(data)
        # # s 的属性是( < QAAnalysis_Stock > )

        # s.open  # 开盘价序列
        # s.close  # 收盘价序列
        # s.high  # 最高价序列
        # s.low  # 最低价序列
        # s.vol  # 量
        # s.volume  # 同vol
        # s.date  # 日期
        # s.datetime
        # s.index  # 索引
        # s.price  # 平均价(O+H+L+C)/4
        # s.mean  # price的平均数
        # s.max  # price的最大值
        # s.min  # price的最小值
        # s.mad  # price的平均绝对偏差
        # # s.mode  # price的众数(没啥用)
        # s.price_diff  # price的一阶差分
        # s.variance  # price的方差
        # s.pvariance  # price的样本方差
        # s.stdev  # price的标准差
        # s.pstdev  # price的样本标准差
        # s.mean_harmonic  # price的调和平均数
        # s.amplitude  # price的振幅[极差]
        # s.skewnewss  # price的峰度 (4阶中心距)
        # s.kurtosis  # price的偏度 (3阶中心距)
        # s.pct_change  # price的百分比变化序列

        # s.add_func(QA.QA_indicator_CCI)  # 指标计算, 和DataStruct用法一致
        
        print("finished test")