# QAEngine 模块文档

## 概述

QAEngine 是 QUANTAXIS 的任务引擎模块，提供了多线程、多进程和异步任务处理能力。该模块为量化交易系统提供了高效的并行计算和任务调度基础设施，支持分布式计算和实时任务处理。

## 模块架构

### 核心组件

1. **QATask.py**: 基础任务类定义
2. **QAThreadEngine.py**: 多线程执行引擎
3. **QAAsyncTask.py**: 异步任务处理
4. **QAAsyncThread.py**: 异步线程管理
5. **QAAsyncSchedule.py**: 异步调度器
6. **QAEvent.py**: 事件处理系统

## 主要功能

### 1. 任务管理 (QATask)

```python
from QUANTAXIS.QAEngine.QATask import QATask

class DataProcessTask(QATask):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def run(self):
        # 执行数据处理逻辑
        result = self.process_data(self.data)
        return result
```

### 2. 多线程引擎 (QAThreadEngine)

```python
from QUANTAXIS.QAEngine.QAThreadEngine import QAThreadEngine

# 创建线程引擎
engine = QAThreadEngine(worker_num=4)

# 添加任务
tasks = [DataProcessTask(data) for data in dataset]
engine.add_tasks(tasks)

# 执行任务
results = engine.run()
```

### 3. 异步任务 (QAAsyncTask)

```python
from QUANTAXIS.QAEngine.QAAsyncTask import QAAsyncTask
import asyncio

class AsyncDataFetcher(QAAsyncTask):
    async def run(self):
        data = await self.fetch_data_async()
        return await self.process_data_async(data)

# 运行异步任务
async def main():
    task = AsyncDataFetcher()
    result = await task.run()
```

### 4. 事件系统 (QAEvent)

```python
from QUANTAXIS.QAEngine.QAEvent import QAEvent

# 定义事件处理器
def on_data_received(event_data):
    print(f"收到数据: {event_data}")

# 创建事件
event = QAEvent('data_received')
event.subscribe(on_data_received)

# 触发事件
event.emit({'data': 'sample_data'})
```

## 使用场景

1. **大批量数据处理**: 并行处理股票数据
2. **实时策略计算**: 多线程策略执行
3. **异步数据获取**: 非阻塞数据获取
4. **任务调度**: 定时任务和事件驱动任务

## 相关模块

- **QAPubSub**: 消息队列和通信
- **QASchedule**: 任务调度
- **QAStrategy**: 策略并行执行