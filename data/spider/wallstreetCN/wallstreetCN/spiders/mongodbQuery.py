import pymongo
import json


class querylist(object):
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db = client['wsc']
    
    def queryMongodbSame(self,collname,keyname,keycontent):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['wsc']
        coll = db[collname]
        count = coll.find({keyname:keycontent}).count()
        return count
    def checkDifferentDatabase(self,col1,col2,keyname1,keyname2,x):
        client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        db = client['wsc']
        coll1 = db[col1]
        coll2 = db[col2]
        countnum=0
        for url in coll1.find():
            urlx=url[keyname1]
            print (col2)
            print (keyname1)
            print (urlx)
            count = self.queryMongodbSame(col2,keyname2,urlx)
            print (count)
            if count == x:
                print ('none in the db2')
                print (countnum)
            else:
                print ('already in')
                continue
                countnum+=1
                print (countnum)
        print (countnum)
    



        
        