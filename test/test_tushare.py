import json
import pymongo
import tushare as ts
dfs = ts.get_stock_basics()

for i in df.index:  
    print(i)
    data=ts.get_hist_data(i)
    try:
        data_json=json.loads(data.to_json(orient='records'))
        coll=pymongo.MongoClient().quantaxis.stock_day
        coll.insert_many(data_json)
    except:
        print('none data')