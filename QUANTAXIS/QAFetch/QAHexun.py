
# shibor  
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=1000000000000000&t=31&ts=1531823886747 # 隔夜
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0100000000000000&t=31&ts=1531823650473 # 一周
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0010000000000000&t=31&ts=1531823827297 # 两周
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0001000000000000&t=31&ts=1531823861493 # 三周
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000100000000000&t=31&ts=1531823916576 # 一个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000010000000000&t=31&ts=1531823987451 # 两个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000001000000000&t=31&ts=1531824032847 # 三个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000100000000&t=31&ts=1531824046563 # 四个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000001000000&t=31&ts=1531824062892 # 六个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000000100000&t=31&ts=1531824078992 # 七个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000000010000&t=31&ts=1531824078992 # 八个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000000001000&t=31&ts=1531824078992 # 九个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000000000100&t=31&ts=1531824078992 # 十个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000000000010&t=31&ts=1531824078992 # 十一个月
#http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r=0000000000000001&t=31&ts=1531824091973 # 十二个月

import requests
import time
import pandas as pd
from QUANTAXIS.QAFetch.base import headers
from copy import deepcopy
headers_hexun = deepcopy(headers)
headers_hexun['Referer'] = 'http://data.bank.hexun.com/'
headers_hexun['Host'] = 'data.bank.hexun.com'
headers_hexun['X-Requested-With'] = 'XMLHttpRequest'


chibor_url = 'http://data.bank.hexun.com/dataprovider/BankOfferedrateFlash.ashx?r={}&t=31&ts={}'

def QA_fetch_get_chibor(frequence='1D'):
    if frequence == '1D':
        d = '1000000000000000'
    elif frequence == '1W':
        d = '0100000000000000'
    elif frequence == '2W':
        d = '0010000000000000'
    elif frequence == '3W':
        d = '0001000000000000'
    elif frequence == '1M':
        d = '0000100000000000'
    elif frequence == '2M':
        d = '0000010000000000'
    elif frequence == '3M':
        d = '0000001000000000'
    elif frequence == '4M':
        d = '0000000100000000'
    elif frequence == '5M':
        d = '0000000010000000'
    elif frequence == '6M':
        d = '0000000001000000'
    elif frequence == '7M':
        d = '0000000000100000'
    elif frequence == '8M':
        d = '0000000000010000'
    elif frequence == '9M':
        d = '0000000000001000'
    elif frequence == '10M':
        d = '0000000000000100'
    elif frequence == '11M':
        d = '0000000000000010'
    elif frequence == '12M':
        d = '0000000000000001'

    res = requests.get(chibor_url.format(d, int(time.time()*1000)-1), headers= headers_hexun).text
    data = [{'date':d[12:22],'1D':float(d[31:35])} for d in res.split('\r\n') if d[1:5] == 'date']
    return pd.DataFrame(data).set_index('date')