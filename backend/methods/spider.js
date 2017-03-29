var fs = require('fs');
var superagent = require('superagent');
var cheerio = require('cheerio');
var axios = require('axios');
var http = require('http'); 
var events = require('events');

var emitter = new events.EventEmitter()

function Spider (options) {
    var self = this;
    options = options||{};  
    self.init(options);
    self.res= function(){
        console.log('g')
    }
}

Spider.prototype.init = function init (options){
    var self = this;
    self.useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
    console.log('init')
}

Spider.prototype.request = function request (url,callback){
    console.log(this.useragent)
    var response='';
    var req=superagent
            .get(url) 
            .set({
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
            })
            .set({
                'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            })
            .set({
                'accept-encoding' : 'gzip, deflate, sdch, br'
            })
            .set({
                'Accept-Language':'zh-CN,zh;q=0.8,Cache-Control:max-age=0',
                'connection' : 'keep-alive'
            })

            .end(function(err,res){
                if(err)throw err;
                var $ =cheerio.load(res.text);
                var text =$('.t').text();
                console.log('textInside:'+text)
                response=text;
                return response
            });

};
module.exports=Spider;


