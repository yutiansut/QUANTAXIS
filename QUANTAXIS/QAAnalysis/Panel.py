import QUANTAXIS as QA
from fitter import Fitter
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import laplace, norm
import matplotlib.pyplot as plt
from functools import lru_cache

class panelData:

    def __init__(self, prices:pd.DataFrame, analysis_gap =10):
        """
        t day   --> signal


        t+1day open --> twap buy

        t+6day open --> twap sell

        return5 = t+6day open/ t+1day open 

        closeframe = [t-analysis_gap, t] close panel 

        """
        
        
        self.data =  prices
        self.analysis_gap = analysis_gap
        
        if len(self.timeaxis)<analysis_gap+5:
            raise Exception('data length not enough')

    @staticmethod
    def make_returns( data):
        return data/data.iloc[0]
    
    def yaxis(self):
        return self.data.columns
    
    
    def yaxis(self):
        return self.data.index.levels[1]
    @property
    @lru_cache()
    def timeaxis(self):
        return  self.data.index.levels[0]
    
    @property
    @lru_cache()
    def dayaxis(self):
        """
        sometimes the factor data are manufactored by minute data
        using dayaxis to transform
        """
        index = self.data.index.remove_unused_levels()
        return index.levels[0
                               ] if 'date' in self.data.index.names else sorted(
                                   list(set(self.datetime.date))
                               )
        
    
    @property
    @lru_cache()
    def closeframe(self):
        return self.data.close.reset_index().pivot(index='date', columns='code', values='close').sort_index()
    @property
    @lru_cache()
    def nextopenframe(self):
        return self.data.open.reset_index().pivot(index='date', columns='code', values='open').sort_index().shift(-1)
    
    @property
    @lru_cache()
    def return5(self):

        return self.nextopenframe.pct_change(5).shift(-6)
        
    def add_func(self, func ,*arg, **kwargs):
        
        f1 =  self.closeframe.rolling(self.analysis_gap).apply(func, *arg, **kwargs)
        
        
        res = pd.concat([f1.unstack(), self.return5.unstack()], axis=1).dropna(axis=0)
        res.columns =['func', 'ret5']
        return res #staicAnalysis(res.dropna(), self.timeaxis[-6] )


    
    
class staicAnalysis():
    def __init__(self, data, date):
        self.data =  data
        self.date =  date
    def __repr__(self):
        return 'single panel analysis {}'.format(self.date)
    
    @property
    def rankic(self):
        return self.data.corr(method='spearman')
    
    def plot_hist(self):
        return self.data.func.plot.hist()
    
    def standardize(self):
        func = sc.stats.mstats.winsorize(self.data.func,0.01)

        self.data =self.data.assign(stdfunc =  ( func -  func.mean())/func.std())
        
    def fitdistribution(self):
        self.standardize()
        f = Fitter(self.data.func)
        f.fit()
        # may take some time since by default, all distributions are tried
        # but you call manually provide a smaller set of distributions
        return f.summary()