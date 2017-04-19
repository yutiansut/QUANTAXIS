

import pymongo

#collection=pymongo.MongoClient().quantaxis.stock_day
#collection.ensure_index('code')
collection=pymongo.MongoClient().quantaxis.backtest_history
collection.ensure_index('cookie')