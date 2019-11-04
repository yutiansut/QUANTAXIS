"""
定义一些单因子分析常用常量
"""

PRICE_TYPE = ["open", "high", "low", "close", "avg"]

FQ_TYPE = ["pre", "qfq", "前复权", "hfq", "post", "后复权", "none", "不复权", "bfq"]

INDUSTRY_CLS = ["jq_l1", "jq_l2", "sw_l1", "sw_l2", "sw_l3", "zjw", "none"]

WEIGHT_CLS = [
    "avg",
    "mktcap",
    "cmktcap",
    "ln_mktcap",
    "ln_cmktcap",
    "sqrt_mktcap",
    "sqrt_cmktcap",
]

FREQUENCE_TYPE = ["min", "d", "w", "m", "q", "y"]

DECIMAL_TO_BPS = 10000

DAYS_PER_WEEK = 5
DAYS_PER_MONTH = 20
DAYS_PER_QUARTER = 61
DAYS_PER_YEAR = 243
