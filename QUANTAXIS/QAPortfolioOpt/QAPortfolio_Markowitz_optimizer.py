# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2018-2020 azai/Rgveda/GolemQuant
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
#
import datetime
import numpy as np
import pandas as pd

# 带收益预测的Markowitz动态平衡策略仓位自动优化器
# 原作者：韭菜Hulk
# 原链接1：https://www.joinquant.com/view/community/detail/4146bcfd6374efa6f691f51c31afed7f
# 原链接2：https://www.joinquant.com/view/community/detail/4146bcfd6374efa6f691f51c31afed7f
#
# 修改作者：阿财
# 原链接代码计算收益方差有Bug，收益预测部分是我自己琢磨完成的。
# 参考自：https://www.jianshu.com/p/0363bc4fdad4
# 下次迭代计划改为 Expected Shortfall 也就是大摩的 Conditional VAR 模型
# 参考文档：http://www.quantatrisk.com/2016/12/08/conditional-value-at-risk-normal-student-t-var-model-python/
# 数据接口适配 QUANTAXIS
#
import scipy as sp
import scipy.optimize as sco

from scipy import linalg as sla
from scipy import spatial

#import matplotlib.pyplot as plt
try:
    import talib
except:
    print('PLEASE run "pip install TALIB" to call these modules')
    pass
try:
    import QUANTAXIS as QA
    from QUANTAXIS.QAUtil.QAParameter import ORDER_DIRECTION
    from QUANTAXIS.QAData.QADataStruct import (
        QA_DataStruct_Index_min, 
        QA_DataStruct_Index_day, 
        QA_DataStruct_Stock_day, 
        QA_DataStruct_Stock_min,
        QA_DataStruct_CryptoCurrency_day,
        QA_DataStruct_CryptoCurrency_min,
        )
    from QUANTAXIS.QAIndicator.talib_numpy import *
    from QUANTAXIS.QAUtil.QADate_Adv import (
        QA_util_timestamp_to_str,
        QA_util_datetime_to_Unix_timestamp,
        QA_util_print_timestamp
    )
    from QUANTAXIS.QAUtil.QALogs import (
        QA_util_log_info, 
        QA_util_log_debug, 
        QA_util_log_expection
    )
except:
    print('PLEASE run "pip install QUANTAXIS" to call these modules')
    pass


class QA_Portfolio_Markowitz_optimizer():
    """
    带收益预测的Markowitz动态平衡策略仓位自动优化器，
    目前可以提供四种仓位优化方案：
    1、最大sharpe，
    2、最小方差，
    3、经典Markowitz动态平衡策略(抹零最小阈值5%)，
    4、基于高斯稳态收益预测的Markowitz动态平衡策略
    """
    _returns_baseline = None
    _data = None
    _rolling_wnd = 63
    _number_of_assets = 0
    _number_of_ticks = 0
    _codelist = []
    _codename = []

    def __init__(self,
                 codelist,
                 assets_returns,
                 ohlc,
                 codename=None):
        """
        初始化
        """
        self._returns_baseline = assets_returns
        self._codelist = codelist
        if (codename is not None):
            self._codename = codename

        self._data = ohlc

        # 数据预处理，需要填充nan，否则会没计算结果
        self._returns_np = np.nan_to_num(np.array(assets_returns), nan=0)
        self._number_of_ticks, self._number_of_assets = self._returns_np.shape


    # 按照资产种类收益，传入仓位权重，计算周期内收益率、风险、夏普率
    def statistics(self, 
                   weights, 
                   annualized_period=None):
        """
        传入仓位权重，输出周期内收益率、风险、夏普率，
        下次迭代计划改为 Expected Shortfall 大摩的 CVaR模型
        参考文档：http://www.quantatrisk.com/2016/12/08/conditional-value-at-risk-normal-student-t-var-model-python/
        """
        # 计算方式有两种，另一种为了方便用户比较结果进行年化计算
        if (annualized_period is not None):
            # 进行年化计算
            statis_wnd = annualized_period
        else:
            # 自定义计算，默认是3个月 63交易日
            statis_wnd = self._rolling_wnd

        weights = np.array(weights)
        pret = np.sum(self._returns_baseline.mean() * weights) * statis_wnd
        pvol = np.sqrt(np.dot(weights.T,
                                np.dot(self._returns_baseline.cov() * statis_wnd,
                                        weights)))

        return np.array([pret,pvol,pret / pvol])


    def Markowitz(self, dailyReturns, r, C):
        """
        这个在抄来的代码中据称使用了 tau 凸函数优化，但是我单独做测试的时候并未有证据显示
        sco.minimize 支持第三组参数(r, C, tau)，考虑使用 cvxopt 是否更为可行，
        但是 cvxopt 引用了 Intel numpy-mkl 对NUMA架构进程调度存在缺陷，对AMD CPU平台
        则构成负优化，只适合单CPU Intel /非AMD系统使用。
        """
        numData, numAsset = dailyReturns.shape
        w = 1.0 * np.ones(numAsset) / numAsset
        bound = tuple((0,1) for x in range(numAsset))
        constrain = ({'type':'eq', 'fun': lambda w: sum(w) - 1.0 })
    
        N = 500
        s_max = -100.0
        w_s = np.zeros(numAsset)
        r_s = 0.0
        C_s = 0.0
        for tau in [10 ** (5.0 * t / N - 1.0) for t in range(N)]:
            result = sco.minimize(self.objFunc, 
                                  w, (r, C, tau), 
                                  method='SLSQP', 
                                  constraints=constrain, 
                                  bounds=bound)  
            w_opt = result.x
        
            for i in range(numAsset):
                if w_opt[i] < 0.05:
                    w_opt[i] = 0.0
            w_opt = w_opt / sum(w_opt)
  
            r_opt = sum(w_opt * r)
            C_opt = np.dot(np.dot(w, C), w)
            s = r_opt / C_opt
        
            if s_max < s:
                s_max = s
                w_s = w_opt
                r_s = r_opt
                C_s = C_opt

        return w_s
        

    def objFunc(self, w, r, C, tau):
        val = tau * np.dot(np.dot(w, C), w) - sum(w * r)
        return val


    def getReturnCovariance(self, dailyReturns):
        """
        计算利润Returns的方差
        """
        numData, numAsset = dailyReturns.shape
        r = np.zeros(numAsset)
        for i in range(numAsset):
            r[i] = np.mean(dailyReturns[:, i])
        C = np.cov(dailyReturns.transpose())
    
        r = (1 + r) ** 255 - 1
        C = C * 255
    
        return r, C


    def getReturn(self, price):

        p = price.resample('M').last().pct_change().dropna().values
    
        x = np.atleast_2d(np.linspace(0,len(p),len(p))).T
    
        hypcov = [1.0,1.5,0.1]
        K_DD = self.isoSE(hypcov,x,x)
        L_DD = sla.cholesky(K_DD + np.eye(len(x)) * 0.01)
    
        mu = np.mean(p)
        y = p - mu
        alpha = np.atleast_2d(sla.cho_solve((L_DD,False), y)).T
        xt = np.atleast_2d(np.linspace(len(p) - 10,len(p) + 10,20)).T
        K_XD = self.isoSE(hypcov,xt,x)
        yt = mu + np.dot(K_XD,alpha)

        r = np.mean(yt[0].T)
        return r


    def isoSE(self, hypcov, X1=None, X2=None, diag=False):
        """
        """
        sf2 = np.exp(2 * hypcov[0])
        ell2 = np.exp(2 * hypcov[1])
        if diag:
            K = np.zeros((X1.shape[0],1))
        else:
            if X1 is X2:
                K = sp.spatial.distance.cdist(X1 / ell2, X1 / ell2, 'sqeuclidean')
            else:
                K = sp.spatial.distance.cdist(X1 / ell2, X2 / ell2, 'sqeuclidean')
        K = sf2 * np.exp(-K / 2)
        return K
    
    
    def min_func_sharpe(self, weights):
        """
        # 最大化夏普指数
        """
        return -self.statistics(weights)[2]
    
    
    def min_func_variance(self, weights):
        """
        # 最小化投资组合的方差
        """
        return self.statistics(weights)[1] ** 2
    

    def optimize_for_sharpe(self, verbose=False):
        """
        Markowitz投资组合优化，夏普率收益最大化(高风险模型适合牛市)
        """
        cons = ({"type":'eq',"fun":lambda x :np.sum(x) - 1})
        bnds = tuple((0,1) for x in range(self._number_of_assets))

        opts = sco.minimize(self.min_func_sharpe, 
                            self._number_of_assets * [1. / self._number_of_assets,], 
                            method="SLSQP", bounds=bnds, constraints=cons)

        rets_opts = {'info':u'Markowitz经典投资组合优化，夏普率收益最大化',
                     'weights': None}

        if (verbose == True):
            print(rets_opts['info'])

        rets_opts['weights'] = np.c_[self._codelist, 
                                     self._codename, 
                                     np.round(opts['x'],2)]

        rets_opts['statistics'] = np.c_[['预期年化收益率', '波动率', '夏普系数'],
                                        self.statistics(opts['x'], 
                                                        annualized_period=252).round(3)]
       
        return rets_opts


    def optimize_for_variance(self, verbose=False):
        """
        Markowitz投资组合优化，统计窗口3个月，方差最小优化(低风险模型，适合大盘下降趋势)。
        """
        cons = ({"type":'eq',"fun":lambda x :np.sum(x) - 1})
        bnds = tuple((0,1) for x in range(self._number_of_assets))

        optv = sco.minimize(self.min_func_variance, 
                            self._number_of_assets * [1. / self._number_of_assets,], 
                            method="SLSQP", bounds=bnds, constraints=cons)

        rets_optv = {'info':u'Markowitz经典投资组合优化，方差最小优化',
                     'weights': None}

        if (verbose == True):
            print(rets_optv['info'])

        rets_optv['weights'] = np.c_[self._codelist, 
                                     self._codename, 
                                     np.round(optv['x'],2)]

        rets_optv['statistics'] = np.c_[['预期年化收益率', '波动率', '夏普系数'],
                                        self.statistics(optv['x'], 
                                                        annualized_period=252).round(3)]
       
        return rets_optv


    def optimize_for_classical_markowitz(self, verbose=False):
        """
        基于经典Markowitz动态平衡策略
           我抄的，如果错了，那就是抄错了——阿财
        """
        r, C = self.getReturnCovariance(self._returns_np)
        w = self.Markowitz(self._returns_np, r, C)

        classical_markowitz = {'info':u'基于经典Markowitz动态平衡策略',
                               'weights': None}

        if (verbose == True):
            print(classical_markowitz['info'])

        classical_markowitz['weights'] = np.c_[self._codelist, 
                                               self._codename, 
                                               np.round(w,2)]

        classical_markowitz['statistics'] = np.c_[['预期年化收益率', '波动率', '夏普系数'],
                                        self.statistics(w, 
                                                        annualized_period=252).round(3)]

        return classical_markowitz


    def optimize_for_gp_markowitz(self, verbose=False):
        """
        基于带高斯稳态收益预测的Markowitz动态平衡策略
           我抄的，如果错了，那就是抄错了——阿财
        """
        r, C = self.getReturnCovariance(self._returns_np)
        for i in range(self._number_of_assets):
            price = self._data.select_code(self._codelist[i]).close
            r[i] = self.getReturn(price.reset_index(level=[1], drop=True))
    
        w = self.Markowitz(self._returns_np, r, C)

        gp_markowitz = {'info':u'基于带高斯稳态收益预测的Markowitz动态平衡策略',
                        'weights': None}

        if (verbose == True):
            print(gp_markowitz['info'])

        gp_markowitz['weights'] = np.c_[self._codelist, 
                                        self._codename, 
                                        np.round(w,2)]

        gp_markowitz['statistics'] = np.c_[['预期年化收益率', '波动率', '夏普系数'],
                                            self.statistics(w, 
                                                            annualized_period=252).round(3)]

        return gp_markowitz


    def verbose(self, opt_res, no_print=True):
        """
        解读资产配置优化结果
        """
        res_weights = pd.DataFrame(opt_res['weights'], columns=['code', 'name', 'weight'])
        res_weights['weight'] = res_weights['weight'].apply(float)
        ret_verbose = '按夏普率收益最大化计算有推荐仓位的股票：\n{}'.format(res_weights[res_weights['weight'].gt(0)])
        ret_verbose = '{}\n{}'.format(ret_verbose, 
                                     '剩下都是没有推荐仓位(牌面)的：\n{}'.format(res_weights.loc[res_weights['weight'].lt(0.001), ['code', 'name']].values))
        if (no_print == False):
            print(ret_verbose)
        return ret_verbose


def kline_returns_func(data, format='pd'):
    """
    计算单个标的每 bar 跟前一bar的利润率差值
    多用途函数，可以是 QA_DataStruct.add_func 调用（可以用于多标的计算），
    也可以是函数式调用（切记单独函数式调用不能多个标的混合计算）。
    Calculating a signal Stock/price timeseries kline's returns.
    For each data[i]/data[i-1] at series value of percentage.

    Parameters
    ----------
    data : (N,) array_like or pd.DataFrame or QA_DataStruct
        传入 OHLC Kline 序列。参数类型可以为 numpy，pd.DataFrame 或者 QA_DataStruct
        The OHLC Kline.
        在传入参数中不可混入多标的数据，如果需要处理多标的价格数据，通过
        QA_DataStruct.add_func 调用。
        It can prossessing multi indices/stocks by QA_DataStruct.add_func
        called. With auto splited into single price series 
        by QA_DataStruct.add_func().
        For standalone called, It should be only pass one stock/price series. 
        If not the result will unpredictable.
    format : str, optional
        返回类型 默认值为 'pd' 将返回 pandas.DataFrame 格式的结果
        可选类型，'np' 或 etc 返回 nparray 格式的结果
        第一个 bar 会被填充为 0.
        Return data format, default is 'pd'. 
        It will return a pandas.DataFrame as result.
        If seted as string: 'np' or etc string value, 
        It will return a nparray as result.
        The first bar will be fill with zero.

    Returns
    -------
    kline returns : pandas.DataFrame or nparray
        'returns' 跟前一收盘价格变化率的百分比

    """
    from QUANTAXIS.QAData.base_datastruct import _quotation_base
    if isinstance(data, pd.DataFrame) or \
        (isinstance(data, _quotation_base)):
        data = data.close

    if (format == 'pd'):
        kline_returns = pd.DataFrame(data.pct_change().values,
                                     columns=['returns'], 
                                     index=data.index)
        return kline_returns
    else:
        return np.nan_to_num(data.pct_change().values, nan=0)


if __name__ == '__main__':
    # 股票代码，如果选股以后：我们假设有这些代码
    codelist = ['159919', '159908', '159902', '510900', 
                '513100', '512980', '515000', '512800', 
                '512170', '510300', '159941', '512690',
                '159928']

    # 获取ETF基金中文名称，只是为了看得方便，交易策略并不需要ETF基金中文名称
    stock_names = QA.QA_fetch_etf_name(codelist)
    codename = [stock_names.at[code, 'name'] for code in codelist]

    # 股票代码，我直接用我的选股程序获取选股列表。这段别人运行不了，所以注释掉了
    #position_signals = position(portfolio='sharpe_scale_patterns_day',
    #                            frequency='day',
    #                            market_type=QA.MARKET_TYPE.STOCK_CN,
    #                            verbose=False)
    #codelist = position_signals.index.get_level_values(level=1).to_list()

    # 获取股票中文名称，只是为了看得方便，交易策略并不需要股票中文名称
    #stock_names = QA.QA_fetch_stock_name(codelist)
    #codename = [stock_names.at[code, 'name'] for code in codelist]
    #print(codename)

    #data_day = QA.QA_fetch_stock_day_adv(codelist,
    #    start='2014-01-01',
    #    end='{}'.format(datetime.date.today())).to_qfq()

    # 读取 ETF基金 日线，存在index_day中
    data_day = QA.QA_fetch_index_day_adv(codelist,
        start='2014-01-01',
        end='{}'.format(datetime.date.today()))

    # 收益率序列
    rets_jotion = data_day.add_func(kline_returns_func)
    returns = pd.DataFrame(columns=codelist, 
                           index=data_day.data.index.get_level_values(level=0).unique())
    for code in codelist:
        returns[code] = rets_jotion.loc[(slice(None), code), 
                                        :].reset_index(level=[1], drop=True)

    markowitz_opt = QA_Portfolio_Markowitz_optimizer(
        codelist=codelist,
        codename=codename,
        ohlc=data_day,
        assets_returns=returns,)

    opts = markowitz_opt.optimize_for_sharpe()
    print(opts['info'])
    print(markowitz_opt.verbose(opts))
    print(opts['statistics'])

    optv = markowitz_opt.optimize_for_variance()
    print(optv['info'])
    print(markowitz_opt.verbose(optv))
    print(optv['statistics'])

    optc = markowitz_opt.optimize_for_classical_markowitz()
    print(optc['info'])
    print(markowitz_opt.verbose(optc))
    print(optc['statistics'])

    optgpm = markowitz_opt.optimize_for_gp_markowitz()
    print(optgpm['info'])
    print(markowitz_opt.verbose(optgpm))
    print(optgpm['statistics'])