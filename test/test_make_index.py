

import pymongo
collection=pymongo.MongoClient().quantaxis.stock_day
collection.ensure_index('code')
