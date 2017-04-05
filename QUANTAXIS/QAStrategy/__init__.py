
# start_strategy
from .start_strategy import(QA_strategy_import,QA_strategy_choice,QA_strategy_start,QA_strategy_analysis)

from ..QASignal import (QA_signal_resend,QA_signal_send)

from ..QAARP import (QAAccount,QAPortfolio,QARisk)

from ..QAMarket import deal

from ..QAUtil import QA_util_log_info, QA_util_log_expection

from ..QAUtil import QA_util_sql_mongo_setting

"""
- 首先引入策略到空间，并按id存入数据库（QA_strategy_import，QA_util_sql_mongo_setting）
- 选择策略QA_strategy_choice
- 初始化策略 并运行QA_strategy_start，初始化QAAccount,QAPortfolio,QARisk
- 生成信号，并来回状态传值，日志记录 QA_signal_resend,QA_signal_send，QA_util_log_info,                                                    QA_util_log_expection
- 判断是否交易 deal
- 更新QAAccount,QAPortfolio,QARisk
- 更新信号 QA_signal_resend,QA_signal_send
- 更新策略 


- 结束 QA_strategy_analysis，日志记录QA_util_log_info, QA_util_log_expection



"""