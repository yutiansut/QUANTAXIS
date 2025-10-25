# QAResourceManager - QUANTAXIS统一资源管理器

**版本**: QUANTAXIS 2.1.0+
**作者**: @yutiansut @quantaxis
**日期**: 2025

---

## 📋 概述

QAResourceManager是QUANTAXIS 2.1.0新增的统一资源管理器，提供对MongoDB、RabbitMQ、ClickHouse、Redis等外部资源的统一管理和优雅关闭机制。

### 核心特性

✅ **连接池管理** - 自动复用连接，减少开销
✅ **上下文管理器** - 支持`with`语句，自动释放资源
✅ **优雅关闭** - 确保资源正确释放，无泄漏
✅ **自动重连** - 连接断开时自动重试
✅ **健康检查** - 定期检查连接状态
✅ **线程安全** - 支持多线程环境
✅ **单例模式** - 全局资源池管理
✅ **atexit清理** - 程序退出时自动关闭资源

---

## 🚀 快速开始

### 安装依赖

```bash
# 基础依赖 (MongoDB)
pip install pymongo motor

# RabbitMQ
pip install pika

# ClickHouse
pip install clickhouse-driver

# Redis
pip install redis

# 完整安装
pip install quantaxis[full]
```

### 最简示例

```python
from QUANTAXIS.QAUtil.QAResourceManager import QAMongoResourceManager

# 使用with语句(推荐)
with QAMongoResourceManager() as mongo:
    db = mongo.get_database('quantaxis')
    result = db.stock_day.find_one({'code': '000001'})
    print(result)
# 自动关闭连接,无需手动close()
```

---

## 📚 详细文档

### 1. MongoDB资源管理器

#### 1.1 基本用法

```python
from QUANTAXIS.QAUtil.QAResourceManager import QAMongoResourceManager

# 方法1: 上下文管理器(推荐)
with QAMongoResourceManager() as mongo:
    db = mongo.get_database('quantaxis')
    # 操作数据库...

# 方法2: 手动管理
mongo = QAMongoResourceManager()
try:
    mongo.connect()
    db = mongo.get_database('quantaxis')
    # 操作数据库...
finally:
    mongo.close()  # 确保关闭
```

#### 1.2 配置参数

```python
mongo = QAMongoResourceManager(
    uri='mongodb://user:pass@localhost:27017',  # 连接URI
    max_pool_size=100,                          # 连接池大小
    server_selection_timeout_ms=5000,           # 服务器选择超时(毫秒)
    async_mode=False                            # 是否使用异步客户端
)
```

#### 1.3 异步模式

```python
import asyncio

async def async_query():
    async with QAMongoResourceManager(async_mode=True) as mongo:
        db = mongo.get_database('quantaxis')
        result = await db.stock_day.find_one({'code': '000001'})
        return result

# 运行异步函数
asyncio.run(async_query())
```

#### 1.4 连接池配置

QAMongoResourceManager默认配置:
- **maxPoolSize**: 100 (最大连接数)
- **minPoolSize**: 10 (最小连接数)
- **maxIdleTimeMS**: 60000 (60秒, 连接最大空闲时间)
- **waitQueueTimeoutMS**: 5000 (5秒, 等待连接池超时)

### 2. RabbitMQ资源管理器

#### 2.1 基本用法

```python
from QUANTAXIS.QAUtil.QAResourceManager import QARabbitMQResourceManager

with QARabbitMQResourceManager() as rabbitmq:
    channel = rabbitmq.get_channel()

    # 声明队列
    channel.queue_declare(queue='test_queue', durable=True)

    # 发布消息
    channel.basic_publish(
        exchange='',
        routing_key='test_queue',
        body='Hello QUANTAXIS'
    )

    # 消费消息
    method_frame, header_frame, body = channel.basic_get(queue='test_queue')
    if method_frame:
        print(f"收到消息: {body.decode()}")
        channel.basic_ack(method_frame.delivery_tag)
# 自动关闭连接和通道
```

#### 2.2 配置参数

```python
rabbitmq = QARabbitMQResourceManager(
    host='localhost',      # RabbitMQ主机
    port=5672,             # 端口
    username='admin',      # 用户名
    password='admin',      # 密码
    vhost='/',             # 虚拟主机
    heartbeat=600,         # 心跳间隔(秒), 0表示禁用
    socket_timeout=5       # Socket超时(秒)
)
```

#### 2.3 安全特性

- **密码擦除**: 认证后自动清除内存中的密码 (`erase_on_connect=True`)
- **心跳保持**: 默认600秒心跳，防止连接超时
- **优雅关闭**: 先关闭通道，再关闭连接

### 3. ClickHouse资源管理器

#### 3.1 基本用法

```python
from QUANTAXIS.QAUtil.QAResourceManager import QAClickHouseResourceManager

with QAClickHouseResourceManager() as clickhouse:
    # 执行SQL
    result = clickhouse.execute("SELECT version()")
    print(f"ClickHouse版本: {result[0][0]}")

    # 查询并返回DataFrame
    df = clickhouse.query_dataframe("""
        SELECT * FROM stock_day
        WHERE code = '000001'
        LIMIT 10
    """)
    print(df.head())
```

#### 3.2 配置参数

```python
clickhouse = QAClickHouseResourceManager(
    host='localhost',           # ClickHouse主机
    port=9000,                  # Native protocol端口
    database='quantaxis',       # 数据库名
    user='default',             # 用户名
    password='',                # 密码
    compression=True,           # 启用压缩
    insert_block_size=100000000 # 插入块大小
)
```

#### 3.3 性能优化配置

```python
# 内置性能优化设置:
settings = {
    'insert_block_size': 100000000,  # 大批量插入
    'max_threads': 4,                # 最大查询线程数
    'max_block_size': 65536,         # 最大块大小
}
```

### 4. Redis资源管理器

#### 4.1 基本用法

```python
from QUANTAXIS.QAUtil.QAResourceManager import QARedisResourceManager

with QARedisResourceManager() as redis_mgr:
    # 设置键值(60秒过期)
    redis_mgr.set('test_key', 'test_value', ex=60)

    # 获取值
    value = redis_mgr.get('test_key')
    print(f"值: {value}")

    # 删除键
    redis_mgr.delete('test_key')
```

#### 4.2 配置参数

```python
redis_mgr = QARedisResourceManager(
    host='localhost',           # Redis主机
    port=6379,                  # 端口
    db=0,                       # 数据库编号
    password=None,              # 密码(可选)
    max_connections=50,         # 连接池最大连接数
    socket_timeout=5,           # Socket超时(秒)
    socket_keepalive=True,      # 启用TCP keepalive
    decode_responses=True       # 解码响应为字符串
)
```

#### 4.3 管道操作

```python
with QARedisResourceManager() as redis_mgr:
    # 创建管道
    pipe = redis_mgr.pipeline(transaction=True)

    # 批量操作
    pipe.set('key1', 'value1')
    pipe.set('key2', 'value2')
    pipe.set('key3', 'value3')

    # 执行
    results = pipe.execute()
    print(f"管道操作结果: {results}")
```

#### 4.4 健康检查

```python
# Redis内置健康检查,每30秒自动检查连接
# health_check_interval=30
```

### 5. 统一资源池管理器

#### 5.1 基本用法(推荐)

```python
from QUANTAXIS.QAUtil.QAResourceManager import QAResourcePool

# 获取单例实例
pool = QAResourcePool.get_instance()

# 获取各类资源
mongo = pool.get_mongo()
rabbitmq = pool.get_rabbitmq()
clickhouse = pool.get_clickhouse()
redis = pool.get_redis()

# 使用资源...
db = mongo.get_database('quantaxis')
channel = rabbitmq.get_channel()

# 健康检查
health = pool.health_check()
print(health)  # {'mongo': True, 'rabbitmq': True, ...}

# 关闭所有资源
pool.close_all()
```

#### 5.2 单例模式

QAResourcePool采用单例模式，全局唯一：

```python
pool1 = QAResourcePool.get_instance()
pool2 = QAResourcePool.get_instance()

assert pool1 is pool2  # True, 同一实例
```

#### 5.3 自动清理

```python
import atexit

# QAResourcePool在初始化时自动注册atexit清理函数
# 程序退出时自动调用pool.close_all()
# 无需手动清理
```

#### 5.4 单独关闭资源

```python
pool = QAResourcePool.get_instance()

# 关闭单个资源
pool.close_resource('mongo')
pool.close_resource('rabbitmq')
pool.close_resource('clickhouse')
pool.close_resource('redis')

# 或关闭所有资源
pool.close_all()
```

### 6. 便捷函数

#### 6.1 快捷上下文管理器

```python
from QUANTAXIS.QAUtil.QAResourceManager import (
    get_mongo_resource,
    get_rabbitmq_resource,
    get_clickhouse_resource,
    get_redis_resource
)

# MongoDB
with get_mongo_resource() as mongo:
    db = mongo.get_database('quantaxis')
    # ...

# RabbitMQ
with get_rabbitmq_resource() as rabbitmq:
    channel = rabbitmq.get_channel()
    # ...

# ClickHouse
with get_clickhouse_resource() as clickhouse:
    df = clickhouse.query_dataframe("SELECT * FROM stock_day LIMIT 10")
    # ...

# Redis
with get_redis_resource() as redis_mgr:
    redis_mgr.set('key', 'value')
    # ...
```

---

## 🔧 高级用法

### 1. 自定义连接配置

#### MongoDB自定义URI

```python
# 从环境变量获取
import os
mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')

with QAMongoResourceManager(uri=mongo_uri) as mongo:
    db = mongo.get_database('quantaxis')
```

#### RabbitMQ认证

```python
with QARabbitMQResourceManager(
    host='rabbitmq.example.com',
    username='quantaxis_user',
    password='secure_password',
    vhost='/quantaxis'
) as rabbitmq:
    channel = rabbitmq.get_channel()
```

### 2. 连接重试

所有资源管理器均支持`reconnect()`方法：

```python
mongo = QAMongoResourceManager()

try:
    mongo.connect()
    # 使用连接...
except Exception as e:
    # 连接失败,重试
    mongo.reconnect()
```

### 3. 健康检查

```python
pool = QAResourcePool.get_instance()

# 定期健康检查
import time
while True:
    health = pool.health_check()
    for resource, status in health.items():
        if not status:
            print(f"❌ {resource}连接异常,正在重连...")
            # 自动重连逻辑...

    time.sleep(60)  # 每60秒检查一次
```

### 4. 线程安全

所有资源管理器使用`threading.RLock`确保线程安全：

```python
import threading

pool = QAResourcePool.get_instance()

def worker():
    mongo = pool.get_mongo()
    # 多线程安全访问
    db = mongo.get_database('quantaxis')
    # ...

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

---

## 💡 最佳实践

### 1. 使用with语句

✅ **推荐**:
```python
with QAMongoResourceManager() as mongo:
    db = mongo.get_database('quantaxis')
    # 操作...
# 自动关闭
```

❌ **不推荐**:
```python
mongo = QAMongoResourceManager()
mongo.connect()
db = mongo.get_database('quantaxis')
# 忘记close() - 资源泄漏!
```

### 2. 使用资源池管理全局资源

✅ **推荐** (长期运行的应用):
```python
pool = QAResourcePool.get_instance()
mongo = pool.get_mongo()  # 复用同一连接
rabbitmq = pool.get_rabbitmq()

# 应用运行...

# 程序退出时自动清理(atexit)
```

❌ **不推荐** (频繁创建销毁):
```python
for i in range(1000):
    with QAMongoResourceManager() as mongo:  # 每次创建新连接!
        db = mongo.get_database('quantaxis')
```

### 3. 异常处理

✅ **推荐**:
```python
try:
    with QAMongoResourceManager() as mongo:
        db = mongo.get_database('quantaxis')
        # 操作可能抛出异常...
except pymongo.errors.ConnectionFailure as e:
    print(f"MongoDB连接失败: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

### 4. 配置外部化

✅ **推荐**:
```python
# config.py
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')

# app.py
from config import MONGODB_URI, RABBITMQ_HOST

with QAMongoResourceManager(uri=MONGODB_URI) as mongo:
    # ...
```

### 5. 日志监控

```python
import logging

logging.basicConfig(level=logging.INFO)

# QAResourceManager会自动记录:
# - 连接成功/失败
# - 资源关闭
# - 重连尝试
# - 错误信息
```

---

## 📊 性能优化

### MongoDB连接池调优

```python
mongo = QAMongoResourceManager(
    max_pool_size=200,                # 高并发场景
    server_selection_timeout_ms=10000, # 增加超时
)
```

### RabbitMQ心跳调优

```python
rabbitmq = QARabbitMQResourceManager(
    heartbeat=300,        # 减少心跳频率(低流量场景)
    socket_timeout=10     # 增加超时(慢网络)
)
```

### ClickHouse查询优化

```python
clickhouse = QAClickHouseResourceManager(
    insert_block_size=500000000,  # 超大批量插入
)

# 查询时使用压缩
df = clickhouse.query_dataframe("""
    SELECT * FROM stock_day
    WHERE code IN ('000001', '000002')
    SETTINGS max_threads = 8
""")
```

### Redis连接池调优

```python
redis_mgr = QARedisResourceManager(
    max_connections=100,         # 高并发场景
    socket_keepalive=True,       # 保持连接
    health_check_interval=60     # 增加健康检查间隔
)
```

---

## 🐛 故障排查

### 问题1: ImportError

```
ImportError: No module named 'pymongo'
```

**解决**:
```bash
pip install pymongo motor pika clickhouse-driver redis
# 或
pip install quantaxis[full]
```

### 问题2: 连接超时

```
pymongo.errors.ServerSelectionTimeoutError
```

**解决**:
```python
# 增加超时时间
mongo = QAMongoResourceManager(
    server_selection_timeout_ms=10000  # 10秒
)
```

### 问题3: 资源泄漏

**症状**: 程序运行一段时间后，数据库连接数不断增加

**解决**:
```python
# 方法1: 使用with语句
with QAMongoResourceManager() as mongo:
    # 自动关闭

# 方法2: 使用资源池
pool = QAResourcePool.get_instance()
mongo = pool.get_mongo()  # 复用连接
```

### 问题4: RabbitMQ连接断开

**症状**: `pika.exceptions.StreamLostError`

**解决**:
```python
rabbitmq = QARabbitMQResourceManager(
    heartbeat=600,  # 启用心跳
)

# 或手动重连
try:
    channel = rabbitmq.get_channel()
except pika.exceptions.StreamLostError:
    rabbitmq.reconnect()
    channel = rabbitmq.get_channel()
```

---

## 📖 示例代码

完整示例请参考:
- **examples/resource_manager_example.py** - 9个完整示例
- **QUANTAXIS/QAUtil/QAResourceManager.py** - 源码和内联文档

---

## 🔗 相关文档

- [QUANTAXIS主文档](../../../README.md)
- [安装指南](../../../INSTALLATION.md)
- [快速入门](../../../QUICKSTART.md)
- [API参考](../../../API_REFERENCE.md)
- [最佳实践](../../../BEST_PRACTICES.md)

---

## 🤝 贡献

如果发现问题或有改进建议，欢迎:
- 提交Issue: https://github.com/QUANTAXIS/QUANTAXIS/issues
- 提交PR: https://github.com/QUANTAXIS/QUANTAXIS/pulls

---

## 📝 更新日志

### v2.1.0 (2025-01-25)
- ✨ 新增QAResourceManager统一资源管理器
- ✨ 新增MongoDB/RabbitMQ/ClickHouse/Redis管理器
- ✨ 新增QAResourcePool单例资源池
- ✨ 新增便捷上下文管理器函数
- ✨ 新增自动atexit清理机制
- ✨ 新增健康检查功能
- ✨ 新增线程安全支持

---

## 👥 作者

**@yutiansut @quantaxis**

## 📄 许可证

MIT License

Copyright (c) 2016-2025 yutiansut/QUANTAXIS
