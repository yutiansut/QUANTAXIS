# QAPubSub 模块文档

## 概述

QAPubSub 是 QUANTAXIS 的发布-订阅消息系统，基于 RabbitMQ 提供高效的消息队列服务。支持 1-1、1-n、n-n 的消息分发模式，可用于计算任务分发收集、实时订单流处理等场景。

## 模块架构

### 核心组件

1. **base.py**: 基础消息处理类
2. **producer.py**: 消息生产者
3. **consumer.py**: 消息消费者
4. **setting.py**: 配置管理
5. **declaters.py**: 队列声明和管理

## 主要功能

### 1. 消息生产者

```python
from QUANTAXIS.QAPubSub.producer import QAProducer

# 创建生产者
producer = QAProducer(
    host='localhost',
    port=5672,
    username='guest',
    password='guest'
)

# 发送消息
producer.send_message(
    exchange='qa_exchange',
    routing_key='data.stock',
    message={'code': '000001', 'price': 10.5}
)
```

### 2. 消息消费者

```python
from QUANTAXIS.QAPubSub.consumer import QAConsumer

# 定义消息处理函数
def process_message(channel, method, properties, body):
    data = json.loads(body)
    print(f"处理消息: {data}")
    # 确认消息
    channel.basic_ack(delivery_tag=method.delivery_tag)

# 创建消费者
consumer = QAConsumer(
    host='localhost',
    port=5672,
    username='guest',
    password='guest'
)

# 订阅消息
consumer.subscribe(
    queue='data_queue',
    callback=process_message
)

# 开始消费
consumer.start_consuming()
```

### 3. 分发模式

```python
# 1-1 模式：点对点消息
producer.send_direct('task_queue', task_data)

# 1-n 模式：广播消息
producer.send_fanout('broadcast_exchange', broadcast_data)

# n-n 模式：主题订阅
producer.send_topic('topic_exchange', 'stock.price.*', price_data)
```

## 使用场景

1. **实时数据分发**: 行情数据实时推送
2. **任务队列**: 计算任务分发和结果收集
3. **订单流处理**: 交易订单的实时处理
4. **系统解耦**: 微服务间异步通信

## 配置示例

```python
# 消息队列配置
RABBITMQ_CONFIG = {
    'host': 'localhost',
    'port': 5672,
    'username': 'quantaxis',
    'password': 'password',
    'virtual_host': '/qa'
}
```

## 相关模块

- **QAEngine**: 任务引擎，使用消息队列进行任务分发
- **QAWebServer**: Web服务，通过消息队列处理请求
- **QASchedule**: 调度系统，使用消息队列触发任务