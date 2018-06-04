
import os
import sys
import configparser
from ctypes import cdll
sys.path.append(os.path.dirname(__file__))

account_info = dict()
account_info['ip_hq'] = 'tcp://180.168.146.187:10011'
account_info['ip_trade'] = 'tcp://180.168.146.187:10001'
account_info['broker_id'] = "9999"

account_info['account'] = input('account')
account_info['pwd'] = input('password')

api = cdll.LoadLibrary('{}/hqdll.dll'.format(os.path.dirname(__file__)))

# 下单唯一标号
OrderId = 0

# instrument_list = ['rb1810','j1809']
# instrument_list = ['T1806','TF1806']
instrument_list = ['ag1806', 'au1806', 'cu1806', 'rb1810', 'j1809']
instrument_price = dict()
for instrument in instrument_list:
    instrument_price[instrument] = 0.0
