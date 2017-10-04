# QABacktest 模块

QUANTAXIS的回测核心模块 包括回测引擎/回测的绩效分析

```
QAAnalysis.py
    - def QA_backtest_analysis_start
    - def QA_backtest_calc_assets
    - def QA_backtest_calc_benchmark
    - def QA_backtest_calc_alpha
    - def QA_backtest_calc_beta
    - def QA_backtest_calc_profit
    - def QA_backtest_calc_profit_per_year
    - def QA_backtest_calc_profit_matrix
    - def QA_backtest_calc_volatility
    - def QA_backtest_calc_dropback_max
    - def QA_backtest_calc_sharpe
    - def QA_backtest_calc_trade_date
    - def QA_backtest_calc_win_rate
QABacktest.py
    - class QA_Backtest

QAPlot.py[未启用]
QAEventenging.py[未启用] 目前事件引擎内置在QABacktest里面
```
