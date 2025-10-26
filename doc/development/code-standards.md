# 代码规范

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本文档规定QUANTAXIS项目的代码规范，确保代码质量和一致性。

---

## 🎯 代码规范概览

### 核心原则

1. **可读性优先**: 代码是写给人看的，其次才是机器
2. **一致性**: 遵循统一的编码风格
3. **简洁性**: 简单优于复杂，明确优于隐晦
4. **文档化**: 代码即文档，清晰的命名和注释
5. **可测试性**: 代码应该易于测试

---

## 🐍 Python代码规范

### 1. PEP 8 基础规范

```python
# ✅ 正确的导入顺序
import os
import sys
from typing import List, Dict, Optional

import pandas as pd
import numpy as np

import QUANTAXIS as QA
from QUANTAXIS.QAUtil import QA_util_log_info
from QUANTAXIS.QAData import QA_DataStruct_Stock_day

# ❌ 错误的导入
from QUANTAXIS import *  # 避免使用 *

# ✅ 正确的命名
class QADataStruct:  # 类名：CapWords
    pass

def fetch_stock_data():  # 函数名：lowercase_with_underscores
    pass

MARKET_STOCK = 'stock'  # 常量：UPPER_CASE_WITH_UNDERSCORES
user_id = '123'  # 变量：lowercase_with_underscores

# ✅ 正确的空格使用
result = calculate_value(a, b)  # 函数调用
x = 1 + 2  # 运算符两侧
my_list = [1, 2, 3]  # 逗号后

# ❌ 错误的空格
result=calculate_value( a,b )
x=1+2
```

### 2. 类型注解

```python
from typing import List, Dict, Optional, Union
import pandas as pd

# ✅ 函数类型注解
def fetch_stock_day(
    code: str,
    start: str,
    end: str,
    format: str = 'pd'
) -> pd.DataFrame:
    """获取股票日线数据
    
    Args:
        code: 股票代码
        start: 开始日期
        end: 结束日期
        format: 返回格式，默认pandas
        
    Returns:
        股票日线数据DataFrame
    """
    pass

# ✅ 类型注解
class QAAccount:
    def __init__(
        self,
        account_cookie: str,
        init_cash: float = 1000000.0
    ) -> None:
        self.account_cookie: str = account_cookie
        self.init_cash: float = init_cash
        self.balance: float = init_cash
        self.positions: Dict[str, 'QAPosition'] = {}
    
    def get_position(self, code: str) -> Optional['QAPosition']:
        """获取持仓"""
        return self.positions.get(code)
```

### 3. 文档字符串

```python
# ✅ Google风格文档字符串
def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.03
) -> float:
    """计算夏普比率
    
    夏普比率衡量每单位风险的超额收益。
    
    Args:
        returns: 收益率序列
        risk_free_rate: 无风险利率，默认3%
        
    Returns:
        夏普比率
        
    Raises:
        ValueError: 如果收益率序列为空
        
    Examples:
        >>> returns = pd.Series([0.01, 0.02, -0.01, 0.03])
        >>> sharpe = calculate_sharpe_ratio(returns)
        >>> print(f"夏普比率: {sharpe:.2f}")
    """
    if len(returns) == 0:
        raise ValueError("收益率序列不能为空")
    
    excess_returns = returns - risk_free_rate / 252
    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)

# ✅ 类文档字符串
class QAStrategyCtaBase:
    """CTA策略基类
    
    提供CTA策略开发的基础框架，包括事件驱动、持仓管理等功能。
    
    Attributes:
        code: 交易标的代码
        frequence: 数据频率（'1min', '5min', '1day'等）
        start: 回测开始日期
        end: 回测结束日期
        init_cash: 初始资金
        
    Examples:
        >>> class MyStrategy(QAStrategyCtaBase):
        ...     def user_init(self):
        ...         self.ma_period = 20
        ...     
        ...     def on_bar(self, bar):
        ...         # 策略逻辑
        ...         pass
    """
    pass
```

### 4. 错误处理

```python
# ✅ 正确的异常处理
def fetch_data_with_retry(code: str, max_retries: int = 3) -> pd.DataFrame:
    """带重试的数据获取"""
    for attempt in range(max_retries):
        try:
            data = QA.QA_fetch_stock_day(code, '2024-01-01', '2024-12-31')
            if data is None or len(data) == 0:
                raise ValueError(f"未获取到数据: {code}")
            return data
        except ConnectionError as e:
            if attempt == max_retries - 1:
                raise
            logger.warning(f"连接失败，重试 {attempt + 1}/{max_retries}: {e}")
            time.sleep(2 ** attempt)
        except ValueError:
            logger.error(f"数据验证失败: {code}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {e}")
            raise
    
    raise RuntimeError(f"获取数据失败，已重试{max_retries}次")

# ❌ 避免裸except
try:
    data = fetch_data()
except:  # 不要这样做
    pass

# ✅ 使用具体的异常
try:
    data = fetch_data()
except (ValueError, KeyError) as e:
    logger.error(f"数据错误: {e}")
    raise
```

### 5. 代码组织

```python
# ✅ 良好的代码组织
class QAStrategy:
    """策略类"""
    
    # 1. 类变量
    DEFAULT_INIT_CASH = 1000000
    
    # 2. 初始化方法
    def __init__(self, code: str, init_cash: float = None):
        """初始化策略"""
        self.code = code
        self.init_cash = init_cash or self.DEFAULT_INIT_CASH
        self._setup()
    
    # 3. 公共方法
    def run_backtest(self) -> None:
        """运行回测"""
        self._prepare_data()
        self._execute_strategy()
        self._calculate_metrics()
    
    def get_performance(self) -> Dict:
        """获取性能指标"""
        return self._performance_metrics
    
    # 4. 私有方法（按调用顺序）
    def _setup(self) -> None:
        """设置策略"""
        pass
    
    def _prepare_data(self) -> None:
        """准备数据"""
        pass
    
    def _execute_strategy(self) -> None:
        """执行策略"""
        pass
    
    def _calculate_metrics(self) -> None:
        """计算指标"""
        pass
    
    # 5. 魔术方法
    def __repr__(self) -> str:
        return f"QAStrategy(code={self.code}, cash={self.init_cash})"
```

---

## 📝 命名规范

### 1. 模块和包名

```python
# ✅ 正确
QUANTAXIS/
├── QAFetch/           # 包名：短小，全小写
│   ├── __init__.py
│   ├── QAQuery.py     # 模块名：QA前缀 + 功能
│   └── QATdx.py
├── QAData/
└── QAStrategy/

# ❌ 错误
QUANTAXIS/
├── Fetch_Module/      # 避免下划线
├── data.py            # 太通用
└── my_strategy.py     # 避免my/temp等前缀
```

### 2. 类和函数名

```python
# ✅ 类名：大驼峰
class QADataStructStockDay:
    pass

class QAStrategyCtaBase:
    pass

# ✅ 函数名：小写+下划线
def fetch_stock_day():
    pass

def calculate_sharpe_ratio():
    pass

# ✅ 私有方法：单下划线前缀
def _internal_helper():
    pass

# ✅ 魔术方法：双下划线
def __init__(self):
    pass

# ❌ 避免
class qaStrategy:  # 首字母应大写
    pass

def FetchData():  # 函数名不应大写
    pass

def __private_method():  # 避免双下划线前缀（非魔术方法）
    pass
```

### 3. 变量名

```python
# ✅ 正确的变量命名
stock_code = '000001'
user_id = 'user123'
init_cash = 1000000
max_position_size = 5

# ✅ 常量：全大写
MAX_RETRY_TIMES = 3
DEFAULT_FREQUENCE = '1day'
MARKET_TYPE_STOCK = 'stock_cn'

# ✅ 私有变量：单下划线前缀
self._internal_state = None
self._cache = {}

# ❌ 避免
sc = '000001'  # 太短，不清晰
stockCode = '000001'  # Python不使用驼峰
temp = 123  # 避免temp, tmp等无意义名称
```

---

## 🔧 最佳实践

### 1. 函数设计

```python
# ✅ 单一职责
def fetch_stock_data(code: str) -> pd.DataFrame:
    """只负责获取数据"""
    return QA.QA_fetch_stock_day(code, '2024-01-01', '2024-12-31')

def calculate_ma(data: pd.DataFrame, period: int) -> pd.Series:
    """只负责计算均线"""
    return data['close'].rolling(period).mean()

# ❌ 多重职责
def fetch_and_calculate(code: str, period: int):
    """不推荐：一个函数做太多事"""
    data = fetch_stock_data(code)
    ma = calculate_ma(data, period)
    save_to_database(ma)
    send_notification()
    return ma

# ✅ 函数参数不宜过多
def create_strategy(
    code: str,
    start: str,
    end: str,
    *,  # 强制后续参数使用关键字
    init_cash: float = 1000000,
    frequence: str = '1day',
    commission: float = 0.0003
) -> 'QAStrategy':
    """使用默认值和关键字参数"""
    pass

# ❌ 参数过多
def create_strategy(code, start, end, init_cash, frequence, 
                   commission, slippage, benchmark, risk_free):
    pass

# ✅ 使用配置对象
from dataclasses import dataclass

@dataclass
class StrategyConfig:
    code: str
    start: str
    end: str
    init_cash: float = 1000000
    frequence: str = '1day'
    commission: float = 0.0003

def create_strategy(config: StrategyConfig) -> 'QAStrategy':
    """使用配置对象"""
    pass
```

### 2. 列表推导式和生成器

```python
# ✅ 列表推导式（数据量小）
codes = ['000001', '000002', '600000']
stock_names = [get_stock_name(code) for code in codes]

# ✅ 生成器（数据量大）
def fetch_all_stocks():
    """使用生成器避免内存占用"""
    codes = QA.QA_fetch_stock_list()['code']
    for code in codes:
        yield QA.QA_fetch_stock_day(code, '2024-01-01', '2024-12-31')

# ✅ 条件推导
positive_returns = [r for r in returns if r > 0]

# ❌ 过于复杂的推导
result = [
    process(x, y, z) 
    for x in data1 
    for y in data2 
    if condition1(x) 
    for z in data3 
    if condition2(y, z)
]  # 改用普通循环

# ✅ 普通循环更清晰
result = []
for x in data1:
    if not condition1(x):
        continue
    for y in data2:
        for z in data3:
            if condition2(y, z):
                result.append(process(x, y, z))
```

### 3. 上下文管理器

```python
# ✅ 使用with语句
with open('data.csv', 'r') as f:
    data = f.read()

# ✅ 数据库连接
from pymongo import MongoClient

def fetch_from_mongodb(collection: str, query: dict):
    with MongoClient('mongodb://localhost:27017') as client:
        db = client.quantaxis
        return list(db[collection].find(query))

# ✅ 自定义上下文管理器
from contextlib import contextmanager

@contextmanager
def timer(name: str):
    """计时上下文管理器"""
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        logger.info(f"{name} 耗时: {elapsed:.2f}s")

# 使用
with timer("数据获取"):
    data = fetch_stock_data('000001')
```

### 4. 装饰器

```python
import functools
import time
from typing import Callable

# ✅ 缓存装饰器
def cache(func: Callable) -> Callable:
    """简单缓存装饰器"""
    _cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]
    
    return wrapper

@cache
def fetch_stock_list():
    """获取股票列表（会被缓存）"""
    return QA.QA_fetch_stock_list()

# ✅ 重试装饰器
def retry(max_attempts: int = 3, delay: float = 1.0):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2.0)
def fetch_data_from_api(code: str):
    """从API获取数据（带重试）"""
    pass
```

---

## ✅ 代码质量检查

### 1. 使用pylint

```bash
# 安装pylint
pip install pylint

# 检查单个文件
pylint QUANTAXIS/QAStrategy/qactabase.py

# 检查整个包
pylint QUANTAXIS/

# 使用配置文件
pylint --rcfile=.pylintrc QUANTAXIS/
```

### 2. 使用black格式化

```bash
# 安装black
pip install black

# 格式化代码
black QUANTAXIS/

# 检查但不修改
black --check QUANTAXIS/
```

### 3. 使用mypy类型检查

```bash
# 安装mypy
pip install mypy

# 类型检查
mypy QUANTAXIS/

# 配置文件 mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
```

---

## 📊 性能优化规范

```python
# ✅ 使用局部变量
def calculate_total(data: pd.DataFrame) -> float:
    # 缓存属性访问
    values = data['close'].values
    total = 0
    for value in values:
        total += value
    return total

# ❌ 重复属性访问
def calculate_total_slow(data: pd.DataFrame) -> float:
    total = 0
    for i in range(len(data)):
        total += data['close'].iloc[i]  # 每次都访问
    return total

# ✅ 使用向量化
import numpy as np

def calculate_returns_fast(prices: np.ndarray) -> np.ndarray:
    """向量化计算收益率"""
    return np.diff(prices) / prices[:-1]

# ❌ 使用循环
def calculate_returns_slow(prices: list) -> list:
    """循环计算（慢）"""
    returns = []
    for i in range(1, len(prices)):
        returns.append((prices[i] - prices[i-1]) / prices[i-1])
    return returns
```

---

## 🔗 相关资源

- **测试指南**: [测试指南文档](./testing.md)
- **性能优化**: [性能优化指南](../advanced/performance-tuning.md)
- **PEP 8**: https://peps.python.org/pep-0008/

---

## 📝 总结

代码规范要点：

✅ **遵循PEP 8**: Python官方代码风格指南  
✅ **类型注解**: 提高代码可读性和可维护性  
✅ **清晰命名**: 变量和函数名应具有描述性  
✅ **文档完善**: 使用docstring记录API  
✅ **工具检查**: 使用pylint/black/mypy  

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[返回开发指南](../README.md)
