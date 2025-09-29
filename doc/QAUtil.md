# QAUtil 模块文档

## 概述

QAUtil 是 QUANTAXIS 的核心工具模块，提供了丰富的实用功能，包括时间处理、数据转换、文件操作、数据库连接、配置管理等基础设施功能，是整个框架的基础支撑模块。

## 模块架构

### 核心组件

1. **时间处理工具**
   - **QADate.py**: 基础时间日期处理
   - **QADate_trade.py**: 交易日期和时间处理
   - **QADateTools.py**: 高级日期工具
   - **QABar.py**: 时间周期处理

2. **数据处理工具**
   - **QATransform.py**: 数据格式转换
   - **QACode.py**: 股票代码处理
   - **QAList.py**: 列表操作工具
   - **QADict.py**: 字典操作工具

3. **系统工具**
   - **QASetting.py**: 系统配置管理
   - **QAMongo.py**: MongoDB数据库操作
   - **QASql.py**: SQL相关工具
   - **QACache.py**: 缓存管理

4. **辅助工具**
   - **QALogs.py**: 日志管理
   - **QAFile.py**: 文件操作
   - **QAMail.py**: 邮件发送
   - **QAWebutil.py**: 网络工具

## 主要功能

### 时间日期处理

#### 基础时间功能 (QADate)

```python
# 时间戳转换
QA_util_date_stamp('2020-01-01')  # 获取时间戳
QA_util_stamp2datetime(timestamp)  # 时间戳转datetime

# 日期格式转换
QA_util_date_str2int('2020-01-01')  # 字符串转整数
QA_util_date_int2str(20200101)      # 整数转字符串

# 获取当前时间
QA_util_date_today()    # 今日日期
QA_util_time_now()      # 当前时间
QA_util_today_str()     # 今日字符串格式
```

#### 交易时间处理 (QADate_trade)

```python
# 交易日判断
QA_util_if_trade('2020-01-01')      # 是否交易日
QA_util_if_tradetime('09:30:00')    # 是否交易时间

# 交易日计算
QA_util_get_next_trade_date('2020-01-01')  # 下一个交易日
QA_util_get_pre_trade_date('2020-01-01')   # 前一个交易日

# 获取交易日期范围
QA_util_get_trade_range('2020-01-01', '2020-01-31')

# 期货时间转换
QA_util_future_to_realdatetime('2020-01-01 21:00:00')
```

#### 日期工具 (QADateTools)

```python
# 月份计算
QA_util_add_months('2020-01-01', 3)        # 增加月份
QA_util_getBetweenMonth('2020-01', '2020-12')  # 获取月份列表

# 季度计算
QA_util_getBetweenQuarter('2020-Q1', '2020-Q4')
```

### 数据格式转换

#### 格式转换 (QATransform)

```python
# pandas 相关转换
QA_util_to_json_from_pandas(df)           # DataFrame转JSON
QA_util_to_pandas_from_json(json_data)    # JSON转DataFrame
QA_util_to_list_from_pandas(df)           # DataFrame转列表

# numpy 相关转换
QA_util_to_list_from_numpy(np_array)      # numpy数组转列表
```

#### 代码处理 (QACode)

```python
# 股票代码格式处理
QA_util_code_tostr(codes)           # 代码列表转字符串
QA_util_code_tolist('000001,000002') # 字符串转代码列表
QA_util_code_adjust_ctp(code)       # CTP代码调整
QA_util_code_change_format(code, 'wind')  # 代码格式转换
```

### 数据库操作

#### MongoDB 工具 (QAMongo)

```python
# MongoDB 连接管理
QA_util_mongo_initial()         # 初始化MongoDB连接
QA_util_mongo_status()          # 检查MongoDB状态
QA_util_mongo_infos()           # 获取MongoDB信息
```

#### SQL 工具 (QASql)

```python
# MongoDB查询配置
QA_util_sql_mongo_setting(ip, port, user, password)
QA_util_sql_async_mongo_setting(ip, port, user, password)

# 排序设置
QA_util_sql_mongo_sort_ASCENDING()   # 升序排列
QA_util_sql_mongo_sort_DESCENDING()  # 降序排列
```

### 系统配置

#### 配置管理 (QASetting)

```python
# 系统配置
from QUANTAXIS.QAUtil import QASETTING
DATABASE = QASETTING.get_config('DATABASE')

# IP地址列表
stock_ip_list           # 股票数据源IP列表
future_ip_list          # 期货数据源IP列表
info_ip_list           # 信息数据源IP列表
```

#### 参数常量 (QAParameter)

```python
# 市场类型
MARKET_TYPE.STOCK_CN      # 中国股票市场
MARKET_TYPE.FUTURE_CN     # 中国期货市场

# 订单方向
ORDER_DIRECTION.BUY       # 买入
ORDER_DIRECTION.SELL      # 卖出

# 订单状态
ORDER_STATUS.NEW          # 新订单
ORDER_STATUS.FILLED       # 已成交

# 数据频率
FREQUENCE.DAY            # 日线
FREQUENCE.MIN1           # 1分钟线
```

### 工具函数

#### 缓存管理 (QACache)

```python
# 缓存装饰器
@QA_util_cache
def expensive_function():
    # 耗时计算
    return result
```

#### 并行处理 (Parallelism)

```python
# 并行处理
from QUANTAXIS.QAUtil import Parallelism

# 创建并行任务
parallel = Parallelism(worker_num=4)
results = parallel.run(func, data_list)

# 线程并行
from QUANTAXIS.QAUtil import Parallelism_Thread
thread_parallel = Parallelism_Thread(worker_num=4)
```

#### 日志管理 (QALogs)

```python
# 日志记录
QA_util_log_info('信息日志')
QA_util_log_debug('调试日志')
QA_util_log_expection('异常日志')
```

#### 文件操作 (QAFile)

```python
# 文件MD5校验
md5_hash = QA_util_file_md5('file_path.txt')
```

#### 网络工具 (QAWebutil)

```python
# 网络连通性测试
is_connected = QA_util_web_ping('www.baidu.com')
```

#### 邮件发送 (QAMail)

```python
# 发送邮件
QA_util_send_mail(
    sender='sender@email.com',
    password='password',
    receiver='receiver@email.com',
    subject='主题',
    content='内容'
)
```

## 时间周期处理

### 时间索引生成 (QABar)

```python
# 生成分钟级索引
min_index = QA_util_make_min_index('09:30', '15:00', freq='1min')

# 生成小时级索引
hour_index = QA_util_make_hour_index('09:00', '15:00')

# 计算时间间隔
gap = QA_util_time_gap('09:30', '10:30', freq='min')
```

## 设计模式

### 单例模式 (QASingleton)

```python
from QUANTAXIS.QAUtil import singleton

@singleton
class ConfigManager:
    def __init__(self):
        self.config = {}
```

### 性能监控

```python
from QUANTAXIS.QAUtil import print_used_time

@print_used_time
def time_consuming_function():
    # 耗时操作
    pass
```

## 配置示例

### 数据库配置

```python
# MongoDB配置
MONGODB_CONFIG = {
    'ip': 'localhost',
    'port': 27017,
    'username': 'user',
    'password': 'password',
    'database': 'quantaxis'
}

# 初始化数据库连接
QA_util_mongo_initial()
```

### 日志配置

```python
# 配置日志级别和输出
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 最佳实践

1. **时间处理**
   - 统一使用QAUtil的时间函数处理交易时间
   - 注意时区处理，特别是期货夜盘时间

2. **数据转换**
   - 使用标准的转换函数确保数据格式一致
   - 注意数据类型检查和异常处理

3. **配置管理**
   - 集中管理系统配置，避免硬编码
   - 使用环境变量区分开发和生产环境

4. **性能优化**
   - 合理使用缓存减少重复计算
   - 使用并行处理提高数据处理效率

## 注意事项

1. **线程安全**: 在多线程环境下注意共享资源的线程安全
2. **内存管理**: 大数据处理时注意内存使用，及时释放不需要的对象
3. **异常处理**: 网络操作和文件操作要做好异常处理
4. **时区处理**: 处理跨时区数据时要特别注意时间转换

## 相关模块

- **QAData**: 使用QAUtil的时间和转换工具
- **QAFetch**: 依赖QAUtil的网络和配置工具
- **QASU**: 使用QAUtil的数据库和文件工具