# QUANTAXIS RUNTIME

QUANTAXIS致力于一个全生态链的闭环实现,因此, 当我们实现了历史数据的分析,处理,维护,回测以后, 实时的问题就摆在了眼前:


QUANTAXIS给出了如下的解决方案:


<!-- TOC -->

- [QUANTAXIS RUNTIME](#quantaxis-runtime)
    - [便捷开启实时行情快照收集](#便捷开启实时行情快照收集)
    - [数据采样:](#数据采样)
    - [数据重采样:](#数据重采样)
    - [数据合并 (QADataStruct 对于实时的支持)](#数据合并-qadatastruct-对于实时的支持)
    - [数据拆分 (QADataStruct 对于实时的支持)](#数据拆分-qadatastruct-对于实时的支持)

<!-- /TOC -->

基于以上, 我们就可以对于实时的行情,进行分析和处理


## 便捷开启实时行情快照收集

在交易时间段内, 使用命令行 ```quantaxisq```即可开启全市场行情快照扫描工具

会将市场行情数据收集进mongodb中


## 数据采样:

收集的数据,先使用```QA.QA_fetch_quotation```调取,可以使用``` QA.QA_data_tick_resample``` 进行采样和处理

一般来说我们会采样成1分钟线 剩余的级别使用1min线去合成

## 数据重采样:

对于其他级别的数据, 我们参考通达信,同花顺的处理方式

1分钟级别--合成5分钟级别 --合成15分钟级别--合成30分钟级别 -- 合成小时级别

1分钟级别--合成其他分钟级别


## 数据合并 (QADataStruct 对于实时的支持)

使用 QA.concat([QADataStruct1,QADataStruct2,....])可以将数据合并, 如 先收集好的分钟线数据+ 刚合成的数据--一起缓存

## 数据拆分 (QADataStruct 对于实时的支持)

使用 ```QA.QADataStruct.select_time/select_code/seletime_time_with_gap```都可以讲数据的任意时间段/股票选出来 实现数据拆分