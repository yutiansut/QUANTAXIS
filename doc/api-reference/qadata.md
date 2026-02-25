# QAData 模块文档

## 概述

QAData 是 QUANTAXIS 的核心数据结构模块，提供了标准化的金融数据容器和处理方法。该模块定义了多种数据结构来处理不同类型的金融数据，包括股票、期货、指数、加密货币等，同时提供数据重采样、复权处理、技术指标计算等功能。

## 模块架构

### 核心数据结构

1. **基础数据结构**
   - **base_datastruct.py**: 数据结构基类
   - **QADataStruct.py**: 主要数据结构实现
   - **paneldatastruct.py**: 面板数据结构

2. **专业数据结构**
   - **QABlockStruct.py**: 板块数据结构
   - **QAFinancialStruct.py**: 财务数据结构
   - **QAIndicatorStruct.py**: 指标数据结构
   - **QASeriesStruct.py**: 时间序列数据结构

3. **数据处理功能**
   - **data_resample.py**: 数据重采样
   - **data_fq.py**: 复权处理
   - **data_marketvalue.py**: 市值计算
   - **dsmethods.py**: 数据结构方法

## 主要数据结构类

### 1. 股票数据结构

#### QA_DataStruct_Stock_day (股票日线)
```python
from QUANTAXIS.QAData import QA_DataStruct_Stock_day

# 创建股票日线数据结构
stock_day = QA_DataStruct_Stock_day(data)

# 主要方法
stock_day.select_time('2020-01-01', '2020-12-31')  # 时间筛选
stock_day.select_code(['000001', '000002'])        # 代码筛选
stock_day.add_func(lambda x: x['close'] > 10)      # 条件筛选
stock_day.pivot('close')                           # 数据透视
stock_day.to_qfq()                                 # 前复权
stock_day.to_hfq()                                 # 后复权
```

#### QA_DataStruct_Stock_min (股票分钟线)
```python
from QUANTAXIS.QAData import QA_DataStruct_Stock_min

# 创建股票分钟数据结构
stock_min = QA_DataStruct_Stock_min(data)

# 数据重采样
stock_5min = stock_min.resample('5min')    # 重采样为5分钟
stock_hour = stock_min.resample('60min')   # 重采样为小时线
stock_day = stock_min.resample('D')        # 重采样为日线
```

### 2. 期货数据结构

#### QA_DataStruct_Future_day (期货日线)
```python
from QUANTAXIS.QAData import QA_DataStruct_Future_day

# 期货日线数据
future_day = QA_DataStruct_Future_day(data)

# 期货特有方法
future_day.get_contract_info()             # 获取合约信息
future_day.calculate_margin()              # 计算保证金
future_day.get_main_contract()             # 获取主力合约
```

#### QA_DataStruct_Future_min (期货分钟线)
```python
from QUANTAXIS.QAData import QA_DataStruct_Future_min

# 期货分钟数据
future_min = QA_DataStruct_Future_min(data)

# 期货分钟线特殊处理
future_min.resample_with_volume()          # 考虑成交量的重采样
future_min.handle_night_session()          # 夜盘时间处理
```

### 3. 指数数据结构

#### QA_DataStruct_Index_day/min (指数数据)
```python
from QUANTAXIS.QAData import QA_DataStruct_Index_day, QA_DataStruct_Index_min

# 指数日线和分钟线
index_day = QA_DataStruct_Index_day(data)
index_min = QA_DataStruct_Index_min(data)

# 指数特有功能
index_day.calculate_index_return()         # 计算指数收益率
index_day.get_constituents()               # 获取成分股
```

### 4. 加密货币数据结构

```python
from QUANTAXIS.QAData import (
    QA_DataStruct_CryptoCurrency_day,
    QA_DataStruct_CryptoCurrency_min
)

# 加密货币数据
crypto_day = QA_DataStruct_CryptoCurrency_day(data)
crypto_min = QA_DataStruct_CryptoCurrency_min(data)

# 24小时交易特殊处理
crypto_min.handle_24h_trading()            # 处理24小时交易
```

### 5. 实时数据结构

```python
from QUANTAXIS.QAData import QA_DataStruct_Stock_realtime

# 实时数据
realtime_data = QA_DataStruct_Stock_realtime(data)

# 实时数据特有方法
realtime_data.get_latest_price()           # 获取最新价格
realtime_data.get_bid_ask()                # 获取买卖盘
realtime_data.calculate_change()           # 计算涨跌幅
```

## 数据处理功能

### 1. 数据重采样 (data_resample.py)

```python
from QUANTAXIS.QAData.data_resample import (
    QA_data_min_resample,
    QA_data_day_resample,
    QA_data_tick_resample
)

# 分钟线重采样
def resample_minute_data():
    # 1分钟 -> 5分钟
    data_5min = QA_data_min_resample(data_1min, '5min')

    # 1分钟 -> 15分钟
    data_15min = QA_data_min_resample(data_1min, '15min')

    # 1分钟 -> 日线
    data_day = QA_data_min_to_day(data_1min)

    return data_5min, data_15min, data_day

# Tick数据重采样
def resample_tick_data():
    # Tick -> 1分钟
    data_1min = QA_data_tick_resample(tick_data, '1min')

    # Tick -> 5分钟
    data_5min = QA_data_tick_resample(tick_data, '5min')

    return data_1min, data_5min
```

### 2. 复权处理 (data_fq.py)

```python
from QUANTAXIS.QAData.data_fq import QA_data_stock_to_fq

# 前复权处理
def apply_forward_adjust():
    # 原始数据
    raw_data = get_stock_data('000001')

    # 前复权
    qfq_data = QA_data_stock_to_fq(raw_data, '000001', 'qfq')

    # 后复权
    hfq_data = QA_data_stock_to_fq(raw_data, '000001', 'hfq')

    return qfq_data, hfq_data
```

### 3. 市值计算 (data_marketvalue.py)

```python
from QUANTAXIS.QAData.data_marketvalue import QA_data_calc_marketvalue

# 计算市值
def calculate_market_value():
    # 计算个股市值
    market_value = QA_data_calc_marketvalue(
        price_data=stock_data,
        shares_data=shares_data
    )

    # 总市值和流通市值
    total_mv = market_value['total_market_value']
    float_mv = market_value['float_market_value']

    return total_mv, float_mv
```

## 面板数据结构 (QAPanelDataStruct)

### 多维数据处理

```python
from QUANTAXIS.QAData.paneldatastruct import QAPanelDataStruct

# 创建面板数据结构
panel_data = QAPanelDataStruct(data)

# 面板数据操作
panel_data.add_dimension('sector')          # 添加维度
panel_data.group_by('industry')             # 按行业分组
panel_data.apply_func(lambda x: x.mean())   # 应用函数
panel_data.cross_section('2020-01-01')     # 横截面数据
```

## 财务数据结构 (QAFinancialStruct)

```python
from QUANTAXIS.QAData.QAFinancialStruct import QA_DataStruct_Financial

# 财务数据结构
financial_data = QA_DataStruct_Financial(data)

# 财务指标计算
financial_data.calculate_roe()              # 计算ROE
financial_data.calculate_debt_ratio()       # 计算负债率
financial_data.get_financial_indicator()    # 获取财务指标
financial_data.quarter_growth()             # 季度增长率
```

## 指标数据结构 (QAIndicatorStruct)

```python
from QUANTAXIS.QAData.QAIndicatorStruct import QA_DataStruct_Indicators

# 技术指标数据结构
indicator_data = QA_DataStruct_Indicators(data)

# 指标计算和管理
indicator_data.add_indicator('MA', period=20)    # 添加移动平均
indicator_data.add_indicator('RSI', period=14)   # 添加RSI
indicator_data.calculate_all()                   # 计算所有指标
indicator_data.get_signals()                     # 获取交易信号
```

## 数据结构方法 (dsmethods.py)

### 包装器函数

```python
from QUANTAXIS.QAData.dsmethods import (
    QDS_StockDayWarpper,
    QDS_StockMinWarpper,
    QDS_IndexDayWarpper,
    concat,
    from_tushare
)

# 使用包装器快速创建数据结构
stock_day = QDS_StockDayWarpper(raw_data)
stock_min = QDS_StockMinWarpper(raw_data)
index_day = QDS_IndexDayWarpper(raw_data)

# 数据连接
combined_data = concat([data1, data2, data3])

# 从Tushare数据转换
qa_data = from_tushare(tushare_data)
```

## 使用示例

### 完整的数据处理流程

```python
import QUANTAXIS as QA

# 1. 获取原始数据
raw_data = QA.QA_fetch_stock_day_adv('000001', '2020-01-01', '2020-12-31')

# 2. 创建数据结构
stock_data = QA.QA_DataStruct_Stock_day(raw_data)

# 3. 数据处理
# 前复权
qfq_data = stock_data.to_qfq()

# 选择时间范围
filtered_data = qfq_data.select_time('2020-06-01', '2020-12-31')

# 添加技术指标
ma_data = filtered_data.add_func(lambda x: QA.MA(x['close'], 20))

# 4. 数据重采样
weekly_data = stock_data.resample('W')

# 5. 数据分析
returns = stock_data.add_func(lambda x: x['close'].pct_change())
volatility = returns.add_func(lambda x: x.rolling(20).std())

# 6. 数据导出
stock_data.to_csv('stock_data.csv')
stock_data.to_json('stock_data.json')
```

### 多标的数据处理

```python
# 获取多只股票数据
codes = ['000001', '000002', '000858']
multi_data = QA.QA_fetch_stock_day_adv(codes, '2020-01-01', '2020-12-31')

# 创建数据结构
stock_panel = QA.QA_DataStruct_Stock_day(multi_data)

# 按代码分组处理
for code in codes:
    single_stock = stock_panel.select_code(code)
    # 进行单只股票的分析
    ma20 = single_stock.add_func(lambda x: QA.MA(x['close'], 20))

# 横截面分析
latest_data = stock_panel.tail(1)  # 最新数据
cross_section = latest_data.pivot('close')  # 创建横截面
```

## 性能优化

### 1. 内存优化

```python
# 使用生成器减少内存占用
def process_large_dataset(data):
    for chunk in data.chunk(10000):  # 分块处理
        yield process_chunk(chunk)

# 及时释放不需要的数据
del unused_data
```

### 2. 计算优化

```python
# 使用向量化操作
data['returns'] = data['close'].pct_change()  # 向量化计算收益率

# 使用缓存
@lru_cache(maxsize=128)
def cached_calculation(data_hash):
    return expensive_calculation(data)
```

## 最佳实践

1. **数据一致性**: 确保所有数据结构使用相同的时间索引格式
2. **内存管理**: 处理大数据集时注意内存使用，及时释放不需要的对象
3. **类型检查**: 在数据处理前进行数据类型和格式检查
4. **异常处理**: 对数据缺失和异常值进行适当处理

## 相关模块

- **QAFetch**: 提供原始数据给QAData处理
- **QAIndicator**: 技术指标计算，与QAData数据结构集成
- **QAUtil**: 提供时间处理和数据转换工具
- **QAStrategy**: 使用QAData结构进行策略回测