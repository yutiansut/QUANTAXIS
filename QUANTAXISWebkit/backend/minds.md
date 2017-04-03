# 我们需要一个什么样的后台


1.能实时爬取数据
2.能部署到服务器,实时部署
3.存取数据,实时更新(定时/响应式更新)
4.用户的登录,策略的存贮
5.爬虫的部署/启停

后台要有一个一直能跑的爬虫,还需要一些按需爬取的爬虫

对于数据库

1.股票数据
    日线,周线
2.新闻数据
    url/下载后的
3.实时数据


1.索引链[url/title/website]
2.内容库[url/title/website/content/poster/time/tags/comments]
3.hot数据库(redis)
4.历史数据库[datas]
5.用户数据库[id/user/mail/password/strategy:id/result:id]
user:id/post:id


数据接口
### apis/data/
### apis/content/
### users/personal
    * users/personal/login?name=xxx&password=xxx
    * users/personal/signup?name=xxx&password=xxx
    * users/personal/update?name=xx|password=xxx|mail=xxx
### users/strategy
    * users/strategy/new?
    *



users{
    'id':'xxx',
    'name':'xxx',
    'password':'xxx',
    'mail':'xxx'
}

post
{
    
}