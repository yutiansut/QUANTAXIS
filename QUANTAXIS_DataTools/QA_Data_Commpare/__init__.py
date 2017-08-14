# coding:utf-8


"""
用于比对和清洗数据
尤其是当前复权数据等不一致的时候

"""

import QUANTAXIS as QA
import random

stock_list=QA.QA_fetch_stock_list()


for i in range(10):
    ran_id=random.randint(0,len(stock_list))

    ran_id_for_start=random.randint(0,len(QA.trade_date_sse))




    for item in ['ts','ths']:
        print('===================='+item+'======================')
        print(stock_list[ran_id])
        print(QA.trade_date_sse[ran_id_for_start])


        data_x=QA.QA_fetch_get_stock_day(item,stock_list[ran_id],QA.trade_date_sse[ran_id_for_start],QA.trade_date_sse[ran_id_for_start+10],'00')


        print(data_x)
