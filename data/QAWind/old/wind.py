from WindPy import *
w.start()
from datetime import datetime
#前复权：复权后价格=[(复权前价格-现金红利)+配(新)股价格×流通股份变动比例]÷(1+流通股份变动比例)
#后复权：复权后价格=复权前价格×(1+流通股份变动比例)+现金红利
import talib