# 关于数据的维护/下载/更新


## 数据下载/更新

quantaxis使用了mongodb作为数据库存储,目前提供两种数据下载的方式

1. CLI 命令行下载
2. 更新脚本下载

### QUANTAXIS CLI下载指令



|    指令             |              详细内容                        |                            说明                      | 
| --------------- | ---------------------------------------------   | -------------------------------------------- | 
| save all            | save stock_day/xdxr/ index_day/ stock_list         | 存储/更新 股票日线/权息 指数日线 股票列表   | 
| save X 或save x     | save stock_day/xdxr/min index_day/min etf_day/min stock_list/block   | 存储/更新 股票日线/权息/分钟线 指数日线/分钟线 ETF日线/分钟线 股票列表/版块列表   | 
| save day            | save stock_day/xdxr index_day etf_day stock_list         | 存储/更新 股票日线/权息 指数日线 ETF日线 股票列表   | 
| save min            | save stock_day/xdxr index_day etf_day stock_list         | 存储/更新 股票分钟线/权息 指数分钟线 ETF分钟线 股票列表   | 
| | |
| save stock_day             | save stock_day | 存储/更新 股票日线  | 
| save stock_xdxr             | save stock_xdxr| 存储/更新 股票权息  | 
| save stock_min             | save stock_min | 存储/更新 股票分钟线  | 
| save index_day             | save index_day | 存储/更新 指数日线  | 
| save index_min             | save index_min | 存储/更新 指数分钟线  | 
| save etf_day             | save etf_day | 存储/更新 ETF日线  | 
| save etf_min             | save etf_min | 存储/更新 ETF分钟线  | 
| save stock_list         | save stock_list| 存储/更新 股票列表|
| save stock_block        | save stock_block | 存储/更新 股票版块|
| save stock_info         | save stock_info  | 存储/更新 股票财务数据表|
| save financialfiles     | save financialfiles | 存储/更新 财务报表


### 更新脚本

参考 [```update_data.py```](https://github.com/QUANTAXIS/QUANTAXIS/blob/master/config/update_data.py)脚本

可以使用linux系统的crontab以及windows系统的定时执行计划(组策略)来定时执行更新脚本
