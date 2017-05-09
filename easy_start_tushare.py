#coding:utf-8

import QUANTAXIS as QA
import pymongo

# 1. 全市场股票日线数据存储
QA.QA_save_stock_day_all()
# 2. 更新数据库,建立索引
QA.QA_update_standard_sql()
# 3. 股票列表存储
QA.QA_SU_save_stock_list('ts',pymongo.MongoClient())
# 4. 交易日期存储
QA.QA_SU_save_trade_date_all()
# 5. 股票基本面信息存储
QA.QA_SU_save_stock_info('ts',pymongo.MongoClient())


#仅仅是为了初始化才在这里插入用户,如果想要注册用户,要到webkit底下注册
pymongo.MongoClient().quantaxis.user_list.insert({'username':'admin','password':'admin'})


