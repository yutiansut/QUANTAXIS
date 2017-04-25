var cheerio = require('cheerio');
var request = require('superagent-charset');
var express = require('express');
var path = require('path');
var app = express();


app.get('/',function(req,res,next){
    request
    .get('http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml')
    .charset('gbk')
    .end(function(err,resx){
        var $ = cheerio.load(resx.text);
        res.send($('#dataTable').text())
})
});
app.listen(3010);