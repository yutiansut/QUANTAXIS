# 常见问题

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本文档收集了QUANTAXIS使用过程中的常见问题和解决方案。

---

## 📚 目录

- [安装问题](#安装问题)
- [数据获取](#数据获取)
- [策略开发](#策略开发)
- [回测系统](#回测系统)
- [实盘交易](#实盘交易)
- [性能优化](#性能优化)
- [部署运维](#部署运维)

---

## 🔧 安装问题

### Q1: pip install QUANTAXIS失败？

**A**: 

```bash
# 方法1: 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple QUANTAXIS

# 方法2: 从源码安装
git clone https://github.com/QUANTAXIS/QUANTAXIS.git
cd QUANTAXIS
pip install -e .

# 方法3: 安装特定版本
pip install QUANTAXIS==2.1.0
```

### Q2: 安装后import报错？

**A**: 

```python
# 检查版本
import QUANTAXIS as QA
print(QA.__version__)

# 常见原因:
# 1. Python版本不兼容（需要3.5-3.10）
python --version

# 2. 依赖包缺失
pip install -r requirements.txt

# 3. 虚拟环境问题
# 确保在正确的虚拟环境中
which python
```

### Q3: MongoDB连接失败？

**A**:

```python
# 检查MongoDB状态
# Linux/Mac
systemctl status mongod
# 或
mongo --eval "db.version()"

# 检查连接配置
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
try:
    client.server_info()
    print("MongoDB连接成功")
except Exception as e:
    print(f"连接失败: {e}")

# 常见问题：
# 1. MongoDB未启动
sudo systemctl start mongod

# 2. 端口被占用
sudo netstat -tulpn | grep 27017

# 3. 认证失败
client = MongoClient(
    'mongodb://username:password@localhost:27017/',
    authSource='admin'
)
```

---

## 📊 数据获取

### Q4: 无法获取股票数据？

**A**:

```python
import QUANTAXIS as QA

# 1. 检查数据源
data = QA.QA_fetch_get_stock_day(
    package='tdx',  # 尝试不同数据源: tdx/tushare/ths
    code='000001',
    start='2024-01-01',
    end='2024-12-31'
)

# 2. 检查数据库
# 确保数据已保存到MongoDB
QA.QA_SU_save_stock_day('000001')

# 3. 检查代码格式
# A股代码应为6位数字
code = '000001'  # ✅ 正确
code = '1'       # ❌ 错误
```

### Q5: 期货数据缺失？

**A**:

```python
# 1. 更新期货列表
QA.QA_SU_save_future_list()

# 2. 保存期货数据
QA.QA_SU_save_future_day('rb2501')
QA.QA_SU_save_future_min('rb2501')

# 3. 检查合约代码
# 期货合约代码格式：品种+年月
'rb2501'  # ✅ 螺纹钢2025年1月
'rb25'    # ❌ 错误格式

# 4. 使用最新合约
from QUANTAXIS.QAUtil import QA_util_get_real_date
date = QA_util_get_real_date('20250101')
```

### Q6: 如何加速数据获取？

**A**:

```python
from multiprocessing import Pool
import QUANTAXIS as QA

# 并行获取多个股票
def fetch_stock(code):
    return QA.QA_fetch_stock_day(code, '2024-01-01', '2024-12-31')

codes = ['000001', '000002', '600000']
with Pool(processes=4) as pool:
    results = pool.map(fetch_stock, codes)

# 使用缓存
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_cached(code, start, end):
    return QA.QA_fetch_stock_day(code, start, end)
```

---

## 💡 策略开发

### Q7: 策略无法运行？

**A**:

```python
from QUANTAXIS.QAStrategy import QAStrategyCtaBase

class MyStrategy(QAStrategyCtaBase):
    def user_init(self):
        # 必须实现user_init
        self.ma_period = 20
    
    def on_bar(self, bar):
        # 必须实现on_bar
        # 常见错误：
        # 1. 没有实现必要方法
        # 2. 方法签名错误
        pass

# 检查继承
strategy = MyStrategy(code='rb2501')
print(isinstance(strategy, QAStrategyCtaBase))  # 应为True
```

### Q8: 如何调试策略？

**A**:

```python
import logging

class MyStrategy(QAStrategyCtaBase):
    def user_init(self):
        # 配置日志
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    
    def on_bar(self, bar):
        # 打印调试信息
        self.logger.debug(f"收到Bar: {bar.datetime} {bar.close}")
        
        # 检查持仓
        self.logger.info(f"当前持仓: {self.acc.positions}")
        
        # 检查账户
        self.logger.info(f"账户权益: {self.acc.balance}")

# 使用Python调试器
import pdb

def on_bar(self, bar):
    pdb.set_trace()  # 设置断点
    # 策略逻辑
```

### Q9: 策略收益不稳定？

**A**:

```python
# 1. 检查交易成本
strategy = MyStrategy(
    code='rb2501',
    commission=0.0003,  # 手续费
    slippage=0.0001     # 滑点
)

# 2. 增加样本外测试
# 训练集
strategy_train = MyStrategy(start='2020-01-01', end='2023-12-31')
strategy_train.run_backtest()

# 测试集
strategy_test = MyStrategy(start='2024-01-01', end='2024-12-31')
strategy_test.run_backtest()

# 3. 参数优化
from itertools import product

params = {
    'fast_period': [5, 10, 15],
    'slow_period': [20, 30, 40]
}

results = []
for fast, slow in product(*params.values()):
    strategy = MyStrategy(fast_period=fast, slow_period=slow)
    strategy.run_backtest()
    results.append({
        'params': (fast, slow),
        'sharpe': strategy.acc.sharpe_ratio
    })

# 找出最优参数
best = max(results, key=lambda x: x['sharpe'])
```

---

## 🔙 回测系统

### Q10: 回测结果与实盘差异大？

**A**:

```python
# 1. 检查交易成本
strategy = MyStrategy(
    commission=0.0003,      # 手续费率
    slippage=0.0001,        # 滑点
    tax=0.001               # 印花税（股票）
)

# 2. 检查成交逻辑
# 避免使用未来数据
def on_bar(self, bar):
    # ❌ 错误：使用当前bar的收盘价
    if bar.close > self.ma[-1]:
        self.BuyOpen(bar.code, 1, bar.close)
    
    # ✅ 正确：使用历史数据
    if len(self.price_history) > 20:
        ma = sum(self.price_history[-20:]) / 20
        if bar.close > ma:
            self.BuyOpen(bar.code, 1)  # 下一个bar成交

# 3. 检查数据质量
data = QA.QA_fetch_stock_day('000001', '2024-01-01', '2024-12-31')

# 检查缺失值
print(f"缺失值: {data.isnull().sum()}")

# 检查异常值
print(f"价格范围: {data['close'].min()} - {data['close'].max()}")
```

### Q11: 回测速度太慢？

**A**:

```python
# 1. 减少数据查询
class FastStrategy(QAStrategyCtaBase):
    def user_init(self):
        # 预加载数据
        self.preload_data()
    
    def preload_data(self):
        # 一次性加载所有数据
        self.market_data = QA.QA_fetch_stock_day(
            self.code,
            self.start,
            self.end
        )

# 2. 使用Rust加速
import qars2

# 使用QARS2计算指标
ma = qars2.ma(data['close'].values, 20)  # 100x faster

# 3. 并行回测
from multiprocessing import Pool

def run_backtest(params):
    strategy = MyStrategy(**params)
    strategy.run_backtest()
    return strategy.acc.sharpe_ratio

param_list = [{'fast': 5, 'slow': 20}, {'fast': 10, 'slow': 30}]
with Pool(4) as pool:
    results = pool.map(run_backtest, param_list)
```

---

## 🎯 实盘交易

### Q12: 如何从回测切换到实盘？

**A**:

```python
# 回测模式
strategy_backtest = MyStrategy(
    code='rb2501',
    frequence='5min',
    start='2024-01-01',
    end='2024-12-31',
    model='backtest'  # 回测模式
)
strategy_backtest.run_backtest()

# 模拟盘
strategy_sim = MyStrategy(
    code='rb2501',
    frequence='5min',
    model='sim',  # 模拟盘
    data_host='192.168.1.100',
    trade_host='192.168.1.100'
)
strategy_sim.run()

# 实盘
strategy_live = MyStrategy(
    code='rb2501',
    frequence='5min',
    model='live',  # 实盘
    data_host='192.168.1.100',
    trade_host='192.168.1.100'
)
strategy_live.run()

# 注意：策略逻辑完全相同，只改变model参数
```

### Q13: 实盘如何风控？

**A**:

```python
class SafeStrategy(QAStrategyCtaBase):
    def user_init(self):
        # 仓位限制
        self.max_position = 5
        self.max_total_position = 20
        
        # 止损止盈
        self.stop_loss_pct = 0.02
        self.take_profit_pct = 0.05
        
        # 时间控制
        self.trading_start = '09:05'
        self.trading_end = '14:55'
    
    def on_bar(self, bar):
        # 检查交易时间
        if not self.is_trading_time(bar.datetime):
            return
        
        # 检查仓位限制
        if not self.check_position_limit(bar.code):
            return
        
        # 止损止盈
        self.check_stop_loss(bar)
        self.check_take_profit(bar)
        
        # 策略逻辑
        self.strategy_logic(bar)
```

---

## ⚡ 性能优化

### Q14: 如何提升系统性能？

**A**:

```python
# 1. 使用Rust加速
import qars2

# Python方式（慢）
ma = data['close'].rolling(20).mean()

# Rust方式（快100倍）
ma = qars2.ma(data['close'].values, 20)

# 2. 使用MongoDB索引
from pymongo import MongoClient, ASCENDING

client = MongoClient()
db = client.quantaxis

# 创建复合索引
db.stock_day.create_index([
    ('code', ASCENDING),
    ('date_stamp', ASCENDING)
])

# 3. 使用ClickHouse
# 大规模数据分析使用ClickHouse
from clickhouse_driver import Client

client = Client('localhost')
result = client.execute('''
    SELECT * FROM stock_day
    WHERE code = '000001'
    AND date >= '2024-01-01'
''')

# 4. 数据缓存
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_cached(code, start, end):
    return QA.QA_fetch_stock_day(code, start, end)
```

### Q15: 内存占用过高？

**A**:

```python
# 1. 使用生成器
def fetch_all_stocks():
    """使用生成器而非列表"""
    codes = QA.QA_fetch_stock_list()['code']
    for code in codes:
        yield QA.QA_fetch_stock_day(code, '2024-01-01', '2024-12-31')

# 2. 限制历史数据
from collections import deque

class MemoryEfficientStrategy(QAStrategyCtaBase):
    def user_init(self):
        # 只保留必要的历史数据
        self.price_buffer = deque(maxlen=100)
    
    def on_bar(self, bar):
        self.price_buffer.append(bar.close)

# 3. 定期垃圾回收
import gc

def on_dailyclose(self):
    gc.collect()  # 强制垃圾回收
```

---

## 🚀 部署运维

### Q16: 如何部署到生产环境？

**A**:

```bash
# 1. 使用Docker
docker-compose up -d

# 2. 使用Kubernetes
kubectl apply -f k8s/

# 3. 使用Systemd
# /etc/systemd/system/quantaxis.service
[Unit]
Description=QUANTAXIS Strategy
After=network.target

[Service]
Type=simple
User=quantaxis
WorkingDirectory=/home/quantaxis/strategies
ExecStart=/usr/bin/python3 strategy.py
Restart=always

[Install]
WantedBy=multi-user.target

# 启动服务
sudo systemctl enable quantaxis
sudo systemctl start quantaxis
```

### Q17: 如何监控系统状态？

**A**:

```python
# 1. 集成Prometheus
from prometheus_client import Counter, Gauge, start_http_server

# 定义指标
trade_counter = Counter('trades_total', 'Total trades')
balance_gauge = Gauge('account_balance', 'Account balance')

def on_trade(self, trade):
    trade_counter.inc()
    balance_gauge.set(self.acc.balance)

# 启动metrics服务器
start_http_server(8000)

# 2. 日志监控
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('strategy.log'),
        logging.StreamHandler()
    ]
)

# 3. 告警通知
def send_alert(message):
    """发送告警（微信/邮件/钉钉）"""
    # 实现告警逻辑
    pass

def on_bar(self, bar):
    if self.acc.balance < self.init_cash * 0.9:
        send_alert("账户权益低于90%")
```

---

## 📞 获取帮助

### 社区支持

- **GitHub Issues**: https://github.com/QUANTAXIS/QUANTAXIS/issues
- **QQ群**: 563280067
- **论坛**: https://www.yutiansut.com

### 文档资源

- [快速开始](../README.md)
- [用户指南](../user-guide/README.md)
- [API文档](../api/README.md)

---

## 📝 总结

常见问题分类：

✅ **安装配置**: 环境搭建、依赖安装、数据库配置  
✅ **数据获取**: 数据源切换、数据质量、性能优化  
✅ **策略开发**: 调试技巧、风险控制、参数优化  
✅ **回测系统**: 结果验证、性能提升、样本外测试  
✅ **实盘交易**: 模式切换、风控措施、监控告警  

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[返回文档中心](../README.md)
