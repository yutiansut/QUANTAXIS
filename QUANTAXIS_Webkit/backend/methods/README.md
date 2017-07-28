## 交易数据

## 1. 获取个股历史数据
```
const options = {
  code: '600848',
  ktype: 'week'
};
stock.getHistory(options).then(({ data }) => {
  console.log(data);
});

```

`options` 参数说明：
```
{
code: {String} 股票代码，6位数字代码
ktype: {String} 数据类型，day=日k线 week=周 month=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为day
start: {String} 开始日期，格式YYYY-MM-DD
end: {String} 结束日期，格式YYYY-MM-DD
}
```

## 2. 获取历史分笔数据
```
const options = {
  code: '600848',
  date: '2015-12-31'
};
stock.getTick(options).then(({ data }) => {
  console.log(data);
});
```

`options` 参数说明：
```
{
  date: {String} 历史分笔日期，格式YYYY-MM-DD
  code: {String} 股票代码，6位数字代码
}
```

## 3. 实时行情
```
stock.getTodayAll().then(({ data }) => {
  console.log(data);
});
```

`options(可选)` 参数说明：
```
{
  pageSize: 设置单次返回股票的数量，默认10000，即全部股票
  pageNo: 页码，都懂得
}
```

## 4. 实时分笔
```
var options = {
  codes: [
    '600848',
    '600000'
  ]
};
stock.getLiveData(options).then(({ data }) => {
  console.log(data);
});
```

`options` 参数说明：
```
{
  codes: 股票代码数组
}
```

## 5. 当日历史分笔
>该方法返回指定时间前五分钟的分笔数据，如需获得所有数据，需要多次调用该方法

```
var options = {
  code: '600848',
  end: '15:00:00'
};
stock.getTodayTick(options).then(({ data }) => {
  console.log(data);
});
```

`options` 参数说明：
```
{
  code: 股票代码，6位数字
  end: 结束时间
}
```

## 6. 大盘指数行情数据
```
stock.getIndex().then(({ data }) => {
  console.log(data);
});
```

## 7. 大单交易数据
```
var options = {
  code: '600848',
  volume: 700
};
stock.getSinaDD(options).then(({ data }) => {
  console.log(data);
});
```

`options` 参数说明：
```
{
  code: 股票代码，6位数字
  volume: (手)默认400，返回大于xx手的大单数据
}
```

## 行业分类数据

## 1. 获取新浪行业分类信息
比如：房地产、电子信息、钢铁行业等等新浪行业分类信息
```
stock.getSinaIndustryClassified().then(({ data }) => {
  console.log(data);
});
```

## 2. 获取新浪某个行业分类的具体信息：所包含的股票及其交易信息
这里的tag是分类行业分类的tag，可以从上一个接口：tushare.stock.getSinaIndustryClassified获得
```
var options = {
  tag: 'new_jrhy'
};
stock.getSinaClassifyDetails(options).then(({ data }) => {
  console.log(data);
});
```

`options` 参数说明：
```
{
  tag: 新浪行业代码
}
```

## 3. 获取新浪概念分类信息
返回数据中的tag可用于上面（#2）的接口，用于获取某个概念分类的具体信息
```
stock.getSinaConceptsClassified().then(({ data }) => {
  console.log(data);
});
```

## 4. 获取所有上市公司股票基本信息
```
stock.getAllStocks().then(({ data }) => {
  console.log(data);
});
```

## 5. 获取沪深300股票信息
```
stock.getHS300().then(({ data }) => {
  console.log(data);
});
```

## 6. 获取上证50股票信息
```
stock.getSZ50().then(({ data }) => {
  console.log(data);
});
```

## 龙虎榜

## 1. 龙虎榜单（来自网易财经）
```
  var options = {
    start: '2016-01-15',
    end: '2016-01-15',
    pageNo: 1,
    pageSize: 150
  };
  stock.lhb(options).then(({ data }) => {
    console.log(data);
  });
```

`options` 参数说明：
```
{
start: 开始日期
end: 结束日期
pageNo: （optional, default: 1）
pageSize: optional, default: 150）
}
```

## 2. 大宗交易（来自网易财经）
```
  var options = {
    start: '2016-01-15',
    end: '2016-01-15',
    pageNo: 1,
    pageSize: 150
  };
  stock.blockTeade(options).then(({ data }) => {
    console.log(data);
  });
```

`options` 参数说明：
```
{
start: 开始日期
end: 结束日期
pageNo: （optional, default: 1）
pageSize: optional, default: 150）
}
```
