# QAFetch 模块文档

## 概述

QAFetch 是 QUANTAXIS 的数据获取核心模块，提供了统一的接口来获取多种金融数据源的数据，包括股票、期货、期权、数字货币等多个市场的实时和历史数据。

## 模块架构

### 核心组件

1. **统一接口层** (`__init__.py`)
   - 提供统一的数据获取API
   - 支持多数据源切换
   - 标准化数据输出格式

2. **数据源适配器**
   - **QATdx.py**: 通达信数据源接口
   - **QATushare.py**: Tushare数据源接口
   - **QAThs.py**: 同花顺数据源接口
   - **QAClickhouse.py**: ClickHouse数据库接口
   - **QAEastMoney.py**: 东方财富数据源
   - **QAHexun.py**: 和讯数据源

3. **加密货币交易所接口**
   - **QAbinance.py**: 币安交易所
   - **QAhuobi.py**: 火币交易所
   - **QABitmex.py**: BitMEX交易所
   - **QABitfinex.py**: Bitfinex交易所
   - **QAOKEx.py**: OKEx交易所

4. **查询引擎**
   - **QAQuery.py**: 基础查询功能
   - **QAQuery_Advance.py**: 高级查询功能
   - **QAQuery_Async.py**: 异步查询支持

## 主要功能

### 股票数据获取

```python
# 获取股票日线数据
QA_fetch_get_stock_day(package, code, start, end, if_fq='00', level='day', type_='pd')

# 获取股票分钟线数据
QA_fetch_get_stock_min(package, code, start, end, level='1min')

# 获取股票实时数据
QA_fetch_get_stock_realtime(package, code)

# 获取股票交易明细
QA_fetch_get_stock_transaction(package, code, start, end, retry=2)
```

### 指数数据获取

```python
# 获取指数日线数据
QA_fetch_get_index_day(package, code, start, end, level='day')

# 获取指数分钟线数据
QA_fetch_get_index_min(package, code, start, end, level='1min')

# 获取指数实时数据
QA_fetch_get_index_realtime(package, code)
```

### 期货数据获取

```python
# 获取期货日线数据
QA_fetch_get_future_day(package, code, start, end, frequence='day')

# 获取期货分钟线数据
QA_fetch_get_future_min(package, code, start, end, frequence='1min')

# 获取期货实时数据
QA_fetch_get_future_realtime(package, code)
```

### 数据列表获取

```python
# 获取股票列表
QA_fetch_get_stock_list(package, type_='stock')

# 获取期货列表
QA_fetch_get_future_list(package)

# 获取期权列表
QA_fetch_get_option_list(package)

# 获取指数列表
QA_fetch_get_index_list(package)
```

## 数据源支持

### 主要数据源

1. **TDX (通达信)**
   - 支持：股票、指数、期货、期权、港股、美股
   - 优势：数据全面，更新及时
   - 使用：`package='tdx'` 或 `package='pytdx'`

2. **Tushare**
   - 支持：股票、指数、财务数据
   - 优势：数据质量高，接口稳定
   - 使用：`package='tushare'` 或 `package='ts'`

3. **同花顺 (THS)**
   - 支持：股票、指数
   - 优势：专业金融数据
   - 使用：`package='ths'` 或 `package='THS'`

4. **东方财富**
   - 支持：股票、基金数据
   - 使用：通过 QAEastMoney 模块

### 数字货币交易所

- **Binance**: 全球最大加密货币交易所
- **Huobi**: 火币全球站
- **OKEx**: OKEx交易所
- **BitMEX**: 专业衍生品交易所
- **Bitfinex**: 专业交易平台

## 使用示例

### 基础用法

```python
import QUANTAXIS as QA

# 获取股票数据
data = QA.QA_fetch_get_stock_day('tdx', '000001', '2020-01-01', '2020-12-31')

# 获取实时数据
realtime_data = QA.QA_fetch_get_stock_realtime('tdx', '000001')

# 获取股票列表
stock_list = QA.QA_fetch_get_stock_list('tdx')
```

### 多数据源使用

```python
# 使用 use() 函数切换数据源
tdx_engine = QA.QAFetch.use('tdx')
tushare_engine = QA.QAFetch.use('tushare')

# 直接使用特定数据源
import QUANTAXIS.QAFetch.QATdx as QATdx
data = QATdx.QA_fetch_get_stock_day('000001', '2020-01-01', '2020-12-31')
```

## 配置参数

### 复权处理 (if_fq)
- `'00'`: 不复权
- `'01'`: 前复权
- `'02'`: 后复权

### 数据级别 (level/frequence)
- `'day'`: 日线
- `'1min'`: 1分钟线
- `'5min'`: 5分钟线
- `'15min'`: 15分钟线
- `'30min'`: 30分钟线
- `'60min'`: 60分钟线

### 数据类型 (type_)
- `'pd'`: pandas DataFrame格式
- `'json'`: JSON格式
- `'numpy'`: numpy数组格式

## 错误处理

```python
try:
    data = QA.QA_fetch_get_stock_day('tdx', '000001', '2020-01-01', '2020-12-31')
    if data is None or data.empty:
        print("数据获取失败或为空")
except Exception as e:
    print(f"数据获取异常: {e}")
```

## 性能优化

1. **批量获取**: 尽量批量获取数据而不是逐个获取
2. **缓存机制**: 对频繁访问的数据进行缓存
3. **异步获取**: 使用 QAQuery_Async 进行异步数据获取
4. **数据分片**: 对大量数据进行分片处理

## 注意事项

1. **网络依赖**: 大部分数据源需要网络连接
2. **频率限制**: 各数据源可能有API调用频率限制
3. **数据延迟**: 免费数据源可能有数据延迟
4. **格式统一**: 不同数据源返回的数据格式可能略有差异

## 扩展开发

要添加新的数据源：

1. 创建新的数据源模块文件
2. 实现标准的数据获取接口
3. 在 `__init__.py` 中注册新的数据源
4. 在 `use()` 函数中添加对应的映射

## 相关模块

- **QAData**: 数据结构化处理
- **QASU**: 数据存储和更新
- **QAUtil**: 工具函数支持