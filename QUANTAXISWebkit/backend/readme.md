BACKEND

## APIS

localhost:3000/stock
### /stock/history/all?code=xxx&feq=xxx
### /stock/history/time?code=xxx&start=(yyyy-mm-dd)&end=(yyyy-mm-dd)
### /stock/index/
### /stock/live?code=xxx
### /stock/quota/lhb?
### /stock/quota/lhb?


localhost:3000/backtest
### /ts?bidCode=000001&bidTime=2001-01-04&bidPrice=4.08
返回Success  则成交 返回failed 则不成交
一定要给报价


localhost:3000/users
### /signup?username=xxx&password=xxx
### /login?username=xxx&password=xxx

localhost:3000/apis 
### /queryContentbyName
### /queryTitlebyName
### /queryContentbyTitle