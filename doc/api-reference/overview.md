# QUANTAXIS API参考文档

> 📚 **完整API参考** - QUANTAXIS 2.1.0核心接口文档
>
> **版本**: v2.1.0-alpha2 | **更新**: 2025-10-25

---

## 📋 目录

- [数据获取API](#数据获取api)
- [数据结构API](#数据结构api)
- [QIFI账户API](#qifi账户api)
- [QARSBridge API](#qarsbridge-api)
- [QADataBridge API](#qadatabridge-api)
- [回测框架API](#回测框架api)
- [工具函数API](#工具函数api)

---

## 📊 数据获取API

### 股票数据

#### `QA_fetch_get_stock_day(code, start, end)`

获取股票日线数据

**参数**:
- `code` (str): 股票代码，如'000001'
- `start` (str): 开始日期，格式'YYYY-MM-DD'
- `end` (str): 结束日期，格式'YYYY-MM-DD'

**返回**:
- `pd.DataFrame`: 包含open, high, low, close, volume等字段

**示例**:
```python
df = QA.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-01-31')
```

---

#### `QA_fetch_get_stock_min(code, start, end, frequence='1min')`

获取股票分钟线数据

**参数**:
- `code` (str): 股票代码
- `start` (str): 开始时间
- `end` (str): 结束时间
- `frequence` (str): 频率，'1min'/'5min'/'15min'/'30min'/'60min'

**返回**:
- `pd.DataFrame`: 分钟线数据

---

#### `QA_fetch_get_stock_list()`

获取所有股票列表

**返回**:
- `pd.DataFrame`: 股票代码和名称列表

---

### 期货数据

#### `QA_fetch_get_future_day(code, start, end)`

获取期货日线数据

**参数**:
- `code` (str): 期货合约代码，如'IF2512'
- `start` (str): 开始日期
- `end` (str): 结束日期

**返回**:
- `pd.DataFrame`: 期货日线数据

---

#### `QA_fetch_get_future_min(code, start, end, frequence='1min')`

获取期货分钟线数据

**参数同股票分钟线**

---

### 指数数据

#### `QA_fetch_get_index_day(code, start, end)`

获取指数日线数据

**参数**:
- `code` (str): 指数代码，如'000001'（上证指数）
- `start` (str): 开始日期
- `end` (str): 结束日期

---

## 📈 数据结构API

### QA_DataStruct_Stock_day

股票日线数据结构

**初始化**:
```python
data = QA.QA_DataStruct_Stock_day(df)
```

**属性**:
- `data` (pd.DataFrame): 原始数据
- `index` (pd.Index): 时间索引
- `code` (list): 股票代码列表

**方法**:
- `select_time(start, end)`: 选择时间范围
- `select_code(code)`: 选择特定股票
- `pivot(column)`: 数据透视
- `add_func(func)`: 添加自定义函数

**示例**:
```python
data = QA.QA_DataStruct_Stock_day(df)

# 选择时间范围
data_jan = data.select_time('2024-01-01', '2024-01-31')

# 选择特定股票
data_000001 = data.select_code('000001')

# 计算收益率
data.data['returns'] = data.data['close'].pct_change()
```

---

### QA_DataStruct_Future_day

期货日线数据结构

**用法同股票数据结构**

---

### QA_DataStruct_Stock_min

股票分钟线数据结构

**额外方法**:
- `resample(frequence)`: 重采样到不同频率

---

## 🏦 QIFI账户API

### QIFI_Account

统一账户接口，支持股票/期货/期权

**初始化**:
```python
account = QA.QIFI_Account(
    username="account_name",
    password="password",
    model="stock",  # 或 "future"
    init_cash=100000
)
```

**参数**:
- `username` (str): 账户名称
- `password` (str): 账户密码
- `model` (str): 账户类型，'stock'或'future'
- `init_cash` (float): 初始资金

**属性**:
- `cash` (float): 可用资金
- `balance` (float): 总资产
- `positions` (dict): 持仓字典
- `orders` (dict): 订单字典
- `trades` (dict): 成交字典

**方法**:

#### `receive_simpledeal(order_dict)`

接收简单成交

**参数**:
```python
order_dict = {
    'code': '000001',
    'price': 10.5,
    'amount': 1000,
    'datetime': '2024-01-15',
    'towards': 'buy'  # 或 'sell'
}
```

#### `buy(code, price, amount, datetime=None)`

买入（股票）

#### `sell(code, price, amount, datetime=None)`

卖出（股票）

#### `open_long(code, price, amount, datetime=None)`

开多（期货）

#### `close_long(code, price, amount, datetime=None)`

平多（期货）

**示例**:
```python
# 创建账户
account = QA.QIFI_Account("test", "test", "stock", 100000)

# 买入
account.receive_simpledeal({
    'code': '000001',
    'price': 10.5,
    'amount': 1000,
    'datetime': '2024-01-15',
    'towards': 'buy'
})

# 查看持仓
print(account.positions)

# 卖出
account.receive_simpledeal({
    'code': '000001',
    'price': 11.0,
    'amount': 1000,
    'datetime': '2024-01-20',
    'towards': 'sell'
})

# 查看盈亏
print(f"总盈亏: {account.balance - account.init_cash}")
```

---

## ⚡ QARSBridge API

### has_qars_support()

检查QARS2是否可用

**返回**:
- `bool`: True表示QARS2已安装

**示例**:
```python
from QUANTAXIS.QARSBridge import has_qars_support

if has_qars_support():
    print("✅ QARS2可用")
```

---

### QARSAccount

Rust高性能账户（100x加速）

**初始化**:
```python
from QUANTAXIS.QARSBridge import QARSAccount

account = QARSAccount(
    account_cookie="rust_account",
    init_cash=100000.0,
    commission_rate=0.0003
)
```

**参数**:
- `account_cookie` (str): 账户标识
- `init_cash` (float): 初始资金
- `commission_rate` (float): 佣金费率，默认0.0003

**方法**:

#### `buy(code, price, datetime, amount)`

买入

**参数**:
- `code` (str): 股票代码
- `price` (float): 价格
- `datetime` (str): 时间
- `amount` (int): 数量

**返回**:
- `str`: 订单ID

#### `sell(code, price, datetime, amount)`

卖出（参数同buy）

#### `get_position(code)`

获取持仓

**返回**:
- `dict`: 持仓信息

**示例**:
```python
# 创建Rust账户
account = QARSAccount("test", init_cash=100000.0)

# 买入（100x加速）
order_id = account.buy("000001", 10.5, "2024-01-15", 1000)

# 查看持仓
position = account.get_position("000001")
print(f"持仓数量: {position['volume']}")
print(f"成本价: {position['cost_price']}")

# 卖出
account.sell("000001", 11.0, "2024-01-20", 1000)

# 查看盈亏
print(f"现金余额: {account.cash}")
```

---

### QARSBacktest

Rust高性能回测引擎（10x加速）

**初始化**:
```python
from QUANTAXIS.QARSBridge import QARSBacktest

backtest = QARSBacktest(
    code="000001",
    start_date="2024-01-01",
    end_date="2024-01-31",
    init_cash=100000.0
)
```

**方法**:

#### `run()`

运行回测

**返回**:
- `dict`: 回测结果

**示例**:
```python
# 创建回测
backtest = QARSBacktest("000001", "2024-01-01", "2024-01-31", 100000.0)

# 运行回测（10x加速）
result = backtest.run()

print(f"总收益率: {result['total_return']:.2%}")
print(f"夏普比率: {result['sharpe_ratio']:.2f}")
print(f"最大回撤: {result['max_drawdown']:.2%}")
```

---

## 🔄 QADataBridge API

### has_dataswap_support()

检查QADataSwap是否可用

**返回**:
- `bool`: True表示QADataSwap已安装

---

### convert_pandas_to_polars(df, preserve_index=False)

Pandas转Polars（零拷贝，2.5x加速）

**参数**:
- `df` (pd.DataFrame): Pandas DataFrame
- `preserve_index` (bool): 是否保留索引

**返回**:
- `pl.DataFrame`: Polars DataFrame

**示例**:
```python
from QUANTAXIS.QADataBridge import convert_pandas_to_polars
import pandas as pd

df_pandas = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df_polars = convert_pandas_to_polars(df_pandas)  # 2.5x加速
```

---

### convert_polars_to_pandas(df, use_pyarrow_extension_array=False)

Polars转Pandas（零拷贝）

**参数**:
- `df` (pl.DataFrame): Polars DataFrame
- `use_pyarrow_extension_array` (bool): 使用PyArrow扩展数组

**返回**:
- `pd.DataFrame`: Pandas DataFrame

---

### SharedMemoryWriter

共享内存写入器（7x加速）

**初始化**:
```python
from QUANTAXIS.QADataBridge import SharedMemoryWriter

writer = SharedMemoryWriter(
    name="market_data",
    size_mb=50,
    buffer_count=3
)
```

**方法**:

#### `write(df)`

写入DataFrame

**参数**:
- `df` (pd.DataFrame | pl.DataFrame): 数据

**返回**:
- `bool`: 是否成功

#### `get_stats()`

获取统计信息

**返回**:
- `dict`: 统计数据

**示例**:
```python
# 创建写入器
writer = SharedMemoryWriter("data", size_mb=50)

# 写入数据（7x加速）
import polars as pl
df = pl.DataFrame({'price': [10.5, 20.3], 'volume': [1000, 2000]})
writer.write(df)

# 获取统计
stats = writer.get_stats()
print(stats)

# 关闭
writer.close()
```

---

### SharedMemoryReader

共享内存读取器

**初始化**:
```python
from QUANTAXIS.QADataBridge import SharedMemoryReader

reader = SharedMemoryReader(name="market_data")
```

**方法**:

#### `read(timeout_ms=5000, to_pandas=False)`

读取DataFrame

**参数**:
- `timeout_ms` (int): 超时时间（毫秒）
- `to_pandas` (bool): 是否转换为Pandas

**返回**:
- `pl.DataFrame | pd.DataFrame | None`: 数据或None（超时）

**示例**:
```python
# 创建读取器
reader = SharedMemoryReader("data")

# 读取数据
df = reader.read(timeout_ms=5000, to_pandas=True)

if df is not None:
    print(f"读取到{len(df)}行数据")

reader.close()
```

---

## 🔄 回测框架API

### QAStrategyCtaBase

CTA策略基类

**继承示例**:
```python
from QUANTAXIS.QAStrategy import QAStrategyCtaBase

class MyStrategy(QAStrategyCtaBase):
    def __init__(self):
        super().__init__()
        self.ma_period = 20

    def on_bar(self, bar):
        """每根K线回调"""
        ma = bar['close'].rolling(self.ma_period).mean().iloc[-1]
        current_price = bar['close'].iloc[-1]

        if current_price > ma:
            self.buy(bar['code'].iloc[-1], current_price, 100)
        else:
            self.sell(bar['code'].iloc[-1], current_price, 100)

    def on_order(self, order):
        """订单回调"""
        print(f"订单: {order}")

    def on_trade(self, trade):
        """成交回调"""
        print(f"成交: {trade}")
```

---

## 🛠️ 工具函数API

### 日期时间

#### `QA_util_get_trade_date(start, end)`

获取交易日列表

**参数**:
- `start` (str): 开始日期
- `end` (str): 结束日期

**返回**:
- `list`: 交易日列表

---

#### `QA_util_if_trade(date)`

判断是否交易日

**参数**:
- `date` (str): 日期

**返回**:
- `bool`: 是否交易日

---

### 数据处理

#### `QA_data_tick_resample(tick_data, type_='1min')`

Tick数据重采样

**参数**:
- `tick_data` (pd.DataFrame): Tick数据
- `type_` (str): 目标频率

**返回**:
- `pd.DataFrame`: 重采样后的数据

---

#### `QA_data_min_resample(min_data, type_='5min')`

分钟线重采样

---

### MongoDB操作

#### `QA_util_mongo_initial()`

初始化MongoDB连接

---

#### `QA_util_mongo_status()`

检查MongoDB状态

**返回**:
- `bool`: 是否连接成功

---

## 📊 因子分析API

### QASingleFactor_DailyBase

单因子分析基类

**示例**:
```python
from QUANTAXIS.QAFactor import QASingleFactor_DailyBase

class MyFactor(QASingleFactor_DailyBase):
    def calculate(self, data):
        """计算因子值"""
        return data['close'] / data['close'].shift(20) - 1

factor = MyFactor()
result = factor.backtest(data)
```

---

## 🔢 常用常量

### MARKET_TYPE

市场类型

```python
from QUANTAXIS.QAUtil import MARKET_TYPE

MARKET_TYPE.STOCK_CN        # 股票市场
MARKET_TYPE.FUTURE_CN       # 期货市场
MARKET_TYPE.INDEX_CN        # 指数市场
MARKET_TYPE.OPTION_CN       # 期权市场
```

---

### FREQUENCE

数据频率

```python
from QUANTAXIS.QAUtil import FREQUENCE

FREQUENCE.TICK              # Tick级别
FREQUENCE.ONE_MIN           # 1分钟
FREQUENCE.FIVE_MIN          # 5分钟
FREQUENCE.FIFTEEN_MIN       # 15分钟
FREQUENCE.THIRTY_MIN        # 30分钟
FREQUENCE.HOUR              # 小时
FREQUENCE.DAY               # 日线
FREQUENCE.WEEK              # 周线
FREQUENCE.MONTH             # 月线
```

---

### ORDER_DIRECTION

订单方向

```python
from QUANTAXIS.QAUtil import ORDER_DIRECTION

ORDER_DIRECTION.BUY         # 买入
ORDER_DIRECTION.SELL        # 卖出
ORDER_DIRECTION.BUY_OPEN    # 买开（期货）
ORDER_DIRECTION.SELL_CLOSE  # 卖平（期货）
```

---

## 📝 使用建议

### 性能优化

1. **使用Rust组件**（100x加速）
```python
from QUANTAXIS.QARSBridge import QARSAccount
account = QARSAccount(...)  # 替代 QIFI_Account
```

2. **使用零拷贝转换**（2-5x加速）
```python
from QUANTAXIS.QADataBridge import convert_pandas_to_polars
df_polars = convert_pandas_to_polars(df_pandas)
```

3. **使用共享内存**（7x加速）
```python
from QUANTAXIS.QADataBridge import SharedMemoryWriter, SharedMemoryReader
```

### 错误处理

```python
try:
    df = QA.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-01-31')
except Exception as e:
    print(f"数据获取失败: {e}")
```

### 批量操作

```python
# 批量获取数据
codes = ['000001', '000002', '600000']
data_list = [
    QA.QA_fetch_get_stock_day(code, '2024-01-01', '2024-01-31')
    for code in codes
]
```

---

## 🔗 相关文档

- [快速入门](./QUICKSTART.md)
- [安装指南](./INSTALLATION.md)
- [QARSBridge文档](./QUANTAXIS/QARSBridge/README.md)
- [QADataBridge文档](./QUANTAXIS/QADataBridge/README.md)
- [最佳实践](./BEST_PRACTICES.md)

---

**@yutiansut @quantaxis**
**最后更新**: 2025-10-25
