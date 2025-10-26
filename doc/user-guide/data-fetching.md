# 数据获取

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本章节介绍如何使用QUANTAXIS的QAFetch模块获取各类金融数据。QAFetch提供统一的数据获取接口，支持多种数据源和多种资产类型。

---

## 📚 模块概览

QAFetch是QUANTAXIS的数据获取模块，具有以下特点：

### ✨ 核心特性

- **多数据源支持**: TDX（通达信）、Tushare、同花顺、东方财富等
- **统一接口**: 所有数据源使用相同的API调用方式
- **多资产覆盖**: 股票、期货、期权、数字货币、港股、美股
- **多时间周期**: 日线、分钟线、Tick、实时行情
- **灵活格式**: 支持pandas DataFrame、JSON、NumPy等格式
- **容错机制**: 数据源切换和自动重试

### 🔧 主要组件

```python
from QUANTAXIS.QAFetch import (
    QAQuery,        # MongoDB查询接口
    QATdx,          # 通达信数据源
    QATushare,      # Tushare数据源
    QAfinancial,    # 财务数据
)
```

---

## 📈 股票数据获取

### 1. 股票日线数据

#### 从MongoDB查询（推荐）

```python
import QUANTAXIS as QA
from datetime import datetime

# 查询单只股票日线数据
data = QA.QA_fetch_stock_day(
    code='000001',           # 股票代码
    start='2020-01-01',      # 开始日期
    end='2024-12-31',        # 结束日期
    format='pd',             # 返回格式: 'pd'(DataFrame), 'json', 'numpy'
    frequence='day'          # 频率: 'day', 'week', 'month'
)

print(data.head())
#              code        date    open   high    low  close     volume
# 0  000001  2020-01-02  16.02  16.27  15.83  16.01  593058.25
# ...

# 查询多只股票
data = QA.QA_fetch_stock_day(
    code=['000001', '000002', '600000'],
    start='2024-01-01',
    end='2024-12-31'
)

# 查询全市场某日数据
data = QA.QA_fetch_stock_full(
    date='2024-10-25',
    format='pd'
)
```

#### 从数据源直接获取

```python
# 使用通达信数据源
data = QA.QA_fetch_get_stock_day(
    package='tdx',           # 数据源: 'tdx', 'tushare', 'ths'
    code='000001',
    start='2020-01-01',
    end='2024-12-31',
    if_fq='00',              # 复权: '00'不复权, '01'前复权, '02'后复权
    level='day'              # 周期: 'day', 'week', 'month'
)

# 使用Tushare数据源
data = QA.QA_fetch_get_stock_day(
    package='tushare',
    code='000001',
    start='2020-01-01',
    end='2024-12-31',
    if_fq='01',              # 前复权
    type_='pd'               # 返回类型
)
```

### 2. 股票分钟线数据

```python
# 从MongoDB查询
data = QA.QA_fetch_stock_min(
    code='000001',
    start='2024-10-01',
    end='2024-10-25',
    format='pd',
    frequence='1min'         # '1min', '5min', '15min', '30min', '60min'
)

# 从通达信获取
data = QA.QA_fetch_get_stock_min(
    package='tdx',
    code='000001',
    start='2024-10-01 09:30:00',
    end='2024-10-25 15:00:00',
    level='5min'
)

# 查看数据结构
print(data.head())
#              code            datetime    open   high    low  close   volume
# 0  000001  2024-10-01 09:30:00  16.02  16.10  15.98  16.05  1250000
# ...
```

### 3. 实时行情

```python
# 获取单只股票实时行情
realtime = QA.QA_fetch_get_stock_realtime(
    package='tdx',
    code='000001'
)

print(realtime)
# {
#     'code': '000001',
#     'name': '平安银行',
#     'price': 16.05,
#     'open': 16.02,
#     'high': 16.27,
#     'low': 15.98,
#     'bid1': 16.04,
#     'ask1': 16.05,
#     'volume': 593058.25,
#     'amount': 9523456.78,
#     ...
# }

# 批量获取多只股票实时行情
codes = ['000001', '000002', '600000', '600036']
for code in codes:
    data = QA.QA_fetch_get_stock_realtime('tdx', code)
    print(f"{data['code']} {data['name']}: {data['price']}")
```

### 4. Tick数据（逐笔成交）

```python
# 获取历史Tick数据
tick_data = QA.QA_fetch_stock_transaction(
    code='000001',
    start='2024-10-25',
    end='2024-10-25',
    format='pd'
)

print(tick_data.head())
#              code                 datetime  price  volume  type
# 0  000001  2024-10-25 09:30:03  16.02    5000    买盘
# 1  000001  2024-10-25 09:30:05  16.03    3200    卖盘
# ...

# 获取实时Tick
realtime_tick = QA.QA_fetch_get_stock_transaction_realtime(
    package='tdx',
    code='000001'
)
```

### 5. 复权数据

```python
# 获取除权除息信息
xdxr = QA.QA_fetch_stock_xdxr(
    code='000001',
    format='pd'
)

print(xdxr)
#        code        date  category  fenhong  peigu  ...
# 0  000001  2023-06-15        DR     0.25    0.0  ...
# 1  000001  2022-06-16        DR     0.22    0.0  ...

# 获取前复权数据
adj_data = QA.QA_fetch_stock_adj(
    code='000001',
    format='pd'
)

# 应用复权
import QUANTAXIS as QA
data = QA.QA_fetch_stock_day('000001', '2020-01-01', '2024-12-31')
adj_data_qfq = QA.QA_data_stock_to_qfq(data)  # 前复权
adj_data_hfq = QA.QA_data_stock_to_hfq(data)  # 后复权
```

### 6. 股票列表和基本信息

```python
# 获取股票列表
stock_list = QA.QA_fetch_stock_list(format='pd')
print(stock_list.head())
#        code      name    sse  sec  ...
# 0  000001  平安银行     sz  stock  ...
# 1  000002  万科A       sz  stock  ...

# 获取ETF列表
etf_list = QA.QA_fetch_etf_list()

# 获取股票基本信息
info = QA.QA_fetch_stock_info(
    code='000001',
    format='pd'
)

print(info)
# 包含：上市日期、发行价格、总股本、流通股本等

# 获取股票名称
name = QA.QA_fetch_stock_name(code='000001')
print(name)  # '平安银行'

# 获取股票上市日期
list_date = QA.QA_fetch_stock_to_market_date(stock_code='000001')
print(list_date)  # '1991-04-03'
```

### 7. 板块数据

```python
# 获取股票所属板块
block = QA.QA_fetch_stock_block(format='pd')

print(block.head())
#        code  blockname  ...
# 0  000001      银行      ...
# 1  000001    深圳本地    ...
```

---

## 📊 指数数据获取

```python
# 指数日线数据
index_data = QA.QA_fetch_index_day(
    code='000001',           # 上证指数
    start='2020-01-01',
    end='2024-12-31',
    format='pd'
)

# 指数分钟线
index_min = QA.QA_fetch_index_min(
    code='000001',
    start='2024-10-01',
    end='2024-10-25',
    frequence='5min'
)

# 指数实时行情
index_realtime = QA.QA_fetch_get_index_realtime(
    package='tdx',
    code='000001'
)

# 获取指数列表
index_list = QA.QA_fetch_index_list()
print(index_list.head())
#        code      name
# 0  000001  上证指数
# 1  399001  深证成指
# 2  399006  创业板指

# 指数名称查询
name = QA.QA_fetch_index_name(code='000001')
print(name)  # '上证指数'
```

---

## 🌾 期货数据获取

### 1. 期货日线数据

```python
# 从MongoDB查询
data = QA.QA_fetch_future_day(
    code='RB2501',          # 期货合约代码
    start='2024-01-01',
    end='2024-12-31',
    format='pd',
    frequence='day'
)

# 从通达信获取
data = QA.QA_fetch_get_future_day(
    package='tdx',
    code='RB2501',
    start='2024-01-01',
    end='2024-12-31',
    frequence='day'
)

print(data.head())
#        code        date    open   high    low  close  ...
# 0  RB2501  2024-01-02  3520.0  3550  3510  3535  ...
```

### 2. 期货分钟线数据

```python
# 查询分钟线
data = QA.QA_fetch_future_min(
    code='RB2501',
    start='2024-10-01',
    end='2024-10-25',
    frequence='5min'         # '1min', '5min', '15min', '30min', '60min'
)

# 从通达信获取
data = QA.QA_fetch_get_future_min(
    package='tdx',
    code='RB2501',
    start='2024-10-01 09:00:00',
    end='2024-10-25 15:00:00',
    frequence='1min'
)
```

### 3. 期货实时行情

```python
# 获取实时行情
realtime = QA.QA_fetch_get_future_realtime(
    package='tdx',
    code='RB2501'
)

print(realtime)
# {
#     'code': 'RB2501',
#     'name': '螺纹钢2501',
#     'price': 3535.0,
#     'open': 3520.0,
#     'high': 3550.0,
#     'low': 3510.0,
#     'bid1': 3534.0,
#     'ask1': 3535.0,
#     ...
# }
```

### 4. 期货Tick数据

```python
# 历史Tick
tick_data = QA.QA_fetch_get_future_transaction(
    package='tdx',
    code='RB2501',
    start='2024-10-25',
    end='2024-10-25'
)

# 实时Tick
realtime_tick = QA.QA_fetch_get_future_transaction_realtime(
    package='tdx',
    code='RB2501'
)

# CTP Tick数据（需要CTP连接）
ctp_tick = QA.QA_fetch_ctp_tick(
    code='rb2501',
    start='2024-10-25 09:00:00',
    end='2024-10-25 15:00:00'
)
```

### 5. 期货合约列表

```python
# 获取期货合约列表
future_list = QA.QA_fetch_future_list()

print(future_list.head())
#        code      name   ...
# 0  RB2501  螺纹钢2501  ...
# 1  RB2502  螺纹钢2502  ...

# 使用通达信获取
future_list = QA.QA_fetch_get_future_list(package='tdx')
```

---

## 🎯 期权数据获取

期权数据获取与期货类似，使用相同的接口：

```python
# 期权日线数据
data = QA.QA_fetch_get_option_day(
    package='tdx',
    code='10004140',         # 期权合约代码
    start='2024-01-01',
    end='2024-12-31',
    frequence='day'
)

# 期权分钟线
data = QA.QA_fetch_get_option_min(
    package='tdx',
    code='10004140',
    start='2024-10-01',
    end='2024-10-25',
    frequence='5min'
)

# 期权合约列表
option_list = QA.QA_fetch_get_option_list(package='tdx')

print(option_list.head())
#          code        name  ...
# 0  10004140  50ETF购10月4000  ...
```

---

## 🪙 加密货币数据获取

QUANTAXIS支持多个主流交易所的加密货币数据。

### 1. 支持的交易所

```python
from QUANTAXIS.QAFetch import (
    QAbinance,      # Binance
    QAhuobi,        # Huobi
    QABitmex,       # Bitmex
    QAOKEx,         # OKEx
    QABitfinex,     # Bitfinex
)
```

### 2. 加密货币日线数据

```python
# 从MongoDB查询
data = QA.QA_fetch_cryptocurrency_day(
    code='btcusdt',          # 交易对
    start='2020-01-01',
    end='2024-12-31',
    format='pd'
)

print(data.head())
#       code        date      open     high      low    close     volume
# 0  btcusdt  2020-01-02  7200.5  7350.0  7180.0  7320.5  12500.25
```

### 3. 加密货币分钟线

```python
data = QA.QA_fetch_cryptocurrency_min(
    code='btcusdt',
    start='2024-10-01',
    end='2024-10-25',
    frequence='1min'         # '1min', '5min', '15min', '30min', '1hour'
)
```

### 4. 获取加密货币列表

```python
# 获取支持的加密货币列表
crypto_list = QA.QA_fetch_cryptocurrency_list(
    market='binance'         # 'binance', 'huobi', 'okex'
)

print(crypto_list)
# ['btcusdt', 'ethusdt', 'bnbusdt', ...]
```

### 5. 实时行情（Websocket）

```python
# Binance实时行情
from QUANTAXIS.QAFetch import QAbinance

client = QAbinance.QA_fetch_binance_realtime()
# 订阅实时行情
client.subscribe(['btcusdt', 'ethusdt'])

# Huobi实时行情
from QUANTAXIS.QAFetch import QAhuobi_realtime

huobi_client = QAhuobi_realtime.QAHuobi_Websocket()
huobi_client.sub_market_depth('btcusdt')
```

---

## 🌏 港股美股数据获取

```python
# 港股日线
hk_data = QA.QA_fetch_get_hkstock_day(
    package='tdx',
    code='00700',            # 腾讯控股
    start='2020-01-01',
    end='2024-12-31',
    frequence='day'
)

# 港股分钟线
hk_min = QA.QA_fetch_get_hkstock_min(
    package='tdx',
    code='00700',
    start='2024-10-01',
    end='2024-10-25',
    frequence='5min'
)

# 美股日线
us_data = QA.QA_fetch_get_usstock_day(
    package='tdx',
    code='AAPL',             # 苹果
    start='2020-01-01',
    end='2024-12-31',
    frequence='day'
)

# 美股分钟线
us_min = QA.QA_fetch_get_usstock_min(
    package='tdx',
    code='AAPL',
    start='2024-10-01',
    end='2024-10-25',
    frequence='5min'
)

# 港股列表
hk_list = QA.QA_fetch_get_hkstock_list(package='tdx')

# 美股列表
us_list = QA.QA_fetch_get_usstock_list(package='tdx')
```

---

## 💰 财务数据获取

```python
from QUANTAXIS.QAFetch import QAfinancial

# 获取财务报表
financial = QA.QA_fetch_financial_report(
    code='000001',
    report_date='2024-09-30',  # 报告期
    ltype='EN'                  # 'EN'英文字段, 'CN'中文字段
)

print(financial)
# 包含：资产负债表、利润表、现金流量表

# 财务日历（预告、快报等）
calendar = QA.QA_fetch_stock_financial_calendar(
    start='2024-01-01',
    end='2024-12-31'
)

# 股息率数据
divyield = QA.QA_fetch_stock_divyield(
    code='000001'
)
```

---

## 🔄 数据源切换

QAFetch支持在多个数据源之间灵活切换：

### 支持的数据源

```python
# 1. TDX（通达信）- 推荐，免费稳定
package = 'tdx'

# 2. Tushare - 需要token
package = 'tushare'

# 3. 同花顺
package = 'ths'

# 4. 东方财富
from QUANTAXIS.QAFetch import QAEastMoney

# 5. 和讯
from QUANTAXIS.QAFetch import QAHexun
```

### 切换示例

```python
# 方法1: 使用统一接口切换
data_tdx = QA.QA_fetch_get_stock_day(
    package='tdx',
    code='000001',
    start='2024-01-01',
    end='2024-12-31'
)

data_tushare = QA.QA_fetch_get_stock_day(
    package='tushare',
    code='000001',
    start='2024-01-01',
    end='2024-12-31'
)

# 方法2: 直接调用特定数据源
from QUANTAXIS.QAFetch import QATdx, QATushare

data1 = QATdx.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-12-31')
data2 = QATushare.QA_fetch_get_stock_day('000001', '2024-01-01', '2024-12-31')
```

### 容错处理

```python
def fetch_with_fallback(code, start, end):
    """多数据源容错获取"""
    sources = ['tdx', 'tushare', 'ths']

    for source in sources:
        try:
            data = QA.QA_fetch_get_stock_day(
                package=source,
                code=code,
                start=start,
                end=end
            )
            if data is not None and len(data) > 0:
                print(f"✅ 使用数据源: {source}")
                return data
        except Exception as e:
            print(f"❌ {source} 失败: {e}")
            continue

    return None

# 使用
data = fetch_with_fallback('000001', '2024-01-01', '2024-12-31')
```

---

## 📅 交易日历

```python
# 获取交易日期列表
trade_dates = QA.QA_fetch_trade_date()

print(trade_dates[:10])
# ['1990-12-19', '1990-12-20', '1990-12-21', ...]

# 判断是否交易日
from QUANTAXIS.QAUtil import QA_util_if_trade

is_trade_day = QA_util_if_trade('2024-10-25')
print(is_trade_day)  # True 或 False

# 获取上一个交易日
from QUANTAXIS.QAUtil import QA_util_get_last_day

last_day = QA_util_get_last_day('2024-10-25')
print(last_day)  # '2024-10-24'

# 获取下一个交易日
from QUANTAXIS.QAUtil import QA_util_get_next_day

next_day = QA_util_get_next_day('2024-10-25')
print(next_day)  # '2024-10-28'
```

---

## 🎯 最佳实践

### 1. 数据更新策略

```python
import QUANTAXIS as QA
from datetime import datetime, timedelta

def update_stock_data(code_list, days=30):
    """更新最近N天的股票数据"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    for code in code_list:
        try:
            # 从通达信获取最新数据
            data = QA.QA_fetch_get_stock_day(
                package='tdx',
                code=code,
                start=start_date,
                end=end_date
            )

            # 保存到MongoDB
            QA.QA_SU_save_stock_day(data)
            print(f"✅ {code} 更新成功")

        except Exception as e:
            print(f"❌ {code} 更新失败: {e}")

# 使用
stock_list = ['000001', '000002', '600000']
update_stock_data(stock_list)
```

### 2. 批量数据获取

```python
def batch_fetch_stock_day(code_list, start, end, batch_size=50):
    """批量获取股票数据"""
    results = {}

    for i in range(0, len(code_list), batch_size):
        batch = code_list[i:i+batch_size]

        for code in batch:
            try:
                data = QA.QA_fetch_stock_day(
                    code=code,
                    start=start,
                    end=end
                )
                results[code] = data

            except Exception as e:
                print(f"❌ {code}: {e}")

        print(f"✅ 已完成 {min(i+batch_size, len(code_list))}/{len(code_list)}")

    return results

# 使用
codes = QA.QA_fetch_stock_list()['code'].tolist()
data_dict = batch_fetch_stock_day(codes[:100], '2024-01-01', '2024-12-31')
```

### 3. 数据验证

```python
def validate_data(data):
    """验证数据完整性"""
    if data is None or len(data) == 0:
        return False, "数据为空"

    # 检查必要字段
    required_cols = ['code', 'date', 'open', 'high', 'low', 'close', 'volume']
    missing = [col for col in required_cols if col not in data.columns]
    if missing:
        return False, f"缺少字段: {missing}"

    # 检查空值
    null_cols = data.columns[data.isnull().any()].tolist()
    if null_cols:
        return False, f"存在空值: {null_cols}"

    # 检查异常值
    if (data['high'] < data['low']).any():
        return False, "存在high < low的异常数据"

    if (data['close'] > data['high']).any() or (data['close'] < data['low']).any():
        return False, "存在close超出high/low范围的异常数据"

    return True, "数据验证通过"

# 使用
data = QA.QA_fetch_stock_day('000001', '2024-01-01', '2024-12-31')
is_valid, message = validate_data(data)
print(message)
```

### 4. 缓存机制

```python
import pickle
from pathlib import Path

class DataCache:
    """数据缓存管理"""

    def __init__(self, cache_dir='./cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_path(self, key):
        return self.cache_dir / f"{key}.pkl"

    def save(self, key, data):
        """保存数据到缓存"""
        cache_path = self.get_cache_path(key)
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)

    def load(self, key):
        """从缓存加载数据"""
        cache_path = self.get_cache_path(key)
        if not cache_path.exists():
            return None

        with open(cache_path, 'rb') as f:
            return pickle.load(f)

    def is_valid(self, key, max_age_hours=24):
        """检查缓存是否有效"""
        cache_path = self.get_cache_path(key)
        if not cache_path.exists():
            return False

        from datetime import datetime
        file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        age_hours = (datetime.now() - file_time).total_seconds() / 3600

        return age_hours < max_age_hours

# 使用
cache = DataCache()

def fetch_with_cache(code, start, end):
    """带缓存的数据获取"""
    cache_key = f"stock_{code}_{start}_{end}"

    # 尝试从缓存加载
    if cache.is_valid(cache_key):
        data = cache.load(cache_key)
        if data is not None:
            print(f"✅ 从缓存加载: {cache_key}")
            return data

    # 从数据库获取
    data = QA.QA_fetch_stock_day(code, start, end)

    # 保存到缓存
    cache.save(cache_key, data)
    print(f"✅ 已缓存: {cache_key}")

    return data

# 测试
data = fetch_with_cache('000001', '2024-01-01', '2024-12-31')
```

---

## ⚠️ 常见问题

### Q1: 数据获取失败怎么办？

**A**: 使用多数据源容错机制：

```python
def robust_fetch(code, start, end):
    # 优先从MongoDB查询
    try:
        data = QA.QA_fetch_stock_day(code, start, end)
        if data is not None and len(data) > 0:
            return data
    except:
        pass

    # 从通达信获取
    try:
        data = QA.QA_fetch_get_stock_day('tdx', code, start, end)
        if data is not None:
            QA.QA_SU_save_stock_day(data)  # 保存到MongoDB
            return data
    except:
        pass

    # 从Tushare获取
    try:
        data = QA.QA_fetch_get_stock_day('tushare', code, start, end)
        if data is not None:
            QA.QA_SU_save_stock_day(data)
            return data
    except:
        pass

    raise Exception(f"所有数据源都无法获取 {code} 的数据")
```

### Q2: 如何处理复权数据？

**A**: QUANTAXIS提供多种复权方式：

```python
# 不复权
data = QA.QA_fetch_get_stock_day('tdx', '000001', '2020-01-01', '2024-12-31', if_fq='00')

# 前复权（推荐用于回测）
data = QA.QA_fetch_get_stock_day('tdx', '000001', '2020-01-01', '2024-12-31', if_fq='01')

# 后复权
data = QA.QA_fetch_get_stock_day('tdx', '000001', '2020-01-01', '2024-12-31', if_fq='02')

# 手动复权
import QUANTAXIS as QA
data = QA.QA_fetch_stock_day('000001', '2020-01-01', '2024-12-31')
data_qfq = QA.QA_data_stock_to_qfq(data)  # 前复权
data_hfq = QA.QA_data_stock_to_hfq(data)  # 后复权
```

### Q3: 数据存储在哪里？

**A**: QUANTAXIS使用MongoDB存储数据：

```python
# 查看MongoDB配置
from QUANTAXIS.QAUtil import DATABASE

print(DATABASE.stock_day)      # stock_day集合
print(DATABASE.stock_min)      # stock_min集合
print(DATABASE.future_day)     # future_day集合

# 保存数据到MongoDB
QA.QA_SU_save_stock_day(data)       # 保存日线
QA.QA_SU_save_stock_min(data)       # 保存分钟线
QA.QA_SU_save_future_day(data)      # 保存期货日线
```

### Q4: 如何限制数据获取频率？

**A**: 使用速率限制器：

```python
import time
from functools import wraps

def rate_limit(max_per_second=5):
    """速率限制装饰器"""
    min_interval = 1.0 / max_per_second
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)

            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

@rate_limit(max_per_second=2)
def fetch_stock_data(code):
    return QA.QA_fetch_get_stock_day('tdx', code, '2024-01-01', '2024-12-31')

# 使用
for code in ['000001', '000002', '600000']:
    data = fetch_stock_data(code)
    print(f"✅ {code} 获取完成")
```

---

## 🔗 相关资源

- **API参考**: [QAFetch API文档](../api-reference/qafetch.md)
- **数据存储**: [QAStore数据存储](../api-reference/qastore.md)
- **数据分析**: [QAData数据结构](../api-reference/qadata.md)
- **示例代码**: [GitHub Examples](https://github.com/QUANTAXIS/QUANTAXIS/tree/master/examples)

---

## 📝 总结

QAFetch模块提供了完整的金融数据获取能力：

✅ **多数据源**: TDX、Tushare、同花顺等
✅ **全资产**: 股票、期货、期权、数字货币、港美股
✅ **全周期**: 日线、分钟、Tick、实时
✅ **灵活性**: 支持多种数据格式和存储方式
✅ **可靠性**: 容错机制和数据验证

**下一步**: 学习如何使用获取的数据进行[策略开发](./strategy-development.md)

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[← 上一页：快速开始](../getting-started/quickstart.md) | [下一页：策略开发 →](./strategy-development.md)
