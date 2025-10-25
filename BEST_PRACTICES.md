# QUANTAXIS 最佳实践

> 💡 **生产环境最佳实践** - 性能优化、代码规范、架构设计
>
> **版本**: v2.1.0-alpha2 | **适用场景**: 生产环境 | **更新**: 2025-10-25

---

## 📋 目录

- [性能优化](#性能优化)
- [代码规范](#代码规范)
- [架构设计](#架构设计)
- [错误处理](#错误处理)
- [数据库优化](#数据库优化)
- [安全建议](#安全建议)
- [测试策略](#测试策略)
- [部署建议](#部署建议)

---

## ⚡ 性能优化

### 1. 使用Rust组件（100x加速）

#### ✅ 推荐做法

```python
from QUANTAXIS.QARSBridge import has_qars_support, QARSAccount

# 检查并使用Rust账户
if has_qars_support():
    # 使用Rust账户（100x加速）
    account = QARSAccount("account_id", init_cash=100000.0)
else:
    # 降级到Python实现
    from QUANTAXIS.QIFI import QIFI_Account
    account = QIFI_Account("account_id", "pwd", "stock", 100000)
```

**性能提升**:
- 账户创建: 50ms → 0.5ms（100x）
- 订单处理: 10ms → 0.1ms（100x）
- 持仓计算: 5ms → 0.05ms（100x）

#### ❌ 避免的做法

```python
# 不要: 始终使用Python实现
account = QIFI_Account(...)  # 性能损失100x
```

---

### 2. 使用零拷贝数据转换（2-5x加速）

#### ✅ 推荐做法

```python
from QUANTAXIS.QADataBridge import (
    has_dataswap_support,
    convert_pandas_to_polars
)

if has_dataswap_support():
    # 零拷贝转换（2.5x加速）
    df_polars = convert_pandas_to_polars(df_pandas)

    # 使用Polars进行高性能计算
    result = (
        df_polars
        .filter(pl.col("volume") > 1000000)
        .group_by("code")
        .agg(pl.col("price").mean())
    )

    # 转回Pandas（如需要）
    result_pandas = convert_polars_to_pandas(result)
else:
    # 降级到标准处理
    result = df_pandas[df_pandas['volume'] > 1000000].groupby('code')['price'].mean()
```

**性能对比**:
| 操作 | Pandas | Polars (零拷贝) | 加速比 |
|------|--------|----------------|--------|
| 数据转换 (100万行) | 450ms | 180ms | 2.5x |
| 过滤操作 | 120ms | 25ms | 4.8x |
| 分组聚合 | 350ms | 60ms | 5.8x |

#### ❌ 避免的做法

```python
# 不要: 频繁的类型转换
for i in range(100):
    df_polars = pl.from_pandas(df)  # 每次都复制数据
    result = df_polars.filter(...)
    df_pandas = result.to_pandas()  # 又复制回来
```

---

### 3. 使用共享内存（7x加速）

#### ✅ 推荐做法 - 行情数据分发

**进程A（行情服务器）**:
```python
from QUANTAXIS.QADataBridge import SharedMemoryWriter

# 创建共享内存写入器
writer = SharedMemoryWriter("realtime_market", size_mb=20)

while True:
    # 接收实时tick数据
    tick_df = receive_tick_from_exchange()

    # 写入共享内存（7x加速）
    writer.write(tick_df)

    time.sleep(0.1)  # 100ms更新一次
```

**进程B（策略进程）**:
```python
from QUANTAXIS.QADataBridge import SharedMemoryReader

# 创建共享内存读取器
reader = SharedMemoryReader("realtime_market")

while True:
    # 读取最新行情（零拷贝）
    tick_df = reader.read(timeout_ms=200)

    if tick_df is not None:
        # 策略逻辑
        execute_strategy(tick_df)
```

**性能对比**:
- 共享内存传输: ~20ms (100万行)
- Pickle序列化: ~140ms (100万行)
- **加速比: 7x**

#### ❌ 避免的做法

```python
# 不要: 使用pickle在进程间传输
import pickle
import multiprocessing

queue = multiprocessing.Queue()

# 进程A
queue.put(pickle.dumps(df))  # 序列化开销大

# 进程B
df = pickle.loads(queue.get())  # 反序列化开销大
```

---

### 4. 向量化操作

#### ✅ 推荐做法

```python
# 使用向量化计算收益率
df['returns'] = df['close'].pct_change()

# 使用向量化计算信号
df['signal'] = np.where(df['ma5'] > df['ma20'], 1, -1)

# 使用向量化计算累积收益
df['cumulative_returns'] = (1 + df['returns']).cumprod()
```

**性能提升**: 通常快10-100x

#### ❌ 避免的做法

```python
# 不要: 使用循环
returns = []
for i in range(1, len(df)):
    ret = (df.iloc[i]['close'] / df.iloc[i-1]['close']) - 1
    returns.append(ret)
df['returns'] = [0] + returns  # 慢100x
```

---

### 5. 批量操作

#### ✅ 推荐做法

```python
# 批量获取数据
codes = QA.QA_fetch_get_stock_list()['code'].tolist()[:100]

# 使用列表推导式批量处理
data_list = [
    QA.QA_fetch_get_stock_day(code, '2024-01-01', '2024-01-31')
    for code in codes
]

# 合并数据
all_data = pd.concat(data_list, keys=codes)
```

#### ❌ 避免的做法

```python
# 不要: 逐个处理
all_data = pd.DataFrame()
for code in codes:
    df = QA.QA_fetch_get_stock_day(code, '2024-01-01', '2024-01-31')
    df['code'] = code
    all_data = all_data.append(df)  # append很慢，每次都重新分配内存
```

---

## 📝 代码规范

### 1. 命名规范

#### ✅ 推荐做法

```python
# 变量名：小写下划线
stock_code = '000001'
close_price = 10.5
ma_period = 20

# 类名：大驼峰
class MovingAverageStrategy:
    pass

# 函数名：小写下划线
def calculate_returns(prices):
    return prices.pct_change()

# 常量：大写下划线
MAX_POSITION_SIZE = 1000000
DEFAULT_COMMISSION_RATE = 0.0003
```

---

### 2. 类型提示

#### ✅ 推荐做法

```python
from typing import Optional, Union, List
import pandas as pd

def get_stock_data(
    code: str,
    start: str,
    end: str,
    adjust: Optional[str] = None
) -> pd.DataFrame:
    """
    获取股票数据

    参数:
        code: 股票代码
        start: 开始日期
        end: 结束日期
        adjust: 复权类型，可选

    返回:
        股票数据DataFrame
    """
    return QA.QA_fetch_get_stock_day(code, start, end)
```

---

### 3. 文档字符串

#### ✅ 推荐做法

```python
def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.03
) -> float:
    """
    计算夏普比率

    夏普比率衡量每单位风险的超额收益，计算公式:
    Sharpe = (年化收益率 - 无风险利率) / 年化波动率

    参数:
        returns: 收益率序列
        risk_free_rate: 无风险利率，默认3%

    返回:
        夏普比率

    示例:
        >>> returns = pd.Series([0.01, -0.02, 0.03, 0.01])
        >>> sharpe = calculate_sharpe_ratio(returns)
        >>> print(f"夏普比率: {sharpe:.2f}")
    """
    annual_return = returns.mean() * 252
    annual_vol = returns.std() * np.sqrt(252)
    return (annual_return - risk_free_rate) / annual_vol
```

---

### 4. 配置管理

#### ✅ 推荐做法

```python
# config.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class TradingConfig:
    """交易配置"""
    init_cash: float = 100000.0
    commission_rate: float = 0.0003
    slippage: float = 0.0001
    max_position: int = 10

    # MongoDB配置
    mongo_host: str = 'localhost'
    mongo_port: int = 27017
    mongo_db: str = 'quantaxis'

    @classmethod
    def from_file(cls, path: str) -> 'TradingConfig':
        """从配置文件加载"""
        import json
        with open(path) as f:
            config_dict = json.load(f)
        return cls(**config_dict)

# main.py
config = TradingConfig.from_file('config.json')
account = QARSAccount("account", init_cash=config.init_cash)
```

#### ❌ 避免的做法

```python
# 不要: 硬编码配置
init_cash = 100000  # 魔法数字
commission = 0.0003  # 魔法数字
mongo_host = 'localhost'  # 硬编码
```

---

## 🏗️ 架构设计

### 1. 分层架构

#### ✅ 推荐架构

```
项目结构:
├── data/              # 数据层
│   ├── fetcher.py     # 数据获取
│   ├── storage.py     # 数据存储
│   └── processor.py   # 数据处理
│
├── strategy/          # 策略层
│   ├── base.py        # 策略基类
│   ├── ma_strategy.py # 均线策略
│   └── factors.py     # 因子策略
│
├── execution/         # 执行层
│   ├── account.py     # 账户管理
│   ├── broker.py      # 券商接口
│   └── risk.py        # 风险控制
│
├── backtest/          # 回测层
│   ├── engine.py      # 回测引擎
│   └── analyzer.py    # 绩效分析
│
└── utils/             # 工具层
    ├── logger.py      # 日志
    ├── config.py      # 配置
    └── helpers.py     # 辅助函数
```

---

### 2. 策略模式

#### ✅ 推荐做法

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStrategy(ABC):
    """策略基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.positions = {}

    @abstractmethod
    def generate_signal(self, data: pd.DataFrame) -> int:
        """
        生成交易信号

        返回:
            1: 买入信号
            0: 持有
            -1: 卖出信号
        """
        pass

    @abstractmethod
    def on_bar(self, bar: pd.Series):
        """K线回调"""
        pass

class MAStrategy(BaseStrategy):
    """均线策略"""

    def generate_signal(self, data: pd.DataFrame) -> int:
        ma5 = data['close'].rolling(5).mean().iloc[-1]
        ma20 = data['close'].rolling(20).mean().iloc[-1]

        if ma5 > ma20:
            return 1
        elif ma5 < ma20:
            return -1
        return 0

    def on_bar(self, bar: pd.Series):
        # 实现交易逻辑
        pass
```

---

### 3. 依赖注入

#### ✅ 推荐做法

```python
class BacktestEngine:
    """回测引擎"""

    def __init__(
        self,
        strategy: BaseStrategy,
        data_source: DataSource,
        account: AccountInterface
    ):
        self.strategy = strategy
        self.data_source = data_source
        self.account = account

    def run(self):
        data = self.data_source.load()
        for bar in data:
            signal = self.strategy.generate_signal(bar)
            if signal == 1:
                self.account.buy(...)
            elif signal == -1:
                self.account.sell(...)

# 使用
strategy = MAStrategy(config)
data_source = MongoDataSource()
account = QARSAccount("test", 100000)

engine = BacktestEngine(strategy, data_source, account)
engine.run()
```

---

## 🚨 错误处理

### 1. 异常处理

#### ✅ 推荐做法

```python
import logging

logger = logging.getLogger(__name__)

def fetch_stock_data(code: str, start: str, end: str) -> Optional[pd.DataFrame]:
    """
    安全地获取股票数据

    返回None表示失败，便于调用者处理
    """
    try:
        df = QA.QA_fetch_get_stock_day(code, start, end)

        # 数据验证
        if df is None or len(df) == 0:
            logger.warning(f"股票{code}数据为空")
            return None

        # 数据清洗
        df = df.dropna()

        return df

    except Exception as e:
        logger.error(f"获取股票{code}数据失败: {e}", exc_info=True)
        return None

# 使用
df = fetch_stock_data('000001', '2024-01-01', '2024-01-31')
if df is not None:
    # 处理数据
    pass
else:
    # 降级处理
    pass
```

#### ❌ 避免的做法

```python
# 不要: 忽略异常
try:
    df = QA.QA_fetch_get_stock_day(code, start, end)
except:
    pass  # 静默失败，难以调试

# 不要: 过于宽泛的异常捕获
try:
    df = QA.QA_fetch_get_stock_day(code, start, end)
except Exception:  # 捕获所有异常，包括KeyboardInterrupt
    pass
```

---

### 2. 断言验证

#### ✅ 推荐做法

```python
def calculate_position_size(
    account_value: float,
    risk_ratio: float,
    price: float
) -> int:
    """
    计算仓位大小

    参数:
        account_value: 账户总值
        risk_ratio: 风险比例 (0-1)
        price: 股票价格

    返回:
        持仓数量（100股整数倍）
    """
    # 输入验证
    assert account_value > 0, "账户总值必须大于0"
    assert 0 < risk_ratio <= 1, "风险比例必须在(0, 1]之间"
    assert price > 0, "价格必须大于0"

    # 计算仓位
    position_value = account_value * risk_ratio
    shares = int(position_value / price / 100) * 100

    return shares
```

---

## 💾 数据库优化

### 1. 索引优化

#### ✅ 推荐做法

```python
from pymongo import ASCENDING, DESCENDING

# 创建复合索引
DATABASE.stock_day.create_index([
    ('code', ASCENDING),
    ('date', DESCENDING)
])

# 创建唯一索引
DATABASE.stock_list.create_index(
    [('code', ASCENDING)],
    unique=True
)

# 查询使用索引
df = DATABASE.stock_day.find({
    'code': '000001',
    'date': {'$gte': '2024-01-01', '$lte': '2024-01-31'}
}).sort('date', DESCENDING)
```

---

### 2. 批量操作

#### ✅ 推荐做法

```python
# 批量插入
documents = [
    {
        'code': code,
        'date': date,
        'price': price,
        ...
    }
    for code, date, price in data_list
]

DATABASE.stock_day.insert_many(documents, ordered=False)
```

#### ❌ 避免的做法

```python
# 不要: 逐条插入
for code, date, price in data_list:
    DATABASE.stock_day.insert_one({
        'code': code,
        'date': date,
        'price': price,
    })  # 每次都是一次网络请求
```

---

### 3. 查询优化

#### ✅ 推荐做法

```python
# 只查询需要的字段
df = DATABASE.stock_day.find(
    {'code': '000001'},
    {'_id': 0, 'code': 1, 'date': 1, 'close': 1}  # 投影
)

# 使用聚合管道
pipeline = [
    {'$match': {'code': '000001'}},
    {'$group': {
        '_id': '$code',
        'avg_price': {'$avg': '$close'}
    }}
]
result = DATABASE.stock_day.aggregate(pipeline)
```

---

## 🔒 安全建议

### 1. 敏感信息保护

#### ✅ 推荐做法

```python
import os
from dotenv import load_dotenv

# 使用环境变量
load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
API_KEY = os.getenv('TUSHARE_API_KEY')

# .env文件 (不要提交到git)
# MONGO_USER=admin
# MONGO_PASSWORD=your_password
# TUSHARE_API_KEY=your_api_key
```

#### ❌ 避免的做法

```python
# 不要: 硬编码密码
MONGO_PASSWORD = "my_password"  # 泄露风险
API_KEY = "abc123xyz"  # 不要提交到git
```

---

### 2. 输入验证

#### ✅ 推荐做法

```python
def validate_stock_code(code: str) -> bool:
    """验证股票代码格式"""
    import re
    # A股代码: 6位数字
    return bool(re.match(r'^\d{6}$', code))

def safe_fetch(code: str, start: str, end: str):
    # 验证输入
    if not validate_stock_code(code):
        raise ValueError(f"无效的股票代码: {code}")

    # 验证日期格式
    try:
        datetime.strptime(start, '%Y-%m-%d')
        datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        raise ValueError("日期格式必须为YYYY-MM-DD")

    return QA.QA_fetch_get_stock_day(code, start, end)
```

---

## 🧪 测试策略

### 1. 单元测试

#### ✅ 推荐做法

```python
import pytest
import pandas as pd

def test_calculate_returns():
    """测试收益率计算"""
    prices = pd.Series([100, 105, 102, 108])
    expected = pd.Series([0.0, 0.05, -0.0286, 0.0588])

    returns = calculate_returns(prices)

    pd.testing.assert_series_equal(
        returns,
        expected,
        check_exact=False,
        rtol=0.01
    )

def test_ma_strategy_signal():
    """测试均线策略信号生成"""
    data = create_test_data()  # 创建测试数据
    strategy = MAStrategy(config)

    signal = strategy.generate_signal(data)

    assert signal in [-1, 0, 1], "信号必须是-1, 0或1"
```

---

### 2. 回测验证

#### ✅ 推荐做法

```python
def test_backtest_consistency():
    """测试回测结果一致性"""
    # 运行两次回测
    result1 = run_backtest(strategy, data, seed=42)
    result2 = run_backtest(strategy, data, seed=42)

    # 结果应该完全相同
    assert result1['final_value'] == result2['final_value']
    assert result1['sharpe_ratio'] == result2['sharpe_ratio']

def test_backtest_sanity():
    """测试回测合理性"""
    result = run_backtest(strategy, data)

    # 基本合理性检查
    assert result['final_value'] > 0, "最终净值必须大于0"
    assert -1 <= result['max_drawdown'] <= 0, "最大回撤范围: [-1, 0]"
    assert result['total_trades'] >= 0, "交易次数不能为负"
```

---

## 🚀 部署建议

### 1. 日志配置

#### ✅ 推荐做法

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_level=logging.INFO):
    """配置日志"""
    logger = logging.getLogger('quantaxis')
    logger.setLevel(log_level)

    # 文件处理器（自动轮转）
    file_handler = RotatingFileHandler(
        'quantaxis.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
```

---

### 2. 监控告警

#### ✅ 推荐做法

```python
class TradingMonitor:
    """交易监控"""

    def __init__(self, account, alert_threshold=0.05):
        self.account = account
        self.alert_threshold = alert_threshold
        self.last_check_time = datetime.now()

    def check_drawdown(self):
        """检查回撤"""
        current_drawdown = self.account.get_drawdown()

        if current_drawdown > self.alert_threshold:
            self.send_alert(
                f"⚠️ 警告: 回撤超过{self.alert_threshold*100}%，"
                f"当前: {current_drawdown*100:.2f}%"
            )

    def check_position_risk(self):
        """检查持仓风险"""
        for code, position in self.account.positions.items():
            position_ratio = position['value'] / self.account.balance

            if position_ratio > 0.3:  # 单只股票超过30%
                self.send_alert(
                    f"⚠️ 警告: {code}持仓过重，"
                    f"占比: {position_ratio*100:.2f}%"
                )

    def send_alert(self, message):
        """发送告警"""
        logger.warning(message)
        # 可以集成其他告警渠道: 邮件、短信、钉钉等
```

---

### 3. 优雅退出

#### ✅ 推荐做法

```python
import signal
import sys

class TradingSystem:
    """交易系统"""

    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n接收到信号{signum}，准备退出...")
        self.running = False

    def cleanup(self):
        """清理资源"""
        # 保存状态
        self.account.save_state()

        # 关闭数据库连接
        DATABASE.client.close()

        # 关闭共享内存
        if hasattr(self, 'writer'):
            self.writer.close()

        print("清理完成")

    def run(self):
        """运行交易系统"""
        try:
            while self.running:
                # 交易逻辑
                pass
        except Exception as e:
            logger.error(f"系统错误: {e}", exc_info=True)
        finally:
            self.cleanup()
            sys.exit(0)
```

---

## 📊 性能基准

### 推荐配置对比

| 配置 | 账户操作 | 数据转换 | 数据传输 | 适用场景 |
|------|---------|---------|---------|---------|
| **基础Python** | 50ms | 450ms | 850ms | 学习/研究 |
| **+Polars** | 50ms | 180ms | 450ms | 数据分析 |
| **+QARS2** | 0.5ms | 180ms | 450ms | 高频交易 |
| **+QADataSwap** | 0.5ms | 180ms | 120ms | 生产环境 |
| **完整Rust** | 0.5ms | 180ms | 120ms | **推荐配置** |

**加速比**:
- 账户操作: **100x**
- 数据转换: **2.5x**
- 数据传输: **7.1x**

---

## 📚 总结清单

### 性能优化 ✅

- [ ] 使用QARS2 Rust账户（100x加速）
- [ ] 使用零拷贝数据转换（2.5x加速）
- [ ] 使用共享内存传输（7x加速）
- [ ] 使用向量化操作
- [ ] 批量处理数据

### 代码质量 ✅

- [ ] 遵循命名规范
- [ ] 添加类型提示
- [ ] 编写文档字符串
- [ ] 配置管理
- [ ] 分层架构

### 可靠性 ✅

- [ ] 完善的异常处理
- [ ] 输入验证
- [ ] 日志记录
- [ ] 监控告警
- [ ] 优雅退出

### 测试 ✅

- [ ] 单元测试覆盖率>80%
- [ ] 回测结果验证
- [ ] 性能基准测试

### 安全 ✅

- [ ] 敏感信息使用环境变量
- [ ] 输入验证
- [ ] 访问控制

---

**@yutiansut @quantaxis**
**最后更新**: 2025-10-25
