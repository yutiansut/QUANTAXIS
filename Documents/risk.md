# QUANTAXIS_RISK 插件

<!-- TOC -->

- [QUANTAXIS_RISK 插件](#quantaxis_risk-插件)

<!-- /TOC -->


QA_RISK插件是QUANTAXIS对于风险,绩效的一个评估插件

QA_RISK的加载方式是直接加载

```python
# coding:utf-8
import QUANTAXIS as QA

risk = QA.QA_Risk(account, benchmark_code='000300', benchmark_type='index_cn', if_fq=True)
"""
account: QA_Account类/QA_PortfolioView类
benchmark_code: [str]对照参数代码
benchmark_type: [QA.PARAM]对照参数的市场
if_fq: [Bool]原account是否使用复权数据

"""

```
加载了account以后,我们可以对account进行分析,以下字段都是惰性计算的

- 账户信息(risk.account.account_cookie)
- 组合信息(risk.account.portfolio_cookie)
- 用户信息(risk.account.user_cookie)
- 年化百分比收益(risk.annualize_return)
- 账户百分比利润(risk.profit)
- 最大回撤(risk.max_dropback)
- 账户交易时长(risk.time_gap)
- 账户资金曲线波动率(risk.volatitlity)
- 对照标的代码(risk.benchmark_code)
- 对照标的百分比年化收益(risk.benchmark_annualize_return)
- 对照标的百分比总收益(self.benchmark_profit)
- beta值(risk.beta)
- alpha值(risk.alpha)
- 夏普值sharpe(risk.sharpe)
- 初始现金(risk.init_cash)
- 最终总资产(risk.last_assets)
- 账户的总手续费(risk.total_commission)
- 账户的总印花税(risk.total_tax)

- 账户资金曲线(risk.assets)
- 对照标的资金曲线(risk.benchmark_assets)
- 每日持仓市值表(risk.market_value)

画图方法:

- 画出资金曲线 plot_assets_curve
- 用热力图画出每日持仓 plot_dailyhold
- 用热力图画出信号列表 plot_signal
