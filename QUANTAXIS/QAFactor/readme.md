# 关于 QAFactor


1. feature 的定义

feature 主要是对于行情/另类数据在股票池(全市场/自定义市场)的一个指标计算, 可以作为对于 QAIndicator 模块的衍生和进一步处理, 也可以直接作为因子投资框架下的基础的 feature 控制

我们并不直接把因子的研究框架内置在 feature 的定义中, 而是希望可以更多的存储初始状态的计算值, 以方便进行更全面的数据分析和最大程度的原始数据留存


你可以将原始的计算结果方便的保存在 clickhouse 中, 并对于 feature 通过 featureAnalysis 进一步的分析, 如中性化, 标准化等等, 并再次使用此 feature 基类进行存储和二次的读取, 基于 feature 自带的版本控制和 description 描述, 方便的管理因子迭代的过程


2. featureView 一个方便管理全量 feature 的基类

基于 featureView 你可以快速的管理多个 feature, 并进行组合和分析, 也可以对于版本进行控制, 支持模糊查询等


3. featureAnalysis

在 featureAnalysis 中, 我们可以对于原始 featue 进行进一步的加工和处理, 并可以定义新的 feature 形成一个迭代


