# coding:utf-8


from .base import base_datastruct
import numpy as np
class QA_Datastruct_ohlc(base_datastruct):
    

    def __init__(self,data):
        self.high=np.asarray(data).T[2]
    def tran_(self):
        pass
    def standard(self):
        pass


    