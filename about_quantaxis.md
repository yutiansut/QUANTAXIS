
QUANTAXIS

## 数据结构

QUANTAXIS 的核心数据是DATASTRUCT,datastruct目前是基于pandas.DataFrame的一个结构.
QUANTAXIS支持5种类型的数据结构:


- list
- numpy ndarray
- json/dict
- pandas dataframe,series
- DATASTRUCT

从速度和性能考虑, dict是取出速度最快的结构, 可以作为临时的缓存使用. numpy因为cython加速的原因,在运算的过程中速度最快, pandas的索引导致他的计算较慢,但比较人性化


## 统一数据接口

```python
QA.QA_quoation(code, start, end, frequence, market, source, output)
    code {str/list} -- 证券/股票的代码
    start {str} -- 开始日期
    end {str} -- 结束日期
    frequence {enum} -- 频率 QA.FREQUENCE
    market {enum} -- 市场 QA.MARKET_TYPE
    source {enum} -- 来源 QA.DATASOURCE
    output {enum} -- 输出类型 QA.OUTPUT_FORMAT
```

