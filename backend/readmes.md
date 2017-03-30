var fs = require('fs');//为了将抓取的图片存到本地，使用fs
var superagent = require('superagent');//引入superagent
var cheerio = require('cheerio');//引入jquery实现
 
var filePath = '/node/学习/sis/img/';//定义抓取妹子文件存放路径
var count = 0;//记录抓取数量
var test = [];
//抓取一个页面的实现。
var getOnePage = function(url){
    //因为煎蛋对请求做了限制，所以将cookie加上了。如果你要访问该网站的话，可以通过浏览器查找cookie 并进行替换
    superagent.get(url)
    .set({
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    })
    .set('cookie','500322148=53; Hm_lvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1454117846; Hm_lpvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1454119909')
    .set({
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'connection' : 'keep-alive',
        'host' : 'jandan.net'
    })
    .end(function(err,sres){//这里是对获取的dom进行处理
        if(err)throw err;
        var $ = cheerio.load(sres.text);
        var nextUrl = $('.previous-comment-page').attr('href');//获得下一页的链接，为了开始下一次请求
        $('img').each(function(index,ele){//循环该页面的所有图片并得到对应的链接，放进数组。
            var u = '';
            if($(ele).attr('org_src')){
                u = $(ele).attr('org_src');
            }else{
                u = $(ele).attr('src');    
            }
            test.push(u);
            //通过superagent 获取图片数据，并保存到本地。
            superagent.get(u).end(function(err,sres){
                if(err)throw err;
                //根据访问路径获得文件名称
                var ttt = u.split('/');
                var name = ttt[ttt.length-1];
                var path = filePath+name
                fs.writeFile(path,sres.body,function(){
                    count++;
                    console.log(u);
                    console.log('已成功抓取..'+count+'张');
                });
            });
        });
        if(null != nextUrl && '' != nextUrl){ //何时开始下一次请求
            getOnePage(nextUrl);
        }
    }); 
 
};
 
getOnePage('http://jandan.net/ooxx/');//触发第一次请求开始