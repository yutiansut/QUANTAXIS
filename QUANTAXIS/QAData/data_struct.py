# coding :utf-8

"""
定义一些可以扩展的数据结构

方便序列化/相互转换

"""

import pandas as pd
import numpy as np

from QUANTAXIS.QAUtil import QA_Setting
class QA_Data_Min():
    def init(self):
        self.open,self.close=np.array()
        self.high=np.array()
        self.date_index=pd.Series()
    def to_dataframe(self):
        return pd.DataFrame([self.open,self.close])

    def resample(self,type='d'):
        return self.to_dataframe().resample('1d').ohlc()
    def to_csv(self):
        pass
    def to_list(self):
        pass
    def to_mongo(self,collection=QA_Setting.client):
        pass

    """
    最好这个可以被复用，以及被快速转化为protobuf
    
    
    """