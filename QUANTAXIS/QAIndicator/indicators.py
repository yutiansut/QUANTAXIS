#coding:utf-8
import pandas as pd
"""
QUANTAXIS  指标计算
"""

def QA_indicator_ma(data,ma):
    return  pd.rolling_mean(data, ma)

def QA_indicator_sma(data,ma):
    return  pd.ewma(data, span=ma)

def QA_indicator_lb(data):
    pass


def QA_indicator_rsi(N1=6, N2=12, N3=24):
    """
    RSI 相对强弱指标
    """
    pass