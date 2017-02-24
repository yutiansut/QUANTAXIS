```python
        coll.update({"Code":codes} , { "$push" : {"lasttrade_date": data.Data[0][0][0]}});
        coll.update({"Code":codes} , { "$push" : {"lastdelivery_date":data.Data[1][0][0]}});
        coll.update({"Code":codes} , { "$push" : {"dlmonth":data.Data[2][0][0]}});
        coll.update({"Code":codes} , { "$push" : {"lprice":data.Data[3][0][0]}});
        coll.update({"Code":codes} , { "$push" : {"sccode":data.Data[4][0][0]}});
        coll.update({"Code":codes} , { "$push": {"changelt":data.Data[6][0][0]}});
        coll.update({"Code":codes} , { "$push" : {"punit":data.Data[7][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"mfprice":data.Data[8][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"contractmultiplier":data.Data[9][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"cdmonths":data.Data[10][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"thours":data.Data[11][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"ltdated":data.Data[12][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"ftmargins":data.Data[13][0][0]}}); 
        coll.update({"Code":codes} , { "$push" : {"trade_hiscode":data.Data[14][0][0]}}); 
```