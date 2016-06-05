# 关于DataFetch类

数据获取类

## 文件夹构成

>[DataFetch]<br>DFMain.m (类包函数，同时兼具初始化的任务)
>>[+Methods]工具函数<br> DFSina.m (新浪接口)<br> DFTushare.m (Python tushare接口)<br> DFWind.m (Wind 接口)<br> DFYahoo.m (Yahoo 接口)
>>>[+Core]<br> DFCore.m (核心包函数，指定该类的属性 FET 以及消息响应控制 MES族)


## 调用方式

```
classdef QAClassPackage< DataFetch.DFMain 
end

classdef QUANTAXIS < QAClassPackage
end
```
## 初始化
## Methods
