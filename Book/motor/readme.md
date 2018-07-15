# motor 


## Motor Tornado API
```
MotorClient – Connection to MongoDB

MotorClientSession – Sequence of operations

MotorDatabase

MotorCollection

MotorChangeStream

MotorCursor

MotorCommandCursor

Motor GridFS Classes

motor.web - Integrate Motor with the Tornado web framework
```
## Motor asyncio API
```
AsyncIOMotorClient – Connection to MongoDB

AsyncIOMotorClientSession – Sequence of operations

AsyncIOMotorDatabase

AsyncIOMotorCollection

AsyncIOMotorChangeStream

AsyncIOMotorCursor

AsyncIOMotorCommandCursor

asyncio GridFS Classes

motor.aiohttp - Integrate Motor with the aiohttp web framework

```
很早就知道motor这个项目, 但是一直没有认真去读, 偶尔发现motor已经升级到2.0了, 仔细看了下他的api 太牛逼了, 于是准备翻译一下:


motor分了两块, 主要是底层和平台兼容性的区别(感觉还是历史遗留问题)

- tornado_base  MotorClient 

- asyncio_base  AsyncIOMotorClient


因为asyncio是python3.4才引入的项目, 而motor在此之前就开始了, 于是最开始用的是基于tornado的异步底层 MotorClient, 而如今 asyncio
越来越完善, 逐步的引入了AsyncioMotorClient的概念和内容.(区别是: tornado对windows的支持不是很完善,而asyncio较为完善, 因此motor官方推荐使用asyncio的client)


参考文献 : [Motor Not Support](http://motor.readthedocs.io/en/stable/requirements.html#not-supported)



##