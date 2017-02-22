# -*- coding:utf-8 -*-


from WindPy import *
w.start()   
from datetime import datetime
import talib
#先搞上期
#数据库

data=w.wsd("AU1703.SHF", "pre_close,open,high,low,close,adjfactor,mf_vol,mf_amt_ratio,mf_vol_ratio,theoryvalue,delta,gamma,vega,theta,rho", "2017-01-23", "2017-02-22", "TradingCalendar=SHFE;Fill=Previous")
print data.Data