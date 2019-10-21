# coding:utf-8
"""
数据获取来源:http://www.9qihuo.com/qihuoshouxufei
保存为excel简单处理之后使用一下代码处理,记录一下方便以后更新:

def get_name_before_digit(arr):
    for i in range(len(arr)):
        if arr[i].isdigit():
            return arr[:i]

def get_commision_by_detail(detail):
    if detail['开仓'][-1]=='元':
        return dict(commission_coeff_peramount=0,
              commission_coeff_pervol=np.round(float(detail['开仓'][:-1]),5),
              commission_coeff_today_peramount=0,
              commission_coeff_today_pervol=np.round(float(detail['平今'][:-1]),5))
    else:
        return dict(commission_coeff_peramount=np.round(float(detail['开仓'][:-1])*0.001,5),
              commission_coeff_pervol=0,
              commission_coeff_today_peramount=np.round(float(detail['平今'][:-1])*0.001,5),
              commission_coeff_today_pervol=0)

excel_path="/xxx"
df=pd.read_excel(excel_path)

# 添加交易所代码,需要手动处理一下或者在excel中处理
exc=np.array(['xxxx']*len(df))
exc[:160]=EXCHANGE_ID.SHFE
exc[160:293]=EXCHANGE_ID.DCE
exc[293:425]=EXCHANGE_ID.CZCE
exc[425:446]='INE'
df['exchange']=exc

# add code和name列
name_code=df['合约品种'].values
df['name']=list(map(lambda x:get_name_before_digit(x),name_code.split('(')[0]))
df['code']=list(map(lambda x:get_name_before_digit(
    x).upper(),name_code.split('(')[1]))

# 获取所有合约的detail并添加到details中
details={}
for i in range(len(df)):
    detail=df.ix[i,:]
    code=detail['code']
    if code not in details:
        d2=df[df['code']==code]
        index=np.where(d2['买开保证金%']==min(d2['买开保证金%']))[0][0]
        detail=d2.iloc[index]
        details[code]=dict(name=detail['name'],
                             unit_table=detail['每手数量'],
                              price_tick=detail['每跳价差/元'],
                             buy_frozen_coeff=detail['买开保证金%']*0.01,
                             sell_frozen_coeff=detail['卖开保证金%']*0.01,
                          exchange=detail['exchange'])
        details[code]=dict(details[code],**get_commision_by_detail(detail))
"""

import pandas as pd
from functools import lru_cache
from QUANTAXIS.QAUtil.QAParameter import EXCHANGE_ID


class MARKET_PRESET:

    def __init__(self):
        """
              unit_table 合约乘数
              price_tick 每跳差价

              buy_frozen_coeff 多头开仓保证金系数
              sell_frozen_coeff 空头开仓保证金系数

              commission_coeff_peramount 按总量计算手续费系数
              commission_coeff_pervol 按手数计算的手续费系数
              commission_coeff_today_peramount 按总量计算的平今手续费系数
              commission_coeff_today_pervol 按手数计算的平今手续费系数

              """
        self.table = {
            'AG': {
                'name': '白银',
                'unit_table': 15,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.06,
                'sell_frozen_coeff': 0.06,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.00005,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00005,
                'commission_coeff_today_pervol': 0
            },
            'AL': {
                'name': '铝',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'AU': {
                'name': '黄金',
                'unit_table': 1000,
                'price_tick': 0.05,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 10.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'BU': {
                'name': '石油沥青',
                'unit_table': 10,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.1,
                'sell_frozen_coeff': 0.1,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0003,
                'commission_coeff_today_pervol': 0
            },
            'CU': {
                'name': '铜',
                'unit_table': 5,
                'price_tick': 10.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.00005,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0,
                'commission_coeff_today_pervol': 0
            },
            'FU': {
                'name': '燃料油',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.1,
                'sell_frozen_coeff': 0.1,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.00005,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0,
                'commission_coeff_today_pervol': 0
            },
            'HC': {
                'name': '热轧卷板',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'NI': {
                'name': '镍',
                'unit_table': 1,
                'price_tick': 10.0,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'PB': {
                'name': '铅',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.00004,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0,
                'commission_coeff_today_pervol': 0
            },
            'RB': {
                'name': '螺纹钢',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.09,
                'sell_frozen_coeff': 0.09,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'RU': {
                'name': '天然橡胶',
                'unit_table': 10,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.09,
                'sell_frozen_coeff': 0.09,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.000045,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.000045,
                'commission_coeff_today_pervol': 0
            },
            'SN': {
                'name': '锡',
                'unit_table': 1,
                'price_tick': 10.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'SP': {
                'name': '漂针浆',
                'unit_table': 10,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.00005,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0,
                'commission_coeff_today_pervol': 0
            },
            'WR': {
                'name': '线材',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.00004,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0,
                'commission_coeff_today_pervol': 0
            },
            'ZN': {
                'name': '锌',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'A': {
                'name': '黄大豆',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 2.0
            },
            'B': {
                'name': '黄大豆',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 1.0
            },
            'BB': {
                'name': '细木工板',
                'unit_table': 500,
                'price_tick': 0.05,
                'buy_frozen_coeff': 0.2,
                'sell_frozen_coeff': 0.2,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00005,
                'commission_coeff_today_pervol': 0
            },
            'C': {
                'name': '黄玉米',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.2,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'CS': {
                'name': '玉米淀粉',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'EG': {
                'name': '乙二醇',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.06,
                'sell_frozen_coeff': 0.06,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 4.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'FB': {
                'name': '中密度纤维板',
                'unit_table': 500,
                'price_tick': 0.05,
                'buy_frozen_coeff': 0.2,
                'sell_frozen_coeff': 0.2,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00005,
                'commission_coeff_today_pervol': 0
            },
            'I': {
                'name': '铁矿石',
                'unit_table': 100,
                'price_tick': 0.5,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.00006,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00006,
                'commission_coeff_today_pervol': 0
            },
            'J': {
                'name': '冶金焦炭',
                'unit_table': 100,
                'price_tick': 0.5,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.00018,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00018,
                'commission_coeff_today_pervol': 0
            },
            'JD': {
                'name': '鲜鸡蛋',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.00015,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00015,
                'commission_coeff_today_pervol': 0
            },
            'JM': {
                'name': '焦煤',
                'unit_table': 60,
                'price_tick': 0.5,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.00018,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00018,
                'commission_coeff_today_pervol': 0
            },
            'L': {
                'name': '线型低密度聚乙烯',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'M': {
                'name': '豆粕',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'P': {
                'name': '棕榈油',
                'unit_table': 10,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'PP': {
                'name': '聚丙烯',
                'unit_table': 5,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.00006,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00003,
                'commission_coeff_today_pervol': 0
            },
            'V': {
                'name': '聚氯乙烯',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'Y': {
                'name': '豆油',
                'unit_table': 10,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'AP': {
                'name': '鲜苹果',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 5.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 5.0
            },
            'CF': {
                'name': '一号棉花',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 4.3,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'CY': {
                'name': '棉纱',
                'unit_table': 5,
                'price_tick': 5.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 4.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'FG': {
                'name': '玻璃',
                'unit_table': 20,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 6.0
            },
            'JR': {
                'name': '粳稻',
                'unit_table': 20,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 3.0
            },
            'LR': {
                'name': '晚籼稻',
                'unit_table': 20,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 3.0
            },
            'MA': {
                'name': '甲醇MA',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 6.0
            },
            'OI': {
                'name': '菜籽油',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'PM': {
                'name': '普通小麦',
                'unit_table': 50,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 5.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 5.0
            },
            'RI': {
                'name': '早籼',
                'unit_table': 20,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 2.5
            },
            'RM': {
                'name': '菜籽粕',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.06,
                'sell_frozen_coeff': 0.06,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 1.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'RS': {
                'name': '油菜籽',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.2,
                'sell_frozen_coeff': 0.2,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 2.0
            },
            'SF': {
                'name': '硅铁',
                'unit_table': 5,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 9.0
            },
            'SM': {
                'name': '锰硅',
                'unit_table': 5,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 6.0
            },
            'SR': {
                'name': '白砂糖',
                'unit_table': 10,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'TA': {
                'name': '精对苯二甲酸',
                'unit_table': 5,
                'price_tick': 2.0,
                'buy_frozen_coeff': 0.06,
                'sell_frozen_coeff': 0.06,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'WH': {
                'name': '优质强筋小麦',
                'unit_table': 20,
                'price_tick': 1.0,
                'buy_frozen_coeff': 0.2,
                'sell_frozen_coeff': 0.2,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 2.5,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'ZC': {
                'name': '动力煤ZC',
                'unit_table': 100,
                'price_tick': 0.2,
                'buy_frozen_coeff': 0.06,
                'sell_frozen_coeff': 0.06,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 4.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 4.0
            },
            'SC': {
                'name': '原油',
                'unit_table': 1000,
                'price_tick': 0.1,
                'buy_frozen_coeff': 0.1,
                'sell_frozen_coeff': 0.1,
                'exchange': EXCHANGE_ID.INE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 20.0,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 0.0
            },
            'EB': {
                'name': '苯乙烯',
                'unit_table': 5,
                'price_tick': 1,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'RR': {
                'name': '粳米',
                'unit_table': 10,
                'price_tick': 1,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.DCE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'NR': {
                'name': '20号胶',
                'unit_table': 10,
                'price_tick': 5,
                'buy_frozen_coeff': 0.09,
                'sell_frozen_coeff': 0.09,
                'exchange': EXCHANGE_ID.INE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0.0
            },
            'SS': {
                'name': '不锈钢',
                'unit_table': 5,
                'price_tick': 5,
                'buy_frozen_coeff': 0.08,
                'sell_frozen_coeff': 0.08,
                'exchange': EXCHANGE_ID.SHFE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0.0
            },
            'CJ': {
                'name': '红枣',
                'unit_table': 5,
                'price_tick': 5,
                'buy_frozen_coeff': 0.07,
                'sell_frozen_coeff': 0.07,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0,
                'commission_coeff_pervol': 3,
                'commission_coeff_today_peramount': 0,
                'commission_coeff_today_pervol': 3
            },
            'UR': {
                'name': '尿素',
                'unit_table': 20,
                'price_tick': 1,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CZCE,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'IC': {
                'name': '中证500指数',
                'unit_table': 200,
                'price_tick': 0.2,
                'buy_frozen_coeff': 0.12,
                'sell_frozen_coeff': 0.12,
                'exchange': EXCHANGE_ID.CFFEX,
                'commission_coeff_peramount': 0.00002301,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00034501,
                'commission_coeff_today_pervol': 0
            },
            'IF': {
                'name': '沪深300指数',
                'unit_table': 300,
                'price_tick': 0.2,
                'buy_frozen_coeff': 0.10,
                'sell_frozen_coeff': 0.10,
                'exchange': EXCHANGE_ID.CFFEX,
                'commission_coeff_peramount': 0.00002301,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'IH': {
                'name': '上证50指数',
                'unit_table': 300,
                'price_tick': 0.2,
                'buy_frozen_coeff': 0.05,
                'sell_frozen_coeff': 0.05,
                'exchange': EXCHANGE_ID.CFFEX,
                'commission_coeff_peramount': 0.00002301,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.00034501,
                'commission_coeff_today_pervol': 0
            },
            'TF': {
                'name': '5年期国债',
                'unit_table': 10000,
                'price_tick': 0.005,
                'buy_frozen_coeff': 0.012,
                'sell_frozen_coeff': 0.012,
                'exchange': EXCHANGE_ID.CFFEX,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
            'TS': {
                'name': '2年期国债',
                'unit_table': 20000,
                'price_tick': 0.005,
                'buy_frozen_coeff': 0.005,
                'sell_frozen_coeff': 0.005,
                'exchange': EXCHANGE_ID.CFFEX,
                'commission_coeff_peramount': 0.0001,
                'commission_coeff_pervol': 0,
                'commission_coeff_today_peramount': 0.0001,
                'commission_coeff_today_pervol': 0
            },
        }

    # 手续费比例

    @property
    @lru_cache()
    def pdtable(self):
        return pd.DataFrame(self.table)

    def __repr__(self):
        return '< QAMARKET_PRESET >'

    @property
    def code_list(self):
        return list(self.table.keys())

    @property
    def exchange_list(self):
        """返回已有的市场列表

        Returns:
            [type] -- [description]
        """

        return list(self.pdtable.loc['exchange'].unique())

    def get_exchangecode(self, exchange):
        return self.pdtable.T.query('exchange=="{}"'.format(exchange)
                                   ).index.tolist()

    def get_code(self, code):
        try:
            int(str(code)[1])
            code = code[0]
        except:
            if str(code).endswith('L8') or str(code).endswith('L9'):
                code = code[0:-2]
            else:
                code = code[0:2]
        return self.table.get(str(code).upper(), {})

    # 合约所属交易所代码

    def get_exchange(self, code):
        return self.get_code(code).get('exchange', None)

    # 合约中文名称
    def get_name(self, code):
        return self.get_code(code).get('name', None)

    # 开仓手续费率
    def get_commission_coeff(self, code):
        """
        当前无法区分是百分比还是按手数收费,不过可以拿到以后自行判断
        """
        return max(
            self.get_code(code).get('commission_coeff_peramount'),
            self.get_code(code).get('commission_coeff_pervol')
        )

    # 平今手续费率
    def get_commission_today_coeff(self, code):
        return max(
            self.get_code(code).get('commission_coeff_today_peramount'),
            self.get_code(code).get('commission_coeff_today_pervol')
        )

    # 印花税系数
    def get_tax_coeff(self, code, dtype):
        pass

    # 交易时间
    def get_trade_time(self, code, dtype):
        pass

    # 每跳毛利/元
    def get_unit(self, code):
        return self.get_code(code).get('unit_table', 1)

    # 每跳价格(价差)
    def get_price_tick(self, code):
        return self.get_code(code).get('price_tick', 0.01)

    # 买卖冻结保证金系数
    def get_frozen(self, code):
        """
        要结合unit_table才能计算出真实的冻结保证金数量
        """
        return self.get_code(code).get('buy_frozen_coeff', 1)
