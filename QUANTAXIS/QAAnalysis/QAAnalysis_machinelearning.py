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
import numpy as np
import scipy.signal as signal

from sklearn import mixture
from sklearn.cluster import AgglomerativeClustering
from sklearn.linear_model import LinearRegression

"""
一个通用的可以接入不同模型的类
"""


class QAAnalysis_Machine_Learning():
    def __init__(self, *args, **kwargs):
        pass

    def training(self):
        pass

    def data_co(self):
        pass

    def cross_valid(self):
        pass

    def load_modules(self):
        pass

    def load_data(self):
        pass


def machine_learning_wavelet_func(data):
    """
    使用机器学习算法统计分析趋势，使用无监督学习的方法快速的识别出K线走势状态。
    简单(不需要太精确，精确的买卖点由个人的指标策略控制完成)划分出波浪区间。
    对不同的波浪就可以继续采用定制化的量化策略。
    """
    def zen_in_wavelet_func(data):
        """
        Find zen trend in only one wavelet.
        缠论 ——> 在一个波浪中。
        这是很有效的算法，能用缠论(或者随便什么你们喜欢称呼的名字)在波浪中找到趋势，
        问题是缠论有个毛病是波浪套波浪，波浪套波浪，而这个算法只会找出给定象限内的
        最大趋势（划重点），所以需要提前把一条K线“切”成（可以盈利或者我们自己交易
        系统所选择的波段区间内）最小波浪，然后函数送进来，Duang！趋势就判断出来了。
        """
        highp = data.high.values #np.r_[data.high.values[:5], TA_HMA(data.high.values, 5)[6:]]
        lowp = data.high.values #np.r_[data.low.values[:5], TA_HMA(data.low.values, 5)[6:]]
        openp = data.open.values
        closep = data.close.values

        bV = lowp[signal.argrelextrema(lowp,np.less)]
        bP = signal.argrelextrema(lowp,np.less)[0]

        d,p = LIS(bV)

        idx = []
        for i in range(len(p)):
            idx.append(bP[p[i]])

        qV = highp[signal.argrelextrema(highp,np.greater)]
        qP = signal.argrelextrema(highp,np.greater)[0]

        qd,qp = LDS(qV)

        qidx = []
        for i in range(len(qp)):
            qidx.append(qP[qp[i]])

        zen_cross = pd.DataFrame(columns=['ZEN_TIDE_CROSS', 
                                          'ZEN_TIDE_CROSS_JX',
                                          'ZEN_TIDE_CROSS_SX'], 
                                 index=data.index)
        zen_cross.iloc[idx, zen_cross.columns.get_loc('ZEN_TIDE_CROSS')] = 1
        zen_cross.iloc[qidx, zen_cross.columns.get_loc('ZEN_TIDE_CROSS')] = -1
        zen_cross.iloc[idx, zen_cross.columns.get_loc('ZEN_TIDE_CROSS_JX')] = 1
        zen_cross.iloc[qidx, zen_cross.columns.get_loc('ZEN_TIDE_CROSS_SX')] = 1
        return zen_cross


    # 统计学习方法分析大趋势：数据准备
    highp = data.high.values
    lowp = data.low.values
    openp = data.open.values
    closep = data.close.values

    # DPGMM 聚类
    X = []
    idx = []
    lag = 30
    for i in range(len(closep)):
        left = max(0,i - lag)
        right = min(len(closep) - 1,i + lag)
        l = max(0,i - 1)
        r = min(len(closep) - 1,i + 1)
        for j in range(left,right):
            minP = min(closep[left:right])
            maxP = max(closep[left:right])
            low = 1 if closep[i] <= closep[l] and closep[i] < closep[r] else 0
            high = 1 if closep[i] >= closep[l] and closep[i] > closep[r] else 0
        x = [i, closep[i], minP, maxP, low, high]
        X.append(x)
        idx.append(i)
    X = np.array(X)
    idx = np.array(idx)

    dpgmm = mixture.BayesianGaussianMixture(n_components=max(int(len(closep) / 10), 16), 
                                            max_iter=1000, 
                                            covariance_type='spherical', 
                                            weight_concentration_prior_type='dirichlet_process')

    # 训练模型不含最后一个点
    dpgmm.fit(X[:-1])
    y_t = dpgmm.predict(X)

    machine_learning_trend = pd.DataFrame(columns=['CLUSTER_GROUP', 
                                                   'REGRESSION_PRICE',
                                                   'REGRESSION_SLOPE',
                                                   'CLUSTER_GROUP_DENSITY',
                                                   'ZEN_TIDE_CROSS', 
                                                   'ZEN_TIDE_CROSS_JX', 
                                                   'ZEN_TIDE_CROSS_SX'], index=data.index)
    machine_learning_trend['CLUSTER_GROUP'] = y_t

    # (假设)我们对这条行情的走势一无所知，使用机器学习可以快速的识别出走势，划分出波浪。
    # DPGMM聚类 将整条行情大致分块，这个随着时间变化会有轻微抖动。
    # 所以不适合做精确买卖点控制。但是作为趋势判断已经足够了。
    #print('自动划分为：{:d} 个形态走势'.format(len(np.unique(y_t))))

    # 以DPGMM聚类进行分段，计算线性回归斜率
    lr = LinearRegression()       
    for c in np.unique(y_t):
        inV = []
        outV = []
        for i in range(len(closep)):
            if y_t[i] - c == 0:
                inV.append(i)
                outV.append(closep[i])

        inV = np.atleast_2d(np.array(inV)).T
        outV = np.array(outV)
        lr.fit(inV,outV)
            
        estV = lr.predict(inV)

        # 数字索引降维
        inV = np.reshape(inV, len(inV))
        machine_learning_trend.iloc[inV, machine_learning_trend.columns.get_loc('REGRESSION_SLOPE')] = lr.coef_[0]

    # DPGMM 聚类分析完毕

    # 下降趋势检测，
    # 再次价格回归。波浪下降趋势一定DEA下沉到零轴下方，所以依次扫描所有聚类，
    # 在时间轴的近端发现有DEA下沉到零轴下方，作为一个分组进行统计学习进行趋势判断。
    macd_cross = macd_cross_func(data)
    machine_learning_trend = machine_learning_trend.assign(CLUSTER_GROUP_GAP=(machine_learning_trend['CLUSTER_GROUP'].diff() != 0).apply(int))
    machine_learning_trend['CLUSTER_GROUP_BEFORE'] = Timeline_Integral_with_cross_before(machine_learning_trend['CLUSTER_GROUP_GAP'])
    machine_learning_trend['CLUSTER_GROUP_GAP'] = ((machine_learning_trend['CLUSTER_GROUP_GAP'] == 1) & (macd_cross['DEA'] < 0))

    # 第一个bar自动成为首个趋势分段（可能DEA > 0）
    machine_learning_trend.iloc[0, machine_learning_trend.columns.get_loc('CLUSTER_GROUP_GAP')] = True

    # 现在机器学习程序自己划分出了可能的存在一个完整波浪趋势的区间（不用人干预，太特么感动了！）
    trend_cluster_groups = machine_learning_trend[machine_learning_trend['CLUSTER_GROUP_GAP'].apply(lambda x: x == True)]

    # 接下来逐个进行分析，再把结果装配起来。
    trend_cluster_groups['CLUSTER_GROUP_FROM'] = trend_cluster_groups.apply(lambda x: machine_learning_trend.index.get_level_values(level=0).get_loc(x.name[0]), axis=1)
    trend_cluster_groups['CLUSTER_GROUP_TO'] = trend_cluster_groups.apply(lambda x: machine_learning_trend.index.get_level_values(level=0).get_loc(x.name[0]), axis=1)
    trend_cluster_groups['CLUSTER_GROUP_TO'] = trend_cluster_groups['CLUSTER_GROUP_TO'].shift(-1)
    trend_cluster_groups.iloc[-1, trend_cluster_groups.columns.get_loc('CLUSTER_GROUP_TO')] = len(machine_learning_trend)
    trend_cluster_groups['CLUSTER_GROUP_TO'] = trend_cluster_groups['CLUSTER_GROUP_TO'].apply(int)
    zen_cross_columns_idx = [machine_learning_trend.columns.get_loc('ZEN_TIDE_CROSS'), 
                            machine_learning_trend.columns.get_loc('ZEN_TIDE_CROSS_JX'),
                            machine_learning_trend.columns.get_loc('ZEN_TIDE_CROSS_SX'),]
    zen_cross = []
    for index, trend_cluster_group in trend_cluster_groups.iterrows():
        trend_cluster_group_range = range(trend_cluster_group['CLUSTER_GROUP_FROM'],trend_cluster_group['CLUSTER_GROUP_TO'])
        trend_cluster_data = data.iloc[trend_cluster_group_range,]
        zen_cross.append(zen_in_wavelet_func(trend_cluster_data))
    zen_cross = pd.concat(zen_cross)
    #print(trend_cluster_groups)
    #print(machine_learning_trend.index.difference(zen_cross.index))
    #print(len(zen_cross.index), len(machine_learning_trend.index))
    machine_learning_trend.iloc[:, zen_cross_columns_idx] = zen_cross
    machine_learning_trend.iloc[0, machine_learning_trend.columns.get_loc('ZEN_TIDE_CROSS_JX')] = 1
    machine_learning_trend.iloc[0, machine_learning_trend.columns.get_loc('ZEN_TIDE_CROSS_SX')] = 1
    machine_learning_trend['ZEN_TIDE_CROSS_JX'] = Timeline_Integral_with_cross_before(machine_learning_trend['ZEN_TIDE_CROSS_JX'])
    machine_learning_trend['ZEN_TIDE_CROSS_SX'] = Timeline_Integral_with_cross_before(machine_learning_trend['ZEN_TIDE_CROSS_SX'])
    machine_learning_trend['CLUSTER_GROUP_DENSITY'] = machine_learning_trend.assign()
    for c in np.unique(y_t):
        # 计算趋势密度
        trend_cluster_group = machine_learning_trend.query('CLUSTER_GROUP=={}'.format(c))
        machine_learning_trend.loc[trend_cluster_group.index, 'CLUSTER_GROUP_DENSITY'] = trend_cluster_group['ZEN_TIDE_CROSS_SX'].sum()/(trend_cluster_group['ZEN_TIDE_CROSS_JX'].sum()+trend_cluster_group['ZEN_TIDE_CROSS_SX'].sum())
        #print(len(trend_cluster_group), trend_cluster_group['ZEN_TIDE_CROSS_JX'].sum(), trend_cluster_group['ZEN_TIDE_CROSS_SX'].sum(),)
        #print('Gruop #{}'.format(c), 'density:', trend_cluster_group['ZEN_TIDE_CROSS_SX'].sum()/(trend_cluster_group['ZEN_TIDE_CROSS_JX'].sum()+trend_cluster_group['ZEN_TIDE_CROSS_SX'].sum()), trend_cluster_group['REGRESSION_SLOPE'].max())

    machine_learning_trend['ZEN_TIDE_MEDIAN'] = int(min(machine_learning_trend['ZEN_TIDE_CROSS_JX'].median(), machine_learning_trend['ZEN_TIDE_CROSS_SX'].median()))
    machine_learning_trend['REGRESSION_PRICE'] = jhta.LSMA(data, price='close', n = machine_learning_trend['ZEN_TIDE_MEDIAN'].min())
    return machine_learning_trend