# 实盘交易

**版本**: 2.1.0-alpha2
**作者**: @yutiansut @quantaxis
**更新日期**: 2025-10-25

本章节介绍如何使用QUANTAXIS进行实盘交易，包括实盘部署、风险控制和监控管理。

---

## 📚 实盘交易概览

QUANTAXIS支持策略从回测到实盘的无缝切换，采用相同的代码和QIFI账户系统。

### ✨ 核心特性

- **回测实盘一体化**: 相同策略代码
- **QIFI账户**: 统一的账户管理
- **多柜台支持**: CTP、OES等
- **EventMQ消息队列**: 异步通信
- **实时监控**: 完整的监控体系

---

## 🚀 快速开始

### 1. 实盘部署

```python
from QUANTAXIS.QAStrategy import QAStrategyCtaBase


class LiveStrategy(QAStrategyCtaBase):
    """实盘策略"""

    def user_init(self):
        self.ma_period = 20

    def on_bar(self, bar):
        # 策略逻辑（与回测完全相同）
        data = self.get_code_marketdata(bar.code)
        if len(data) < self.ma_period:
            return

        close_prices = [x['close'] for x in data]
        ma = sum(close_prices[-self.ma_period:]) / self.ma_period

        positions = self.acc.positions
        if bar.close > ma and bar.code not in positions:
            self.BuyOpen(bar.code, 1)
        elif bar.close < ma and bar.code in positions:
            self.SellClose(bar.code, 1)


# 实盘配置
strategy = LiveStrategy(
    code='rb2501',
    frequence='5min',
    strategy_id='live_ma_strategy',

    # 实盘模式
    model='live',  # 'sim' 模拟, 'live' 实盘

    # EventMQ配置（数据）
    data_host='192.168.1.100',
    data_port=5672,
    data_user='admin',
    data_password='admin',

    # EventMQ配置（交易）
    trade_host='192.168.1.100',
    trade_port=5672,
    trade_user='admin',
    trade_password='admin',

    # 通知
    send_wx=True,  # 微信通知
)

# 启动实盘
strategy.run()
```

---

## ⚙️ 系统架构

### 实盘组件

```
XMonitor (GUI)
    ↓
XServer (Middleware)
    ↓
EventMQ (RabbitMQ)
    ↓
[数据流] → XMarketCenter → XQuant (策略)
                                ↓
[订单流] ← XTrader ← XRiskJudge ←
```

### 组件说明

- **XMarketCenter**: 行情网关（TDX/CTP/OES）
- **XQuant**: 策略引擎
- **XRiskJudge**: 风控引擎
- **XTrader**: 交易网关
- **XServer**: 中间件服务器
- **XMonitor**: 监控客户端

---

## 🔐 风险控制

### 1. 仓位控制

```python
def user_init(self):
    # 单标的最大仓位
    self.max_position = 5
    
    # 账户总仓位限制
    self.max_total_position = 20
    
    # 单笔最大资金比例
    self.max_position_pct = 0.2

def on_bar(self, bar):
    # 检查仓位限制
    positions = self.acc.positions
    if bar.code in positions:
        if positions[bar.code].volume_long >= self.max_position:
            return  # 已达最大仓位
    
    # 检查总仓位
    total_pos = sum(p.volume_long for p in positions.values())
    if total_pos >= self.max_total_position:
        return
```

### 2. 止损止盈

```python
def on_bar(self, bar):
    positions = self.acc.positions
    if bar.code in positions:
        pos = positions[bar.code]
        if pos.volume_long > 0:
            entry_price = pos.open_price_long
            pnl_pct = (bar.close - entry_price) / entry_price
            
            # 止损2%
            if pnl_pct <= -0.02:
                self.SellClose(bar.code, pos.volume_long)
                self.send_wx_message(f"止损: {pnl_pct*100:.2f}%")
            
            # 止盈5%
            elif pnl_pct >= 0.05:
                self.SellClose(bar.code, pos.volume_long)
                self.send_wx_message(f"止盈: {pnl_pct*100:.2f}%")
```

### 3. 时间控制

```python
def on_bar(self, bar):
    from datetime import time
    
    # 避开开盘和收盘
    current_time = bar.datetime.time()
    
    # 期货：避开09:00-09:05和14:55-15:00
    if time(9, 0) <= current_time <= time(9, 5):
        return
    if time(14, 55) <= current_time <= time(15, 0):
        return
```

---

## 📊 监控管理

### 1. 实时日志

```python
import logging

class LiveStrategy(QAStrategyCtaBase):
    
    def user_init(self):
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'live_{self.strategy_id}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(self.strategy_id)
    
    def on_bar(self, bar):
        self.logger.info(f"[BAR] {bar.datetime} {bar.code} {bar.close}")
        
        # 记录交易
        if self.has_signal:
            self.logger.warning(f"[SIGNAL] {self.signal_type}")
    
    def on_order(self, order):
        self.logger.info(f"[ORDER] {order.order_id} {order.status}")
    
    def on_trade(self, trade):
        self.logger.info(f"[TRADE] {trade.trade_id} {trade.volume}@{trade.price}")
```

### 2. 微信通知

```python
def send_wx_message(self, message):
    """发送微信通知"""
    if self.send_wx:
        # QUANTAXIS内置微信通知
        # 需要配置微信企业号
        pass

def on_bar(self, bar):
    # 重要事件通知
    if self.has_signal:
        self.send_wx_message(f"交易信号: {self.signal_type}, 价格: {bar.close}")
    
    # 每日汇总
    if bar.datetime.hour == 15 and bar.datetime.minute == 0:
        balance = self.acc.balance
        positions = len(self.acc.positions)
        self.send_wx_message(f"日终: 权益{balance:.2f}, 持仓{positions}个")
```

### 3. 性能监控

```python
def on_dailyclose(self):
    """每日收盘统计"""
    acc = self.acc
    
    # 计算当日收益
    daily_profit = acc.balance - self.yesterday_balance
    daily_return = daily_profit / self.yesterday_balance * 100
    
    # 统计交易
    today_trades = [t for t in acc.trades.values() 
                   if t.datetime.date() == datetime.date.today()]
    
    # 输出统计
    print(f"{'='*50}")
    print(f"日期: {datetime.date.today()}")
    print(f"权益: {acc.balance:.2f}")
    print(f"当日收益: {daily_profit:.2f} ({daily_return:.2f}%)")
    print(f"当日交易: {len(today_trades)}笔")
    print(f"持仓: {len(acc.positions)}个")
    print(f"{'='*50}")
    
    # 更新昨日权益
    self.yesterday_balance = acc.balance
```

---

## 🛠️ 故障处理

### 1. 断线重连

```python
def on_disconnect(self):
    """处理断线"""
    self.logger.error("连接断开，尝试重连...")
    
    # 保存当前状态
    self.save_state()
    
    # 尝试重连
    for i in range(3):
        try:
            self.reconnect()
            self.logger.info("重连成功")
            break
        except Exception as e:
            self.logger.error(f"重连失败 {i+1}/3: {e}")
            time.sleep(5)

def save_state(self):
    """保存策略状态"""
    state = {
        'positions': self.acc.positions,
        'balance': self.acc.balance,
        'last_datetime': self.dt
    }
    with open(f'state_{self.strategy_id}.json', 'w') as f:
        json.dump(state, f)

def load_state(self):
    """加载策略状态"""
    try:
        with open(f'state_{self.strategy_id}.json', 'r') as f:
            state = json.load(f)
        return state
    except:
        return None
```

### 2. 异常处理

```python
def on_bar(self, bar):
    try:
        # 策略逻辑
        self.strategy_logic(bar)
    except Exception as e:
        self.logger.error(f"策略执行异常: {e}")
        self.logger.exception(e)
        
        # 紧急止损（可选）
        if self.emergency_stop:
            self.close_all_positions()
        
        # 发送警报
        self.send_wx_message(f"❌ 策略异常: {e}")

def close_all_positions(self):
    """紧急平掉所有持仓"""
    for code, pos in self.acc.positions.items():
        if pos.volume_long > 0:
            self.SellClose(code, pos.volume_long)
            self.logger.warning(f"紧急平仓: {code}")
```

---

## 📝 最佳实践

### 1. 逐步上线

```python
# 阶段1: 模拟盘测试（1-2周）
strategy = MyStrategy(model='sim', init_cash=1000000)

# 阶段2: 小资金实盘（1-2周）
strategy = MyStrategy(model='live', init_cash=100000)

# 阶段3: 正常资金实盘
strategy = MyStrategy(model='live', init_cash=1000000)
```

### 2. 实盘检查清单

- [ ] 回测表现稳定（至少6个月历史）
- [ ] 样本外测试通过
- [ ] 模拟盘运行正常（至少2周）
- [ ] 风控参数设置合理
- [ ] 监控告警配置完成
- [ ] 应急预案准备就绪
- [ ] 日志和审计完备

### 3. 持续优化

```python
# 定期review
def weekly_review(self):
    """每周review"""
    # 1. 统计本周表现
    # 2. 分析异常交易
    # 3. 检查风控触发
    # 4. 评估策略有效性
    # 5. 调整参数（谨慎）
    pass
```

---

## ⚠️ 常见问题

### Q1: 实盘和回测结果差异大？

**A**: 
1. 检查滑点和手续费设置
2. 验证信号延迟处理
3. 确认数据源一致性
4. 检查订单成交逻辑

### Q2: 如何保证策略稳定运行？

**A**:
1. 使用进程守护（supervisor/systemd）
2. 配置自动重启
3. 完善异常处理
4. 建立监控告警

### Q3: 如何控制实盘风险？

**A**:
1. 设置严格止损
2. 控制仓位大小
3. 分散投资标的
4. 实时监控异常

---

## 🔗 相关资源

- **策略开发**: [策略开发指南](./strategy-development.md)
- **回测系统**: [回测系统指南](./backtesting.md)
- **部署指南**: [部署概览](../deployment/overview.md)

---

## 📝 总结

QUANTAXIS实盘交易提供了：

✅ **无缝切换**: 回测实盘一体化
✅ **完整监控**: 日志、通知、统计
✅ **风险控制**: 多层次风控机制
✅ **稳定可靠**: 异常处理和恢复
✅ **多柜台**: 支持多种交易接口

---

**作者**: @yutiansut @quantaxis
**最后更新**: 2025-10-25

[← 上一页：回测系统](./backtesting.md) | [返回文档中心](../README.md)
