```python
        coll.update({"Code":codes} , { "$set" : {"lasttrade_date": data.Data[0][0][0]}});
        coll.update({"Code":codes} , { "$set" : {"lastdelivery_date":data.Data[1][0][0]}});
        coll.update({"Code":codes} , { "$set" : {"dlmonth":data.Data[2][0][0]}});
        coll.update({"Code":codes} , { "$set" : {"lprice":data.Data[3][0][0]}});
        coll.update({"Code":codes} , { "$set" : {"sccode":data.Data[4][0][0]}});
        coll.update({"Code":codes} , { "$set": {"changelt":data.Data[6][0][0]}});
        coll.update({"Code":codes} , { "$set" : {"punit":data.Data[7][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"mfprice":data.Data[8][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"contractmultiplier":data.Data[9][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"cdmonths":data.Data[10][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"thours":data.Data[11][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"ltdated":data.Data[12][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"ftmargins":data.Data[13][0][0]}}); 
        coll.update({"Code":codes} , { "$set" : {"trade_hiscode":data.Data[14][0][0]}}); 
```