# QUANTAXIS 的后台api

<!-- vscode-markdown-toc -->
* 1. [后端的标准和格式规范](#)
	* 1.1. [基础标准](#-1)
* 2. [命名格式](#-1)
* 3. [后端的实现方式和注意事项](#-1)
	* 3.1. [跨域支持](#-1)
		* 3.1.1. [Flask](#Flask)
		* 3.1.2. [Tornado](#Tornado)
		* 3.1.3. [express](#express)
	* 3.2. [权限](#-1)
* 4. [必须实现的部分](#-1)
	* 4.1. [用户管理 /user](#user)
		* 4.1.1. [登陆](#-1)
		* 4.1.2. [注册](#-1)
	* 4.2. [回测部分 /backtest](#backtest)
		* 4.2.1. [回测概览(列表查询)](#-1)
		* 4.2.2. [单个回测结果查询()](#-1)
	* 4.3. [行情查询部分 /marketdata & /data](#marketdatadata)
		* 4.3.1. [URI总规则 GENERAL URI RULE](#URIGENERALURIRULE)
		* 4.3.2. [股票日线 STOCK DAY](#STOCKDAY)
		* 4.3.3. [股票分钟线 STOCK MINDATA](#STOCKMINDATA)
		* 4.3.4. [股票实时上下五档 STOCK REALTIME 5-ASK/BID](#STOCKREALTIME5-ASKBID)
		* 4.3.5. [股票分笔数据 STOCK TRANSACTION](#STOCKTRANSACTION)
		* 4.3.6. [股票财务数据](#-1)
		* 4.3.7. [期货日线](#-1)
		* 4.3.8. [期货分钟线](#-1)
	* 4.4. [实时行情推送 /quotation](#quotation)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


quantaxis 采用前后端分离的模式开发,所以对于后端而言 是一个可以快速替换/语言随意的部分.只需要按照规则设置好REST的url即可


##  1. <a name=''></a>后端的标准和格式规范

###  1.1. <a name='-1'></a>基础标准

quantaxis的后台可以用 nodejs(express/koa), python(flask/django/tornado), go 等等语言实现

quantaxis的后台部分主要是作为微服务,给前端(web/client/app)等提供标准化的查询/交互接口


##  2. <a name='-1'></a>命名格式

quantaxis的后台命名格式

http://ip:port/功能(backtest/marketdata/user/..)/细分功能(info/query_code/..)

example:

```
http://localhost:3000/backtest/info_cookie?cookie=xxxxx  ==>  按backtest的cookie查询backtest的信息

```

##  3. <a name='-1'></a>后端的实现方式和注意事项


###  3.1. <a name='-1'></a>跨域支持

因为是前后端分离的模式, 需要对于url采取跨域允许

跨域在python中的实现

####  3.1.1. <a name='Flask'></a>Flask

```python
@app.route("/status")
def status():
    rst = make_response(jsonify('200'))
    rst.headers['Access-Control-Allow-Origin'] = '*'
    rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    allow_headers = "Referer,Accept,Origin,User-Agent"
    rst.headers['Access-Control-Allow-Headers'] = allow_headers
    return rst

```


####  3.1.2. <a name='Tornado'></a>Tornado

```python
class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        print（"setting headers!!!"）
        self.set_header("Access-Control-Allow-Origin", "*") # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def post(self):
        self.write('some post')

    def get(self):
        self.write('some get')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()
```

跨域在nodejs中的实现

####  3.1.3. <a name='express'></a>express

```javascript

router.get('*', function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
  res.header("X-Powered-By", ' 3.2.1')
  res.header("Content-Type", "application/json;charset=utf-8");
  next();
});

```

###  3.2. <a name='-1'></a>权限

后台服务需要保护好隐私不被泄露,避免路径攻击和端口暴露等问题

##  4. <a name='-1'></a>必须实现的部分


###  4.1. <a name='user'></a>用户管理 /user

####  4.1.1. <a name='-1'></a>登陆
```
http://[ip]:[port]/users/login?name=[]&password=[]
```
####  4.1.2. <a name='-1'></a>注册
```
http://[ip]:[port]/users/signup?name=[]&password=[]
```

###  4.2. <a name='backtest'></a>回测部分 /backtest

####  4.2.1. <a name='-1'></a>回测概览(列表查询)
```
http://[ip]:[port]/backtest/list?user=[]
```

####  4.2.2. <a name='-1'></a>单个回测结果查询()
```
http://[ip]:[port]/backtest/info?cookie=[]
```

###  4.3. <a name='marketdatadata'></a>行情查询部分 /marketdata & /data

功能性的API,分别代表着 日线/分钟线/实时(5档)/分笔数据

####  4.3.1. <a name='URIGENERALURIRULE'></a>URI总规则 GENERAL URI RULE
```
总URI为 http://[ip]:[port]/[market_type]/[frequence]?code=[]&start=[]&end=[]
```

####  4.3.2. <a name='STOCKDAY'></a>股票日线 STOCK DAY
```
http://[ip]:[port]/marketdata/stock/day?code=[]&start=[]&end=[]
```

当不给定结束日期的时候,返回的就是直到当前的数据

####  4.3.3. <a name='STOCKMINDATA'></a>股票分钟线 STOCK MINDATA
```
http://[ip]:[port]/marketdata/stock/min?code=[]&start=[]&end=[]
```

当不给定结束日期的时候,返回的就是直到当前的数据

####  4.3.4. <a name='STOCKREALTIME5-ASKBID'></a>股票实时上下五档 STOCK REALTIME 5-ASK/BID
```
http://[ip]:[port]/marketdata/stock/realtime?code=[]
```

实时返回股票的L1上下五档的行情数据

####  4.3.5. <a name='STOCKTRANSACTION'></a>股票分笔数据 STOCK TRANSACTION
```
http://[ip]:[port]/marketdata/stock/transaction?code=[]&start=[]&end=[]
```
code 指的是具体的股票代码
start 指的是分笔开始的时间
end 指的是分笔结束的时间

####  4.3.6. <a name='-1'></a>股票财务数据
```
http://[ip]:[port]/marketdata/stock/info?code=[]&time=[]
```
code 指的是具体的股票
time 指的是时间段

如 code=000001 time=2018Q1 指的是000001的2018年1季度

time的格式为: YEAR['YYYY']+Q+times[1,2,3,4](1- 1季度财报 2- 半年度财报 3- 3季度财报 4- 年报)

####  4.3.7. <a name='-1'></a>期货日线
```
http://[ip]:[port]/marketdata/future/day?code=[]&start=[]&end=[]
```

####  4.3.8. <a name='-1'></a>期货分钟线
```
http://[ip]:[port]/marketdata/future/min?code=[]&start=[]&end=[]
```
###  4.4. <a name='quotation'></a>实时行情推送 /quotation
```
/quotation 推送指的是 建立一个websocket链接:
```
1. user login [Handler]

2. auth []

3. send_req [front end/client]

4. make connection

5. data transport
