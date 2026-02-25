# coding:utf-8
"""
QAResourceManager使用示例

本文件演示如何使用QUANTAXIS统一资源管理器进行MongoDB/RabbitMQ/ClickHouse/Redis资源管理

作者: @yutiansut @quantaxis
版本: 2.1.0+
日期: 2025
"""

import logging
from typing import Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ============================================================================
# 示例1: MongoDB资源管理 (推荐使用with语句)
# ============================================================================

def example1_mongodb_context_manager():
    """
    示例1: 使用with语句管理MongoDB连接

    优点:
    - 自动连接和断开
    - 异常安全
    - 代码简洁
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QAMongoResourceManager

    print("\n" + "=" * 70)
    print("示例1: MongoDB上下文管理器")
    print("=" * 70)

    try:
        # 使用with语句(推荐)
        with QAMongoResourceManager() as mongo:
            # 获取数据库
            db = mongo.get_database('quantaxis')

            # 示例操作: 查询股票日线数据
            result = db.stock_day.find_one({'code': '000001'})
            if result:
                print(f"✅ 查询成功: {result.get('code')} - {result.get('date')}")
            else:
                print("⚠️  未找到数据")

            # 示例操作: 统计集合数量
            collections = db.list_collection_names()
            print(f"✅ 数据库集合数量: {len(collections)}")

        # with块结束后,连接自动关闭
        print("✅ MongoDB连接已自动关闭")

    except Exception as e:
        print(f"❌ MongoDB操作失败: {e}")


def example2_mongodb_manual_management():
    """
    示例2: 手动管理MongoDB连接

    适用场景:
    - 需要长时间保持连接
    - 跨函数使用同一连接
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QAMongoResourceManager

    print("\n" + "=" * 70)
    print("示例2: MongoDB手动管理")
    print("=" * 70)

    mongo = None
    try:
        # 创建资源管理器
        mongo = QAMongoResourceManager()

        # 显式连接
        mongo.connect()
        print(f"✅ MongoDB连接状态: {mongo.is_connected()}")

        # 使用连接
        db = mongo.get_database('quantaxis')
        count = db.stock_list.count_documents({})
        print(f"✅ 股票列表数量: {count}")

    except Exception as e:
        print(f"❌ MongoDB操作失败: {e}")

    finally:
        # 确保连接关闭
        if mongo is not None:
            mongo.close()
            print("✅ MongoDB连接已手动关闭")


def example3_mongodb_async():
    """
    示例3: 异步MongoDB连接

    适用场景:
    - 异步IO应用
    - 高并发场景
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QAMongoResourceManager
    import asyncio

    print("\n" + "=" * 70)
    print("示例3: MongoDB异步连接")
    print("=" * 70)

    async def async_query():
        # 创建异步客户端
        async with QAMongoResourceManager(async_mode=True) as mongo:
            db = mongo.get_database('quantaxis')

            # 异步查询
            result = await db.stock_day.find_one({'code': '000001'})
            if result:
                print(f"✅ 异步查询成功: {result.get('code')}")
            return result

    try:
        # 运行异步函数
        asyncio.run(async_query())
        print("✅ 异步MongoDB操作完成")
    except Exception as e:
        print(f"❌ 异步操作失败: {e}")


# ============================================================================
# 示例4: RabbitMQ资源管理
# ============================================================================

def example4_rabbitmq():
    """
    示例4: RabbitMQ消息队列管理

    功能:
    - 发布消息
    - 消费消息
    - 自动关闭连接和通道
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QARabbitMQResourceManager

    print("\n" + "=" * 70)
    print("示例4: RabbitMQ消息队列")
    print("=" * 70)

    try:
        with QARabbitMQResourceManager() as rabbitmq:
            # 获取通道
            channel = rabbitmq.get_channel()

            # 声明队列
            queue_name = 'test_queue'
            channel.queue_declare(queue=queue_name, durable=True)
            print(f"✅ 队列声明成功: {queue_name}")

            # 发布消息
            message = '{"type": "test", "data": "Hello QUANTAXIS!"}'
            channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message
            )
            print(f"✅ 消息发布成功: {message}")

            # 消费一条消息
            method_frame, header_frame, body = channel.basic_get(queue=queue_name)
            if method_frame:
                print(f"✅ 消息接收: {body.decode()}")
                channel.basic_ack(method_frame.delivery_tag)
            else:
                print("⚠️  队列为空")

        print("✅ RabbitMQ连接和通道已自动关闭")

    except Exception as e:
        print(f"❌ RabbitMQ操作失败: {e}")


# ============================================================================
# 示例5: ClickHouse资源管理
# ============================================================================

def example5_clickhouse():
    """
    示例5: ClickHouse高性能分析数据库

    功能:
    - 执行SQL查询
    - 返回DataFrame
    - 自动连接管理
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QAClickHouseResourceManager

    print("\n" + "=" * 70)
    print("示例5: ClickHouse分析查询")
    print("=" * 70)

    try:
        with QAClickHouseResourceManager() as clickhouse:
            # 测试查询
            result = clickhouse.execute("SELECT version()")
            print(f"✅ ClickHouse版本: {result[0][0]}")

            # 查询并返回DataFrame
            sql = """
            SELECT * FROM stock_day
            WHERE code = '000001'
            LIMIT 10
            """
            df = clickhouse.query_dataframe(sql)
            if not df.empty:
                print(f"✅ 查询成功, 返回{len(df)}行数据")
                print(df.head())
            else:
                print("⚠️  未查询到数据")

        print("✅ ClickHouse连接已自动关闭")

    except Exception as e:
        print(f"❌ ClickHouse操作失败: {e}")


# ============================================================================
# 示例6: Redis资源管理
# ============================================================================

def example6_redis():
    """
    示例6: Redis缓存管理

    功能:
    - 键值存取
    - 管道操作
    - 连接池管理
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QARedisResourceManager

    print("\n" + "=" * 70)
    print("示例6: Redis缓存操作")
    print("=" * 70)

    try:
        with QARedisResourceManager() as redis_mgr:
            # 测试连接
            client = redis_mgr.get_client()
            print(f"✅ Redis连接成功: {client.ping()}")

            # 基本操作
            redis_mgr.set('test_key', 'test_value', ex=60)  # 60秒过期
            value = redis_mgr.get('test_key')
            print(f"✅ 键值操作: test_key = {value}")

            # 管道操作(批量)
            pipe = redis_mgr.pipeline()
            pipe.set('key1', 'value1')
            pipe.set('key2', 'value2')
            pipe.set('key3', 'value3')
            pipe.execute()
            print("✅ 管道操作: 批量设置3个键值")

            # 检查存在
            exists = redis_mgr.exists('key1', 'key2', 'key3')
            print(f"✅ 键存在检查: {exists}个键存在")

            # 清理
            redis_mgr.delete('test_key', 'key1', 'key2', 'key3')
            print("✅ 键已删除")

        print("✅ Redis连接已自动关闭")

    except Exception as e:
        print(f"❌ Redis操作失败: {e}")


# ============================================================================
# 示例7: 统一资源池管理 (推荐用于复杂应用)
# ============================================================================

def example7_resource_pool():
    """
    示例7: 使用QAResourcePool统一管理所有资源

    优点:
    - 单例模式,全局共享
    - 统一管理所有资源
    - 自动atexit清理
    - 健康检查
    """
    from QUANTAXIS.QAUtil.QAResourceManager import QAResourcePool

    print("\n" + "=" * 70)
    print("示例7: 统一资源池")
    print("=" * 70)

    # 获取单例实例
    pool = QAResourcePool.get_instance()
    print(f"✅ 资源池实例: {pool}")

    try:
        # 获取MongoDB资源
        mongo = pool.get_mongo()
        print(f"✅ MongoDB连接: {mongo.is_connected()}")

        # 获取RabbitMQ资源
        try:
            rabbitmq = pool.get_rabbitmq()
            print(f"✅ RabbitMQ连接: {rabbitmq.is_connected()}")
        except Exception as e:
            print(f"⚠️  RabbitMQ不可用: {e}")

        # 获取ClickHouse资源
        try:
            clickhouse = pool.get_clickhouse()
            print(f"✅ ClickHouse连接: {clickhouse.is_connected()}")
        except Exception as e:
            print(f"⚠️  ClickHouse不可用: {e}")

        # 获取Redis资源
        try:
            redis_mgr = pool.get_redis()
            print(f"✅ Redis连接: {redis_mgr.is_connected()}")
        except Exception as e:
            print(f"⚠️  Redis不可用: {e}")

        # 健康检查
        health = pool.health_check()
        print(f"\n📊 健康检查:")
        for resource, status in health.items():
            status_icon = "✅" if status else "❌"
            print(f"   {status_icon} {resource}: {'正常' if status else '异常'}")

        # 使用资源进行业务逻辑...
        db = mongo.get_database('quantaxis')
        collections_count = len(db.list_collection_names())
        print(f"\n✅ MongoDB数据库集合数: {collections_count}")

    finally:
        # 关闭所有资源
        pool.close_all()
        print("\n✅ 所有资源已关闭")


# ============================================================================
# 示例8: 便捷函数
# ============================================================================

def example8_convenience_functions():
    """
    示例8: 使用便捷函数

    特点:
    - 更简洁的API
    - 自动资源管理
    """
    from QUANTAXIS.QAUtil.QAResourceManager import (
        get_mongo_resource,
        get_rabbitmq_resource,
        get_clickhouse_resource,
        get_redis_resource
    )

    print("\n" + "=" * 70)
    print("示例8: 便捷函数")
    print("=" * 70)

    # MongoDB便捷函数
    try:
        with get_mongo_resource() as mongo:
            db = mongo.get_database('test')
            print(f"✅ MongoDB便捷函数: 数据库={db.name}")
    except Exception as e:
        print(f"❌ MongoDB: {e}")

    # RabbitMQ便捷函数
    try:
        with get_rabbitmq_resource() as rabbitmq:
            channel = rabbitmq.get_channel()
            print(f"✅ RabbitMQ便捷函数: 通道={channel.channel_number}")
    except Exception as e:
        print(f"❌ RabbitMQ: {e}")

    # Redis便捷函数
    try:
        with get_redis_resource() as redis_mgr:
            redis_mgr.set('temp_key', 'temp_value')
            print(f"✅ Redis便捷函数: 值={redis_mgr.get('temp_key')}")
            redis_mgr.delete('temp_key')
    except Exception as e:
        print(f"❌ Redis: {e}")


# ============================================================================
# 示例9: 实战场景 - 量化策略中的资源管理
# ============================================================================

class QuantStrategy:
    """
    量化策略示例

    演示在实际策略中如何使用资源管理器
    """

    def __init__(self):
        """初始化策略,获取资源池"""
        from QUANTAXIS.QAUtil.QAResourceManager import QAResourcePool
        self.pool = QAResourcePool.get_instance()
        self.mongo = self.pool.get_mongo()
        self.redis = self.pool.get_redis()

        print("✅ 策略初始化完成")

    def get_market_data(self, code: str, start: str, end: str):
        """从MongoDB获取市场数据"""
        db = self.mongo.get_database('quantaxis')
        cursor = db.stock_day.find({
            'code': code,
            'date': {'$gte': start, '$lte': end}
        })
        data = list(cursor)
        print(f"✅ 获取{code}市场数据: {len(data)}条")
        return data

    def cache_signal(self, code: str, signal: dict):
        """缓存交易信号到Redis"""
        import json
        key = f"signal:{code}"
        value = json.dumps(signal)
        self.redis.set(key, value, ex=300)  # 缓存5分钟
        print(f"✅ 缓存信号: {key} = {signal}")

    def get_cached_signal(self, code: str) -> Optional[dict]:
        """从Redis获取缓存的信号"""
        import json
        key = f"signal:{code}"
        value = self.redis.get(key)
        if value:
            signal = json.loads(value)
            print(f"✅ 读取缓存信号: {key}")
            return signal
        return None

    def run(self):
        """运行策略"""
        print("\n📈 策略运行中...")

        # 获取数据
        data = self.get_market_data('000001', '2024-01-01', '2024-01-31')

        # 计算信号
        signal = {
            'code': '000001',
            'action': 'BUY',
            'price': 10.5,
            'volume': 1000
        }

        # 缓存信号
        self.cache_signal('000001', signal)

        # 读取缓存
        cached = self.get_cached_signal('000001')

        print("✅ 策略运行完成")

    def cleanup(self):
        """清理资源"""
        self.pool.close_all()
        print("✅ 策略资源清理完成")


def example9_strategy():
    """
    示例9: 量化策略中的资源管理
    """
    print("\n" + "=" * 70)
    print("示例9: 量化策略资源管理")
    print("=" * 70)

    strategy = None
    try:
        strategy = QuantStrategy()
        strategy.run()
    except Exception as e:
        print(f"❌ 策略运行失败: {e}")
    finally:
        if strategy:
            strategy.cleanup()


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行所有示例"""
    print("\n" + "=" * 70)
    print("QUANTAXIS资源管理器示例集")
    print("=" * 70)

    examples = [
        ("MongoDB上下文管理器", example1_mongodb_context_manager),
        ("MongoDB手动管理", example2_mongodb_manual_management),
        # ("MongoDB异步连接", example3_mongodb_async),  # 需要异步环境
        ("RabbitMQ消息队列", example4_rabbitmq),
        ("ClickHouse分析查询", example5_clickhouse),
        ("Redis缓存操作", example6_redis),
        ("统一资源池", example7_resource_pool),
        ("便捷函数", example8_convenience_functions),
        ("量化策略", example9_strategy),
    ]

    for name, func in examples:
        try:
            print(f"\n\n{'='*70}")
            print(f"运行示例: {name}")
            print(f"{'='*70}")
            func()
        except Exception as e:
            print(f"\n❌ 示例'{name}'运行失败: {e}")
            import traceback
            traceback.print_exc()

    print("\n\n" + "=" * 70)
    print("所有示例运行完成!")
    print("=" * 70)


if __name__ == '__main__':
    main()
