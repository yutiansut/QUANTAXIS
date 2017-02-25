R利剑NoSQL系列文章 之 MongoDB
R利剑NoSQL系列文章，主要介绍通过R语言连接使用nosql数据库。涉及的NoSQL产品，包括Redis,MongoDB, HBase, Hive, Cassandra, Neo4j。希望通过我的介绍让广大的R语言爱好者，有更多的开发选择，做出更多地激动人心的应用。

关于作者：

张丹(Conan), 程序员Java,R,PHP,Javascript
weibo：@Conan_Z
blog: http://blog.fens.me
email: bsspirit@gmail.com
由于文章篇幅有限，均跳过NoSQL的安装过程，请自行参考文档安装。

转载请注明：
http://blog.fens.me/nosql-r-mongodb/

r-nosql-mongodb

第一篇 R利剑MongeDB，分为4个章节。

MongoDB环境准备
rmongodb函数库
rmongodb基本使用操作
rmongodb测试案例
每一章节，都会分为”文字说明部分”和”代码部分”，保持文字说明与代码的连贯性。

1. MongoDB环境准备

文字说明部分：

首先环境准备，这里我选择了Linux Ubuntu操作系统12.04的32位桌面版本，大家可以根据自己的使用习惯选择顺手的Linux。

MongoDB安装过程跳过。

查看MongoDB服务器环境
使用mongod命令，启动MongoDB。

进程号：pid=2924 
端口：port=27017 
数据文件目录：dbpath=/data/db/ 
软件版本：32-bit 
主机名：host=conan
使用mongo命令，打开mongo shell。

mongo shell的简单操作：
查看数据库，切换数据库，查看数据集.

R语言环境2.15.0，WinXP通过远程连接，访问Mongodb Server。

代码部分：

查看操作系统

~ uname -a

    Linux conan 3.2.0-38-generic-pae #61-Ubuntu SMP Tue Feb 19 12:39:51 UTC 2013 i686 i686 i386 GNU/Linux

~ cat /etc/issue

    Ubuntu 12.04.2 LTS \n \l
启动mongodb

~ mongod

    mongod --help for help and startup options
    Thu Apr 11 11:02:26
    Thu Apr 11 11:02:26 warning: 32-bit servers don't have journaling enabled by default. Please use --journal if you want durability.
    Thu Apr 11 11:02:26
    Thu Apr 11 11:02:26 [initandlisten] MongoDB starting : pid=2924 port=27017 dbpath=/data/db/ 32-bit host=conan
    Thu Apr 11 11:02:26 [initandlisten]
    Thu Apr 11 11:02:26 [initandlisten] ** NOTE: when using MongoDB 32 bit, you are limited to about 2 gigabytes of data
    Thu Apr 11 11:02:26 [initandlisten] **       see http://blog.mongodb.org/post/137788967/32-bit-limitations
    Thu Apr 11 11:02:26 [initandlisten] **       with --journal, the limit is lower
    Thu Apr 11 11:02:26 [initandlisten]
    Thu Apr 11 11:02:26 [initandlisten] db version v2.0.6, pdfile version 4.5
    Thu Apr 11 11:02:26 [initandlisten] git version: e1c0cbc25863f6356aa4e31375add7bb49fb05bc
    Thu Apr 11 11:02:26 [initandlisten] build info: Linux domU-12-31-39-01-70-B4 2.6.21.7-2.fc8xen #1 SMP Fri Feb 15 12:39:36 EST 2008 i686 BOOST_LIB_VERSION=1_41
    Thu Apr 11 11:02:26 [initandlisten] options: {}
    Thu Apr 11 11:02:26 [websvr] admin web console waiting for connections on port 28017
    Thu Apr 11 11:02:26 [initandlisten] waiting for connections on port 27017
打开mongo shell

~ mongo

    MongoDB shell version: 2.0.6
    connecting to: test
进入mongo shell, 列表显示数据库

> show dbs

    db      0.0625GB
    feed    0.0625GB
    foobar  0.0625GB
    local   (empty)
切换数据库

> use foobar

   switched to db foobar
列表显示数据集

> show collections

    blog
    system.indexes
R语言开发环境2.15.0，WinXP

~ R
R version 2.15.0 (2012-03-30)
Copyright (C) 2012 The R Foundation for Statistical Computing
ISBN 3-900051-07-0
Platform: i386-pc-mingw32/i386 (32-bit)
2. rmongodb函数库

文字说明部分：

rmongodb的开发了一大堆的函数，对应mongo的操作。比起别的NoSQL来说，真是工程浩大啊。但我总觉得封装粒度不够，写起代码来比较复杂。

下面列出了所有rmongodb函数库，我只挑选几个常用的介绍。

建立mongo连接

mongo<-mongo.create()
查看接连是否正常

mongo.is.connected(mongo)
创建一个BSON对象缓存

buf <- mongo.bson.buffer.create()
给对象buf增加element

mongo.bson.buffer.append(buf, "name", "Echo")
增加对象类型的element

score <- c(5, 3.5, 4)
names(score) <- c("Mike", "Jimmy", "Ann")
mongo.bson.buffer.append(buf, "score", score)
增加数组类型的element

mongo.bson.buffer.start.array(buf, "comments")
mongo.bson.buffer.append(buf, "0", "a1")
mongo.bson.buffer.append(buf, "1", "a2")
mongo.bson.buffer.append(buf, "2", "a3")
关闭数组类型的element

mongo.bson.buffer.finish.object(buf)
取出缓存数据

b <- mongo.bson.from.buffer(buf)
数据库.数据集

ns="db.blog"
插入一条记录

mongo.insert(mongo,ns,b)

#mongo shell:(Not Run)
db.blog.insert(b)
创建查询对象query

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.append(buf, "name", "Echo")
query <- mongo.bson.from.buffer(buf)
创建查询返回值对象

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.append(buf, "name", 1)
fields <- mongo.bson.from.buffer(buf)
执行单条记录查询

mongo.find.one(mongo, ns, query, fields)

#mongo shell:(Not Run)
db.blog.findOne({query},{fields})
执行列表记录查询

mongo.find(mongo, ns, query, fields)

#mongo shell:(Not Run)
db.blog.find({query},{fields})
创建修改器对象objNew

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.start.object(buf, "$inc")
mongo.bson.buffer.append(buf, "age", 1L)
mongo.bson.buffer.finish.object(buf)
objNew <- mongo.bson.from.buffer(buf)
执行修改操作

mongo.update(mongo, ns, query, objNew)

#mongo shell:(Not Run)
db.blog.update({query},{objNew})
单行代码修改操作

mongo.update(mongo, ns, query, list(name="Echo", age=25))

#mongo shell:(Not Run)
db.blog.update({query},{objNew})
删除所选对象

mongo.remove(mongo, ns, query)

#mongo shell:(Not Run)
db.blog.remove({query},{objNew})
销毁mongo连接

mongo.destroy(mongo)
代码部分：

共有153个函数

mongo.add.user
mongo.authenticate
mongo.binary.binary
mongo.binary.function
mongo.binary.md5
mongo.binary.old
mongo.binary.user
mongo.binary.uuid
mongo.bson.array
mongo.bson.binary
mongo.bson.bool
mongo.bson.buffer.append
mongo.bson.buffer.append.bool
mongo.bson.buffer.append.bson
mongo.bson.buffer.append.code
mongo.bson.buffer.append.code.w.scope
mongo.bson.buffer.append.complex
mongo.bson.buffer.append.double
mongo.bson.buffer.append.element
mongo.bson.buffer.append.int
mongo.bson.buffer.append.list
mongo.bson.buffer.append.long
mongo.bson.buffer.append.null
mongo.bson.buffer.append.object
mongo.bson.buffer.append.oid
mongo.bson.buffer.append.raw
mongo.bson.buffer.append.regex
mongo.bson.buffer.append.string
mongo.bson.buffer.append.symbol
mongo.bson.buffer.append.time
mongo.bson.buffer.append.timestamp
mongo.bson.buffer.append.undefined
mongo.bson.buffer.create
mongo.bson.buffer.finish.object
mongo.bson.buffer.size
mongo.bson.buffer.start.array
mongo.bson.buffer.start.object
mongo.bson.code
mongo.bson.code.w.scope
mongo.bson.date
mongo.bson.dbref
mongo.bson.destroy
mongo.bson.double
mongo.bson.empty
mongo.bson.eoo
mongo.bson.find
mongo.bson.from.buffer
mongo.bson.from.list
mongo.bson.int
mongo.bson.iterator.create
mongo.bson.iterator.key
mongo.bson.iterator.next
mongo.bson.iterator.type
mongo.bson.iterator.value
mongo.bson.long
mongo.bson.null
mongo.bson.object
mongo.bson.oid
mongo.bson.print
mongo.bson.regex
mongo.bson.size
mongo.bson.string
mongo.bson.symbol
mongo.bson.timestamp
mongo.bson.to.list
mongo.bson.undefined
mongo.bson.value
mongo.code.create
mongo.code.w.scope.create
mongo.command
mongo.count
mongo.create
mongo.cursor.destroy
mongo.cursor.next
mongo.cursor.value
mongo.destroy
mongo.disconnect
mongo.distinct
mongo.drop
mongo.drop.database
mongo.find
mongo.find.await.data
mongo.find.cursor.tailable
mongo.find.exhaust
mongo.find.no.cursor.timeout
mongo.find.one
mongo.find.oplog.replay
mongo.find.partial.results
mongo.find.slave.ok
mongo.get.database.collections
mongo.get.databases
mongo.get.err
mongo.get.hosts
mongo.get.last.err
mongo.get.prev.err
mongo.get.primary
mongo.get.server.err
mongo.get.server.err.string
mongo.get.socket
mongo.get.timeout
mongo.gridfile.destroy
mongo.gridfile.get.chunk
mongo.gridfile.get.chunk.count
mongo.gridfile.get.chunks
mongo.gridfile.get.chunk.size
mongo.gridfile.get.content.type
mongo.gridfile.get.descriptor
mongo.gridfile.get.filename
mongo.gridfile.get.length
mongo.gridfile.get.md5
mongo.gridfile.get.metadata
mongo.gridfile.get.upload.date
mongo.gridfile.pipe
mongo.gridfile.read
mongo.gridfile.seek
mongo.gridfile.writer.create
mongo.gridfile.writer.finish
mongo.gridfile.writer.write
mongo.gridfs.create
mongo.gridfs.destroy
mongo.gridfs.find
mongo.gridfs.remove.file
mongo.gridfs.store
mongo.gridfs.store.file
mongo.index.background
mongo.index.create
mongo.index.drop.dups
mongo.index.sparse
mongo.index.unique
mongo.insert
mongo.insert.batch
mongo.is.connected
mongo.is.master
mongo.oid.create
mongo.oid.from.string
mongo.oid.print
mongo.oid.time
mongo.oid.to.string
mongo.reconnect
mongo.regex.create
mongo.remove
mongo.rename
mongo.reset.err
mongo.set.timeout
mongo.shorthand
mongo.simple.command
mongo.symbol.create
mongo.timestamp.create
mongo.undefined.create
mongo.update
mongo.update.basic
mongo.update.multi
mongo.update.upsert
3. rmongodb基本使用操作

文字说明部分：

首先，要安装rmongodb类库，加载类库。

然后，通过mongo.create()函数，建立与MongoDB Server的连接。如果是本地连接，mongo.create()不要参数，下面例子使用远程连接，增加host参数配置IP地址。mongo<-mongo.create(host=“192.168.1.11”)

检查是否连接正常，mongo.is.connected()。这条语句在开发时会经常使用到。在用R语言建模时，如果对象或者函数使用错误，连接会被自动断开。由于MongoDB的异常机制，断开时不会是提示。大家要手动使用这条命令测试，连接是否正常。

接下来，定义两个变量，db和ns。db是我们需要使用的数据库，ns是数据库+数据集。

下面我们创建一个Mongo对象。

{
        "_id" : ObjectId("51663e14da2c51b1e8bc62eb"),
        "name" : "Echo",
        "age" : 22,
        "gender" : "Male",
        "score" : {
                "Mike" : 5,
                "Jimmy" : 3.5,
                "Ann" : 4
        },
        "comments" : [
                "a1",
                "a2",
                "a3"
        ]
}
然后，分别使用修改器$inc,$set,$push进行操作。

最后删除对象，并断开连接。

代码部分：

安装rmongodb

install.packages(rmongodb)
加载类库

library(rmongodb)
远程连接mongodb server

mongo<-mongo.create(host="192.168.1.11")
查看是否连接正常

print(mongo.is.connected(mongo))
定义db

db<-"foobar"
定义db.collection

ns<-"foobar.blog"
组织bson类型数据

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.append(buf, "name", "Echo")
mongo.bson.buffer.append(buf, "age", 22L)
mongo.bson.buffer.append(buf, "gender", 'Male')

#对象类型
score <- c(5, 3.5, 4)
names(score) <- c("Mike", "Jimmy", "Ann")
mongo.bson.buffer.append(buf, "score", score)

#数组类型
mongo.bson.buffer.start.array(buf, "comments")
mongo.bson.buffer.append(buf, "0", "a1")
mongo.bson.buffer.append(buf, "1", "a2")
mongo.bson.buffer.append(buf, "2", "a3")
mongo.bson.buffer.finish.object(buf)
b <- mongo.bson.from.buffer(buf)
插入mongodb

mongo.insert(mongo,ns,b)
单条显示插入的数据

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.append(buf, "name", "Echo")
query <- mongo.bson.from.buffer(buf)
print(mongo.find.one(mongo, ns, query))
使用$inc修改器，修改给age加1

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.start.object(buf, "$inc")
mongo.bson.buffer.append(buf, "age", 1L)
mongo.bson.buffer.finish.object(buf)
objNew <- mongo.bson.from.buffer(buf)
mongo.update(mongo, ns, query, objNew)
print(mongo.find.one(mongo, ns, query))
使用$set修改器，修改age=1

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.start.object(buf, "$set")
mongo.bson.buffer.append(buf, "age", 1L)
mongo.bson.buffer.finish.object(buf)
objNew <- mongo.bson.from.buffer(buf)
mongo.update(mongo, ns, query, objNew)
print(mongo.find.one(mongo, ns, query))
使用$push修改器，给comments数组追加”Orange”数据

buf <- mongo.bson.buffer.create()
mongo.bson.buffer.start.object(buf, "$push")
mongo.bson.buffer.append(buf, "comments", "Orange")
mongo.bson.buffer.finish.object(buf)
objNew <- mongo.bson.from.buffer(buf)
mongo.update(mongo, ns, query, objNew)
print(mongo.find.one(mongo, ns, query))
使用简化修改语句，给对象重新赋值

mongo.update(mongo, ns, query, list(name="Echo", age=25))
print(mongo.find.one(mongo, ns, query))
删除对象

mongo.remove(mongo, ns, query)
销毁mongo连接

mongo.destroy(mongo)
4. rmongodb测试案例

文字说明部分：

批量插入数据，使用修改器批量修改数据

3种修改器速度比较,$push最慢
$push > $set > $inc

终于push是对数组操作，set是对任意值操作，inc是对数字操作，所以下面测试可能不太公平。测试结果仅供参考。

代码部分：

批量插入数据函数

  batch_insert<-function(arr=1:10,ns){
    library(stringr)
    mongo_insert<-function(x){
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.append(buf, "name", str_c("Dave",x))
      mongo.bson.buffer.append(buf, "age", x)
      mongo.bson.buffer.start.array(buf, "comments")
      mongo.bson.buffer.append(buf, "0", "a1")
      mongo.bson.buffer.append(buf, "1", "a2")
      mongo.bson.buffer.append(buf, "2", "a3")
      mongo.bson.buffer.finish.object(buf)
      return(mongo.bson.from.buffer(buf))
    }
    mongo.insert.batch(mongo, ns, lapply(arr,mongo_insert))
  }
批量修改，$inc修改器函数

  batch_inc<-function(data,ns){
    for(i in data){
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.append(buf, "name", str_c("Dave",i))
      criteria <- mongo.bson.from.buffer(buf)
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.start.object(buf, "$inc")
      mongo.bson.buffer.append(buf, "age", 1L)
      mongo.bson.buffer.finish.object(buf)
      objNew <- mongo.bson.from.buffer(buf)
      mongo.update(mongo, ns, criteria, objNew)
    }
  }
批量修改，$set修改器函数

  batch_set<-function(data,ns){
    for(i in data){
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.append(buf, "name", str_c("Dave",i))
      criteria <- mongo.bson.from.buffer(buf)
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.start.object(buf, "$set")
      mongo.bson.buffer.append(buf, "age", 1L)
      mongo.bson.buffer.finish.object(buf)
      objNew <- mongo.bson.from.buffer(buf)
      mongo.update(mongo, ns, criteria, objNew)
    }
  }
批量修改，$push修改器函数

  batch_push<-function(data,ns){
    for(i in data){
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.append(buf, "name", str_c("Dave",i))
      criteria <- mongo.bson.from.buffer(buf)
      buf <- mongo.bson.buffer.create()
      mongo.bson.buffer.start.object(buf, "$push")
      mongo.bson.buffer.append(buf, "comments", "Orange")
      mongo.bson.buffer.finish.object(buf)
      objNew <- mongo.bson.from.buffer(buf)
      mongo.update(mongo, ns, criteria, objNew)
    }
  }
执行程序，3种修改速度比较,$push最慢

  ns="foobar.blog"
  data=1:1000

  mongo.remove(mongo, ns)
  ## [1] TRUE

  system.time(batch_insert(data, ns))
  ##    user  system elapsed 
  ##    0.25    0.00    0.28 

  system.time(batch_inc(data, ns))
  ##    user  system elapsed 
  ##    0.47    0.27    2.50 

  system.time(batch_set(data, ns))
  ##    user  system elapsed 
  ##    0.77    0.48    3.17 

  system.time(batch_push(data, ns))
  ##    user  system elapsed 
  ##    0.81    0.41    4.23