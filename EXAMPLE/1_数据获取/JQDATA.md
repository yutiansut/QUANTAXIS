

```python
from jqdatasdk import *
from pyecharts import  Kline,Bar,Grid
```

首先我们先应JQDATA 的活动演示一下如何调用pyecharts 画图


```python
auth('acc','password')
data=get_price('000001.XSHE')
```

    auth success
    

先打印下 data
我们可以看到  jqdata返回的格式是 一个单index的Dataframe


```python

data.head()
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>open</th>
      <th>close</th>
      <th>high</th>
      <th>low</th>
      <th>volume</th>
      <th>money</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2015-01-05</th>
      <td>10.53</td>
      <td>10.55</td>
      <td>10.72</td>
      <td>10.27</td>
      <td>434357784.0</td>
      <td>4.565388e+09</td>
    </tr>
    <tr>
      <th>2015-01-06</th>
      <td>10.44</td>
      <td>10.39</td>
      <td>10.79</td>
      <td>10.24</td>
      <td>328971478.0</td>
      <td>3.453446e+09</td>
    </tr>
    <tr>
      <th>2015-01-07</th>
      <td>10.25</td>
      <td>10.19</td>
      <td>10.42</td>
      <td>10.08</td>
      <td>258163619.0</td>
      <td>2.634796e+09</td>
    </tr>
    <tr>
      <th>2015-01-08</th>
      <td>10.21</td>
      <td>9.85</td>
      <td>10.25</td>
      <td>9.81</td>
      <td>213761656.0</td>
      <td>2.128003e+09</td>
    </tr>
    <tr>
      <th>2015-01-09</th>
      <td>9.81</td>
      <td>9.93</td>
      <td>10.45</td>
      <td>9.69</td>
      <td>380916192.0</td>
      <td>3.835378e+09</td>
    </tr>
  </tbody>
</table>
</div>



在画K线图的时候, 我们需要的是上下两个部分
![](http://pic.yutiansut.com/jq.png)


```python

# 因此我们初始化2个部分

kline=Kline(width=1360, height=700, page_title='000001')

bar = Bar()


```

然后我们需要对数据进行初步的处理:

- 首先处理横坐标轴(时间轴)
- 分别处理 价格轴/量轴


```python
import numpy as np
import pandas as pd

# 做横轴的处理
datetime = np.array(data.index.map(str))
```


```python
ohlc = np.array(data.loc[:, ['open', 'close', 'low', 'high']])
vol = np.array(data.volume)
```

将数据加载到kline和bar中


```python
kline.add('000001', datetime, ohlc, mark_point=[
      "max", "min"], is_datazoom_show=False, datazoom_orient='horizontal')

bar.add('000001', datetime, vol,
        is_datazoom_show=True,
        datazoom_xaxis_index=[0, 1])
```

使用Grid组合两个图


```python
grid = Grid(width=1360, height=700, page_title='QUANTAXIS')
grid.add(bar, grid_top="80%")
grid.add(kline, grid_bottom="30%")

```


```python
grid.render('000001_plot.html')
```

使用 webbrowser 打开并渲染这个图
![](http://pic.yutiansut.com/QQ%E6%88%AA%E5%9B%BE20181109203715.png)


```python
import webbrowser
webbrowser.open('000001_plot.html')
```




    True




```python
"""
以上是jqdata和pyecharts的结合, 不过QUANTAXIS已经对于这些进行了封装  只需要转化jqdata获取回来的数据为QADataStruct即可
"""
```




    '\n以上是jqdata和pyecharts的结合, 不过QUANTAXIS已经对于这些进行了封装  只需要转化jqdata获取回来的数据为QADataStruct即可\n'




```python
import QUANTAXIS as QA
```


```python
qads=QA.QAData.QA_DataStruct_Stock_day(data.assign(date=data.index,code='000001').set_index(['date','code']))
```


```python
qads
```




    < QA_DataStruct_Stock_day with 1 securities >




```python
qads.plot('000001')
```

    QUANTAXIS>> The Pic has been saved to your path: .\QA_stock_day_000001_bfq.html
    
