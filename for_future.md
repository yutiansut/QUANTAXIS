# QUANTAXIS 在下面的预计改进
2017/7/24

##  web部分的改进


- 参考https://github.com/puikinsh/gentelella的后台管理框架 增加一些功能
- 后台部分(backend)将尽量在python框架内部实现,依然在3000端口


## python部分

- 数据源问题应该得到高度重视
- 回测部分的优化
- 新增一个画图方式 参考https://github.com/chenjiandongx/pyecharts
- 状态的管理  需要重点优化
- 分钟级别和日线级别混合回测
- 框架的指标需要更新, 参考https://github.com/cedricporter/funcat


## 预计的重大改动

- web端的后台用python实现, 同时这个后台需要负责整个回测框架的状态管理
- 策略的易接入性


## 易用性改进

- 需要一个基于装饰器的能快速实现二次开发的模块 参考https://github.com/littlecodersh/danmu
