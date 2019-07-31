# 关于第三方数据的导入和使用



1. 关于数据的存储:


quantaxis对于数据的存储格式的要求较为松散, 满足几个核心的字段即可


### 1.3 future_min


[str(item['code']), float(item['open']), float(item['high']), float(
            item['low']), float(item['close']), float(item['position']), float(item['price']), float(item['trade']),
            item['datetime'], item['tradetime'], item['time_stamp'], item['date'], item['type']

- code
- open
- high
- low
- close
- position
- price     
- trade      
- datetime   真实时间
- tradetime  交易时间
- time_stamp 时间戳
- date  日期
- type  频率
