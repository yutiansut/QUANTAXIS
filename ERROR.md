# 勘误记录

---

## `QAUtil` 模块

### `QAParameter.py`

   1. line 48, 代码重复
   2. line 182, `NETWORK_BROKERN` --> `NETWORK_BROKEN`
   3. line 183, `DATABSECONNECT_LOST` --> `DATABASECONNECT_LOST`
   
### `QADate_trade.py`

   1. TODO: 添加 `QA_util_format_date2str` 函数，支持将 `str, datetime.datetime, int` 类型转换为 "%Y-%m-%d" 格式日期
   2. TODO: 添加 `QA_util_get_next_trade_date` 函数, 可获取指定交易日之后 n 天交易日日期
   3. TODO: 添加 `QA_util_get_pre_trade_date` 函数, 可获取指定交易日之前 n 天交易日日期
   
### `QABar.py`

   1. `QA_util_make_futuremin_index(day, type_="1min")` --> 废弃函数，且函数语句有误，建议删除；或者保留接口用于生成期货品种的分钟指标？


###  `QALogs.py`

   1. `QA_util_log_expection(logs, ui_log=None, ui_progress=None)` --> 处理 exception, 是否考虑将名称改换成 `QA_util_log_exception`,
      经过查找， QA 中用到该函数的文件和函数位置如下:
      
      ```
      quantaxis/QUANTAXIS/QASU/save_backtest.py:from QUANTAXIS.QAUtil import QA_util_log_expection
      quantaxis/QUANTAXIS/QASU/save_backtest.py:        QA_util_log_expection('QA error in saving backtest account')
      quantaxis/QUANTAXIS/QASU/save_tusharepro_pg.py:from QUANTAXIS.QAUtil.QALogs import (QA_util_log_debug, QA_util_log_expection,
      quantaxis/QUANTAXIS/QAUtil/QALogs.py:QA_util_log_expection()
      quantaxis/QUANTAXIS/QAUtil/QALogs.py:def QA_util_log_expection(logs, ui_log=None, ui_progress=None):
      quantaxis/QUANTAXIS/QAUtil/__init__.py:from QUANTAXIS.QAUtil.QALogs import (QA_util_log_debug, QA_util_log_expection,
      quantaxis/QUANTAXIS/__init__.py:    QA_util_log_expection,
      ```

### `QAAuth.py`

1. 空文件

### `QACfg.py`

1. 废弃函数

### `QACode.py`

1. 修改 `QA_util_code_tostr` 函数，增加对 '天软', '掘金', '聚宽', '万得' 股票代码转换支持
