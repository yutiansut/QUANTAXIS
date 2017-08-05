# coding:utf-8

import requests
import pandas as pd
import numpy as np



def get_k_data_year(code,year,if_fq):
    data_=[]
    url='http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js'%(code,if_fq,year)
    for item in requests.get(url).text.split('\"')[3].split(';'):
        data_.append(item.split(',')

    return pd.DataFrame(data_,index=list(np.asarray(data_).T[0]),columns=['date','open','high','low','close','volume','amount','factor'])