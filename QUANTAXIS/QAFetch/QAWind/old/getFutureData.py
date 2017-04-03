# -*- coding:utf-8 -*
from WindPy import w



w.start()
Data=w.wsd("RB1702.SHF", "open,high,low,close,volume", "2016-02-09", "2017-03-11", "TradingCalendar=SHFE;Fill=Previous")

data=Data.Data;
print data[0]