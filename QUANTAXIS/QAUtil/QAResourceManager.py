# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2025 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
QAResourceManager - QUANTAXIS统一资源管理器

本模块提供对MongoDB/RabbitMQ/ClickHouse/Redis等外部资源的统一管理:

1. **连接池管理**: 复用连接,减少开销
2. **上下文管理**: 支持with语句,自动释放资源
3. **优雅关闭**: 确保资源正确释放,无泄漏
4. **自动重连**: 连接断开自动重试
5. **健康检查**: 定期检查连接状态

## 快速开始

### 1. MongoDB资源管理
```python
from QUANTAXIS.QAUtil.QAResourceManager import QAMongoResourceManager

# 使用上下文管理器(推荐)
with QAMongoResourceManager() as mongo:
    db = mongo.get_database('quantaxis')
    result = db.stock_day.find_one({'code': '000001'})
    print(result)
# 自动关闭连接

# 手动管理
mongo = QAMongoResourceManager()
try:
    db = mongo.get_database('quantaxis')
    # ... 操作 ...
finally:
    mongo.close()  # 确保关闭
```

### 2. RabbitMQ资源管理
```python
from QUANTAXIS.QAUtil.QAResourceManager import QARabbitMQResourceManager

with QARabbitMQResourceManager() as rabbitmq:
    channel = rabbitmq.get_channel()
    channel.basic_publish(
        exchange='',
        routing_key='test_queue',
        body='Hello QUANTAXIS'
    )
# 自动关闭连接和通道
```

### 3. ClickHouse资源管理
```python
from QUANTAXIS.QAUtil.QAResourceManager import QAClickHouseResourceManager

with QAClickHouseResourceManager() as clickhouse:
    df = clickhouse.execute("SELECT * FROM stock_day LIMIT 10")
    print(df.head())
# 自动关闭连接
```

### 4. Redis资源管理
```python
from QUANTAXIS.QAUtil.QAResourceManager import QARedisResourceManager

with QARedisResourceManager() as redis:
    redis.set('test_key', 'test_value')
    value = redis.get('test_key')
    print(value)
# 自动关闭连接
```

### 5. 统一资源池管理器
```python
from QUANTAXIS.QAUtil.QAResourceManager import QAResourcePool

# 创建资源池(单例模式)
pool = QAResourcePool.get_instance()

# 获取各类资源
mongo = pool.get_mongo()
rabbitmq = pool.get_rabbitmq()
clickhouse = pool.get_clickhouse()
redis = pool.get_redis()

# 使用资源...

# 关闭所有资源
pool.close_all()
```

## 作者

@yutiansut @quantaxis

## 版本

v2.1.0+ (2025)
"""

import threading
import atexit
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from contextlib import contextmanager

# 导入各类数据库客户端
try:
    import pymongo
    from motor.motor_asyncio import AsyncIOMotorClient
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

try:
    import pika
    HAS_PIKA = True
except ImportError:
    HAS_PIKA = False

try:
    from clickhouse_driver import Client as ClickHouseClient
    HAS_CLICKHOUSE = True
except ImportError:
    HAS_CLICKHOUSE = False

try:
    import redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

# 配置日志
logger = logging.getLogger(__name__)


# ============================================================================
# 基础资源管理器抽象类
# ============================================================================

class QABaseResourceManager(ABC):
    """
    基础资源管理器抽象类

    所有资源管理器必须实现的接口:
    - connect(): 建立连接
    - close(): 关闭连接
    - is_connected(): 检查连接状态
    - reconnect(): 重新连接
    - __enter__/__exit__: 上下文管理器支持
    """

    def __init__(self):
        self._client = None
        self._is_connected = False
        self._lock = threading.RLock()  # 线程安全锁

    @abstractmethod
    def connect(self):
        """建立连接(子类必须实现)"""
        pass

    @abstractmethod
    def close(self):
        """关闭连接(子类必须实现)"""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """检查连接状态(子类必须实现)"""
        pass

    def reconnect(self):
        """
        重新连接
        默认实现: 先关闭再重新连接
        """
        logger.info(f"{self.__class__.__name__}: 正在重新连接...")
        self.close()
        self.connect()

    def __enter__(self):
        """进入上下文管理器"""
        if not self.is_connected():
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器,自动关闭资源"""
        self.close()
        return False  # 不抑制异常

    def __del__(self):
        """析构函数,确保资源释放"""
        try:
            self.close()
        except Exception as e:
            logger.warning(f"{self.__class__.__name__}: 析构时关闭失败: {e}")


# ============================================================================
# MongoDB资源管理器
# ============================================================================

class QAMongoResourceManager(QABaseResourceManager):
    """
    MongoDB资源管理器

    功能:
    - 连接池管理(pymongo自带连接池,maxPoolSize=100)
    - 支持同步/异步客户端
    - 自动重连
    - 线程安全

    参数:
        uri (str): MongoDB连接URI, 默认从环境变量MONGODB获取
        max_pool_size (int): 连接池最大连接数, 默认100
        server_selection_timeout_ms (int): 服务器选择超时(毫秒), 默认5000
        async_mode (bool): 是否使用异步客户端, 默认False

    示例:
        >>> with QAMongoResourceManager() as mongo:
        ...     db = mongo.get_database('quantaxis')
        ...     result = db.stock_day.find_one({'code': '000001'})
    """

    def __init__(
        self,
        uri: Optional[str] = None,
        max_pool_size: int = 100,
        server_selection_timeout_ms: int = 5000,
        async_mode: bool = False
    ):
        super().__init__()

        if not HAS_PYMONGO:
            raise ImportError("pymongo未安装, 请执行: pip install pymongo motor")

        # 从环境变量或配置文件获取URI
        if uri is None:
            import os
            from QUANTAXIS.QAUtil.QASetting import QA_Setting
            try:
                uri = QA_Setting().mongo_uri
            except:
                mongo_host = os.getenv('MONGODB', 'localhost')
                uri = f'mongodb://{mongo_host}:27017'

        self.uri = uri
        self.max_pool_size = max_pool_size
        self.server_selection_timeout_ms = server_selection_timeout_ms
        self.async_mode = async_mode

    def connect(self):
        """建立MongoDB连接"""
        with self._lock:
            if self._is_connected:
                return

            try:
                if self.async_mode:
                    # 异步客户端
                    import asyncio
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    self._client = AsyncIOMotorClient(
                        self.uri,
                        io_loop=loop,
                        maxPoolSize=self.max_pool_size,
                        serverSelectionTimeoutMS=self.server_selection_timeout_ms
                    )
                else:
                    # 同步客户端
                    self._client = pymongo.MongoClient(
                        self.uri,
                        maxPoolSize=self.max_pool_size,
                        serverSelectionTimeoutMS=self.server_selection_timeout_ms,
                        # 连接池配置
                        minPoolSize=10,
                        maxIdleTimeMS=60000,  # 连接最大空闲时间60秒
                        waitQueueTimeoutMS=5000,  # 等待连接池超时5秒
                    )

                    # 测试连接
                    self._client.admin.command('ping')

                self._is_connected = True
                logger.info(f"MongoDB连接成功: {self.uri}")

            except Exception as e:
                self._is_connected = False
                logger.error(f"MongoDB连接失败: {e}")
                raise

    def close(self):
        """关闭MongoDB连接"""
        with self._lock:
            if self._client is not None:
                try:
                    self._client.close()
                    logger.info("MongoDB连接已关闭")
                except Exception as e:
                    logger.warning(f"MongoDB关闭失败: {e}")
                finally:
                    self._client = None
                    self._is_connected = False

    def is_connected(self) -> bool:
        """检查连接状态"""
        if not self._is_connected or self._client is None:
            return False

        try:
            # ping测试
            if not self.async_mode:
                self._client.admin.command('ping')
            return True
        except Exception:
            self._is_connected = False
            return False

    def get_database(self, name: str = 'quantaxis'):
        """
        获取数据库对象

        参数:
            name (str): 数据库名称, 默认'quantaxis'

        返回:
            pymongo.database.Database or motor.motor_asyncio.AsyncIOMotorDatabase
        """
        if not self.is_connected():
            self.connect()
        return self._client[name]

    def get_client(self):
        """获取原始客户端对象"""
        if not self.is_connected():
            self.connect()
        return self._client


# ============================================================================
# RabbitMQ资源管理器
# ============================================================================

class QARabbitMQResourceManager(QABaseResourceManager):
    """
    RabbitMQ资源管理器

    功能:
    - 连接和通道管理
    - 自动重连
    - 心跳保持
    - 优雅关闭

    参数:
        host (str): RabbitMQ主机地址
        port (int): 端口, 默认5672
        username (str): 用户名, 默认'admin'
        password (str): 密码, 默认'admin'
        vhost (str): 虚拟主机, 默认'/'
        heartbeat (int): 心跳间隔(秒), 默认600, 0表示禁用
        socket_timeout (int): Socket超时(秒), 默认5

    示例:
        >>> with QARabbitMQResourceManager() as rabbitmq:
        ...     channel = rabbitmq.get_channel()
        ...     channel.basic_publish(exchange='', routing_key='test', body='hello')
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 5672,
        username: str = 'admin',
        password: str = 'admin',
        vhost: str = '/',
        heartbeat: int = 600,
        socket_timeout: int = 5
    ):
        super().__init__()

        if not HAS_PIKA:
            raise ImportError("pika未安装, 请执行: pip install pika")

        # 从配置获取默认值
        if host is None:
            try:
                from QUANTAXIS.QAPubSub.setting import qapubsub_ip
                host = qapubsub_ip
            except:
                host = 'localhost'

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.heartbeat = heartbeat
        self.socket_timeout = socket_timeout

        self._connection = None
        self._channel = None

    def connect(self):
        """建立RabbitMQ连接"""
        with self._lock:
            if self._is_connected:
                return

            try:
                # 创建认证
                credentials = pika.PlainCredentials(
                    self.username,
                    self.password,
                    erase_on_connect=True  # 安全: 认证后清除密码
                )

                # 连接参数
                parameters = pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.vhost,
                    credentials=credentials,
                    heartbeat=self.heartbeat,
                    socket_timeout=self.socket_timeout,
                    # 重连配置
                    blocked_connection_timeout=300,
                )

                # 建立连接
                self._connection = pika.BlockingConnection(parameters)
                self._channel = self._connection.channel()

                self._is_connected = True
                logger.info(f"RabbitMQ连接成功: {self.host}:{self.port}/{self.vhost}")

            except Exception as e:
                self._is_connected = False
                logger.error(f"RabbitMQ连接失败: {e}")
                raise

    def close(self):
        """关闭RabbitMQ连接"""
        with self._lock:
            # 先关闭通道
            if self._channel is not None:
                try:
                    if self._channel.is_open:
                        self._channel.close()
                    logger.debug("RabbitMQ通道已关闭")
                except Exception as e:
                    logger.warning(f"RabbitMQ通道关闭失败: {e}")
                finally:
                    self._channel = None

            # 再关闭连接
            if self._connection is not None:
                try:
                    if self._connection.is_open:
                        self._connection.close()
                    logger.info("RabbitMQ连接已关闭")
                except Exception as e:
                    logger.warning(f"RabbitMQ连接关闭失败: {e}")
                finally:
                    self._connection = None
                    self._is_connected = False

    def is_connected(self) -> bool:
        """检查连接状态"""
        return (
            self._is_connected
            and self._connection is not None
            and self._connection.is_open
            and self._channel is not None
            and self._channel.is_open
        )

    def get_channel(self):
        """
        获取通道对象

        返回:
            pika.channel.Channel
        """
        if not self.is_connected():
            self.connect()
        return self._channel

    def get_connection(self):
        """获取连接对象"""
        if not self.is_connected():
            self.connect()
        return self._connection


# ============================================================================
# ClickHouse资源管理器
# ============================================================================

class QAClickHouseResourceManager(QABaseResourceManager):
    """
    ClickHouse资源管理器

    功能:
    - 连接管理
    - 自动重连
    - 数据压缩
    - 查询优化

    参数:
        host (str): ClickHouse主机地址
        port (int): 端口, 默认9000 (native protocol)
        database (str): 数据库名, 默认'quantaxis'
        user (str): 用户名, 默认'default'
        password (str): 密码, 默认''
        compression (bool): 是否启用压缩, 默认True
        insert_block_size (int): 插入块大小, 默认100000000

    示例:
        >>> with QAClickHouseResourceManager() as clickhouse:
        ...     df = clickhouse.execute("SELECT * FROM stock_day LIMIT 10")
        ...     print(df.head())
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: int = 9000,
        database: str = 'quantaxis',
        user: str = 'default',
        password: str = '',
        compression: bool = True,
        insert_block_size: int = 100000000
    ):
        super().__init__()

        if not HAS_CLICKHOUSE:
            raise ImportError("clickhouse-driver未安装, 请执行: pip install clickhouse-driver")

        # 从配置获取默认值
        if host is None:
            try:
                from qaenv import clickhouse_ip
                host = clickhouse_ip
            except:
                host = 'localhost'

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.compression = compression
        self.insert_block_size = insert_block_size

    def connect(self):
        """建立ClickHouse连接"""
        with self._lock:
            if self._is_connected:
                return

            try:
                self._client = ClickHouseClient(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    compression=self.compression,
                    settings={
                        'insert_block_size': self.insert_block_size,
                        # 查询优化设置
                        'max_threads': 4,
                        'max_block_size': 65536,
                    }
                )

                # 测试连接
                self._client.execute('SELECT 1')

                self._is_connected = True
                logger.info(f"ClickHouse连接成功: {self.host}:{self.port}/{self.database}")

            except Exception as e:
                self._is_connected = False
                logger.error(f"ClickHouse连接失败: {e}")
                raise

    def close(self):
        """关闭ClickHouse连接"""
        with self._lock:
            if self._client is not None:
                try:
                    self._client.disconnect()
                    logger.info("ClickHouse连接已关闭")
                except Exception as e:
                    logger.warning(f"ClickHouse关闭失败: {e}")
                finally:
                    self._client = None
                    self._is_connected = False

    def is_connected(self) -> bool:
        """检查连接状态"""
        if not self._is_connected or self._client is None:
            return False

        try:
            # 简单查询测试
            self._client.execute('SELECT 1')
            return True
        except Exception:
            self._is_connected = False
            return False

    def execute(self, sql: str, with_column_types: bool = False):
        """
        执行SQL查询

        参数:
            sql (str): SQL语句
            with_column_types (bool): 是否返回列类型信息

        返回:
            list or tuple: 查询结果
        """
        if not self.is_connected():
            self.connect()
        return self._client.execute(sql, with_column_types=with_column_types)

    def query_dataframe(self, sql: str):
        """
        执行查询并返回DataFrame

        参数:
            sql (str): SQL语句

        返回:
            pandas.DataFrame: 查询结果
        """
        if not self.is_connected():
            self.connect()
        return self._client.query_dataframe(sql)

    def get_client(self):
        """获取原始客户端对象"""
        if not self.is_connected():
            self.connect()
        return self._client


# ============================================================================
# Redis资源管理器
# ============================================================================

class QARedisResourceManager(QABaseResourceManager):
    """
    Redis资源管理器

    功能:
    - 连接池管理
    - 自动重连
    - 健康检查
    - 管道支持

    参数:
        host (str): Redis主机地址, 默认'localhost'
        port (int): 端口, 默认6379
        db (int): 数据库编号, 默认0
        password (str): 密码, 默认None
        max_connections (int): 连接池最大连接数, 默认50
        socket_timeout (int): Socket超时(秒), 默认5
        socket_keepalive (bool): 是否启用TCP keepalive, 默认True
        decode_responses (bool): 是否解码响应为字符串, 默认True

    示例:
        >>> with QARedisResourceManager() as redis_mgr:
        ...     redis_mgr.set('test_key', 'test_value')
        ...     value = redis_mgr.get('test_key')
        ...     print(value)
    """

    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 50,
        socket_timeout: int = 5,
        socket_keepalive: bool = True,
        decode_responses: bool = True
    ):
        super().__init__()

        if not HAS_REDIS:
            raise ImportError("redis未安装, 请执行: pip install redis")

        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.max_connections = max_connections
        self.socket_timeout = socket_timeout
        self.socket_keepalive = socket_keepalive
        self.decode_responses = decode_responses

        self._connection_pool = None

    def connect(self):
        """建立Redis连接"""
        with self._lock:
            if self._is_connected:
                return

            try:
                # 创建连接池
                self._connection_pool = redis.ConnectionPool(
                    host=self.host,
                    port=self.port,
                    db=self.db,
                    password=self.password,
                    max_connections=self.max_connections,
                    socket_timeout=self.socket_timeout,
                    socket_keepalive=self.socket_keepalive,
                    decode_responses=self.decode_responses,
                    # 健康检查
                    health_check_interval=30,
                )

                # 创建客户端
                self._client = redis.Redis(connection_pool=self._connection_pool)

                # 测试连接
                self._client.ping()

                self._is_connected = True
                logger.info(f"Redis连接成功: {self.host}:{self.port}/{self.db}")

            except Exception as e:
                self._is_connected = False
                logger.error(f"Redis连接失败: {e}")
                raise

    def close(self):
        """关闭Redis连接"""
        with self._lock:
            if self._connection_pool is not None:
                try:
                    self._connection_pool.disconnect()
                    logger.info("Redis连接已关闭")
                except Exception as e:
                    logger.warning(f"Redis关闭失败: {e}")
                finally:
                    self._connection_pool = None
                    self._client = None
                    self._is_connected = False

    def is_connected(self) -> bool:
        """检查连接状态"""
        if not self._is_connected or self._client is None:
            return False

        try:
            # ping测试
            self._client.ping()
            return True
        except Exception:
            self._is_connected = False
            return False

    def get_client(self):
        """获取Redis客户端对象"""
        if not self.is_connected():
            self.connect()
        return self._client

    def pipeline(self, transaction=True):
        """
        创建管道对象

        参数:
            transaction (bool): 是否启用事务, 默认True

        返回:
            redis.client.Pipeline
        """
        if not self.is_connected():
            self.connect()
        return self._client.pipeline(transaction=transaction)

    # 提供常用Redis命令的快捷方法
    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        """设置键值"""
        if not self.is_connected():
            self.connect()
        return self._client.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def get(self, key):
        """获取值"""
        if not self.is_connected():
            self.connect()
        return self._client.get(key)

    def delete(self, *keys):
        """删除键"""
        if not self.is_connected():
            self.connect()
        return self._client.delete(*keys)

    def exists(self, *keys):
        """检查键是否存在"""
        if not self.is_connected():
            self.connect()
        return self._client.exists(*keys)


# ============================================================================
# 统一资源池管理器 (单例模式)
# ============================================================================

class QAResourcePool:
    """
    统一资源池管理器(单例模式)

    功能:
    - 管理所有类型的资源连接
    - 单例模式,全局唯一
    - 自动注册atexit清理
    - 线程安全

    示例:
        >>> pool = QAResourcePool.get_instance()
        >>> mongo = pool.get_mongo()
        >>> rabbitmq = pool.get_rabbitmq()
        >>> # 使用资源...
        >>> pool.close_all()  # 关闭所有资源
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 只初始化一次
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self._resources: Dict[str, QABaseResourceManager] = {}
        self._resource_lock = threading.RLock()

        # 注册程序退出时的清理函数
        atexit.register(self.close_all)
        logger.info("QAResourcePool已初始化")

    @classmethod
    def get_instance(cls) -> 'QAResourcePool':
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_mongo(self, **kwargs) -> QAMongoResourceManager:
        """
        获取MongoDB资源管理器

        参数:
            **kwargs: 传递给QAMongoResourceManager的参数

        返回:
            QAMongoResourceManager
        """
        return self._get_or_create_resource('mongo', QAMongoResourceManager, **kwargs)

    def get_rabbitmq(self, **kwargs) -> QARabbitMQResourceManager:
        """
        获取RabbitMQ资源管理器

        参数:
            **kwargs: 传递给QARabbitMQResourceManager的参数

        返回:
            QARabbitMQResourceManager
        """
        return self._get_or_create_resource('rabbitmq', QARabbitMQResourceManager, **kwargs)

    def get_clickhouse(self, **kwargs) -> QAClickHouseResourceManager:
        """
        获取ClickHouse资源管理器

        参数:
            **kwargs: 传递给QAClickHouseResourceManager的参数

        返回:
            QAClickHouseResourceManager
        """
        return self._get_or_create_resource('clickhouse', QAClickHouseResourceManager, **kwargs)

    def get_redis(self, **kwargs) -> QARedisResourceManager:
        """
        获取Redis资源管理器

        参数:
            **kwargs: 传递给QARedisResourceManager的参数

        返回:
            QARedisResourceManager
        """
        return self._get_or_create_resource('redis', QARedisResourceManager, **kwargs)

    def _get_or_create_resource(
        self,
        key: str,
        resource_class: type,
        **kwargs
    ) -> QABaseResourceManager:
        """
        获取或创建资源管理器

        参数:
            key (str): 资源键名
            resource_class (type): 资源管理器类
            **kwargs: 传递给资源管理器的参数

        返回:
            QABaseResourceManager子类实例
        """
        with self._resource_lock:
            if key not in self._resources:
                self._resources[key] = resource_class(**kwargs)
                logger.info(f"创建资源管理器: {key}")
            return self._resources[key]

    def close_resource(self, key: str):
        """
        关闭指定资源

        参数:
            key (str): 资源键名 ('mongo', 'rabbitmq', 'clickhouse', 'redis')
        """
        with self._resource_lock:
            if key in self._resources:
                try:
                    self._resources[key].close()
                    del self._resources[key]
                    logger.info(f"资源已关闭: {key}")
                except Exception as e:
                    logger.error(f"关闭资源失败 {key}: {e}")

    def close_all(self):
        """关闭所有资源"""
        with self._resource_lock:
            logger.info("正在关闭所有资源...")
            for key in list(self._resources.keys()):
                self.close_resource(key)
            logger.info("所有资源已关闭")

    def health_check(self) -> Dict[str, bool]:
        """
        健康检查

        返回:
            dict: {资源名: 连接状态}
        """
        with self._resource_lock:
            result = {}
            for key, resource in self._resources.items():
                try:
                    result[key] = resource.is_connected()
                except Exception as e:
                    logger.warning(f"健康检查失败 {key}: {e}")
                    result[key] = False
            return result


# ============================================================================
# 便捷函数
# ============================================================================

@contextmanager
def get_mongo_resource(**kwargs):
    """
    上下文管理器: 获取MongoDB资源

    示例:
        >>> with get_mongo_resource() as mongo:
        ...     db = mongo.get_database('quantaxis')
        ...     # 使用数据库...
    """
    manager = QAMongoResourceManager(**kwargs)
    try:
        yield manager
    finally:
        manager.close()


@contextmanager
def get_rabbitmq_resource(**kwargs):
    """
    上下文管理器: 获取RabbitMQ资源

    示例:
        >>> with get_rabbitmq_resource() as rabbitmq:
        ...     channel = rabbitmq.get_channel()
        ...     # 使用通道...
    """
    manager = QARabbitMQResourceManager(**kwargs)
    try:
        yield manager
    finally:
        manager.close()


@contextmanager
def get_clickhouse_resource(**kwargs):
    """
    上下文管理器: 获取ClickHouse资源

    示例:
        >>> with get_clickhouse_resource() as clickhouse:
        ...     df = clickhouse.query_dataframe("SELECT * FROM stock_day LIMIT 10")
        ...     # 使用数据...
    """
    manager = QAClickHouseResourceManager(**kwargs)
    try:
        yield manager
    finally:
        manager.close()


@contextmanager
def get_redis_resource(**kwargs):
    """
    上下文管理器: 获取Redis资源

    示例:
        >>> with get_redis_resource() as redis_mgr:
        ...     redis_mgr.set('key', 'value')
        ...     # 使用Redis...
    """
    manager = QARedisResourceManager(**kwargs)
    try:
        yield manager
    finally:
        manager.close()


# ============================================================================
# 导出接口
# ============================================================================

__all__ = [
    # 基础类
    'QABaseResourceManager',

    # 资源管理器
    'QAMongoResourceManager',
    'QARabbitMQResourceManager',
    'QAClickHouseResourceManager',
    'QARedisResourceManager',

    # 资源池
    'QAResourcePool',

    # 便捷函数
    'get_mongo_resource',
    'get_rabbitmq_resource',
    'get_clickhouse_resource',
    'get_redis_resource',
]


if __name__ == '__main__':
    # 测试代码
    logging.basicConfig(level=logging.INFO)

    print("=== QAResourceManager测试 ===\n")

    # 测试MongoDB
    print("1. 测试MongoDB...")
    try:
        with QAMongoResourceManager() as mongo:
            print(f"   MongoDB连接状态: {mongo.is_connected()}")
            db = mongo.get_database('test')
            print(f"   数据库: {db.name}")
    except Exception as e:
        print(f"   MongoDB测试失败: {e}")

    # 测试资源池
    print("\n2. 测试QAResourcePool...")
    pool = QAResourcePool.get_instance()
    print(f"   资源池实例: {pool}")

    # 健康检查
    health = pool.health_check()
    print(f"   健康检查: {health}")

    # 关闭所有资源
    pool.close_all()
    print("\n测试完成!")
