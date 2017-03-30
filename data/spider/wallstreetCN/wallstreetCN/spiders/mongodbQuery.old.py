import pymongo
import datetime


def get_db(dbname):
    # 建立连接
    client = pymongo.MongoClient(host="127.0.0.1", port=27017)
    db = client[dbname]
    print 'connent to pymongo'
    #或者 db = client.example
    return db


def get_collection(dbcoll):
    # 选择集合（mongo中collection和database都是延时创建的）
    coll = db[dbcoll]
    print db.collection_names()
    return coll


def insert_one_doc(db):
     #插入一个document
    coll = db['title']
    information = {"name": "quyang", "age": "25"}
    information_id = coll.insert(information)
    print information_id


#def insert_multi_docs(db):
    # 批量插入documents,插入一个数组
    #coll = db['informations']
    #information = [{"name": "xiaoming", "age": "25"}, {"name": "xiaoqiang", "age": "24"}]
    #information_id = coll.insert(information)
    #print information_id


def get_one_doc(db):
    # 有就返回一个，没有就返回None
    coll = db['informations']
    print coll.find_one()  # 返回第一条记录



def get_one_by_id(db):
    # 通过objectid来查找一个doc
    coll = db['informations']
    obj = coll.find_one()
    obj_id = obj["_id"]
    print "_id 为ObjectId类型，obj_id:" + str(obj_id)

    print coll.find_one({"_id": obj_id})
    # 需要注意这里的obj_id是一个对象，不是一个str，使用str类型作为_id的值无法找到记录
    print "_id 为str类型 "
    print coll.find_one({"_id": str(obj_id)})
    # 可以通过ObjectId方法把str转成ObjectId类型
    from bson.objectid import ObjectId

    print "_id 转换成ObjectId类型"
    print coll.find_one({"_id": ObjectId(str(obj_id))})


def get_many_docs(db):
    # mongo中提供了过滤查找的方法，可以通过各种条件筛选来获取数据集，还可以对数据进行计数，排序等处理
    coll = db['informations']
    #ASCENDING = 1 升序;DESCENDING = -1降序;default is ASCENDING
    for item in coll.find().sort("age", pymongo.DESCENDING):
        print item

    count = coll.count()
    print "集合中所有数据 %s个" % int(count)

    #条件查询
    count = coll.find({"name":"quyang"}).count()
    print "quyang: %s"%count

def clear_all_datas(db):
    #清空一个集合中的所有数据
    db["informations"].remove()

if __name__ == '__main__':
    db = get_db()
    my_collection = get_collection(db)
    post = {"author": "Mike", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    # 插入记录
    my_collection.insert(post)
    insert_one_doc(db)
    # 条件查询
    print my_collection.find_one({"x": "10"})
    # 查询表中所有的数据
    for iii in my_collection.find():
        print iii
    print my_collection.count()
    my_collection.update({"author": "Mike"},
                         {"author": "quyang", "text": "My first blog post!", "tags": ["mongodb", "python", "pymongo"],
                          "date": datetime.datetime.utcnow()})
    for jjj in my_collection.find():
        print jjj
    get_one_doc(db)
    get_one_by_id(db)
    get_many_docs(db)
    # clear_all_datas(db)