//用于测试superagent
//测试部分是http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml


var cheerio = require('cheerio');
var request = require('superagent-charset');

var ggtj =exports.ggtj =function(){
     var testx=request
                .get('http://vip.stock.finance.sina.com.cn/q/go.php/vLHBData/kind/ggtj/index.phtml')
                .charset('gbk')
                .end(function(err,res){
                    var $ = cheerio.load(res.text);
                    var test= $('#dataTable').text();
                    return this.test
                })
    console.log(testx)

}

//result
/**
 *          300052
            中青宝
            1
            14246
            5945.46
            8300.54
            5
            5
 * 
 */