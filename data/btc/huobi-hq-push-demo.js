//
// 火币实时行情push演示
// 注意socket.io-client版本是用的0.9.16版本的，最新版本的socket.io可能有兼容问题，连接不上推送服务器。
// 在node命令行下执行:node huobi-hq-push-demo.js
// node.js下socket.io版本请用0.9.16：安装命令：npm install socket.io-client@0.9.16。
// 其他语言请用找开源是socket.io实现，即可连接火币实时行情推送服务器。
//

var g_isConnect = 0;

// 获取错误信息
exports.dumpError = function(err) {
    var errMsg = '';
    
    if (typeof err === 'object') {
        if (err.message) {
            errMsg = '\nMessage: ' + err.message;
        }
        if (err.stack) {
            errMsg += '\nStacktrace:';
            errMsg += '====================';
            errMsg += err.stack;
        }
    } else {
        errMsg = '\ndumpError :: argument is not an object';
    }
    
    return errMsg;
}

// 写入到错误日志文件
exports.quicklog = function(s) {
    var logpath = "./error.log";
    var fs = require('fs');
    s = s.toString().replace(/\r\n|\r/g, '\n'); // hack
    var fd = fs.openSync(logpath, 'a+', 0666);
    fs.writeSync(fd, s + '\n');
    fs.closeSync(fd);
}

exports.systemlog = function(s) {
    console.log(s);
}


// 检查推送的数据完整性
exports.checkConnection = function() {
    try {
        exports.systemlog("checkConnection start");

        if(g_isConnect == 2)
        {
            exports.systemlog("checkConnection checking");
            exports.connect();
        }
    } catch(err) {
        var errMsg = exports.dumpError(err);
        exports.quicklog(errMsg);
    }
};

var io = require('socket.io-client');
        
exports.connect = function() {
    try {
        if(g_isConnect == 3)
        {
            console.log('websocket client is connecting to push server:');
            return;
        }
        
        g_isConnect = 3;
    
        var option = {'force new connection': true, reconnection: true};
        var socket = io.connect('hq.huobi.com:80', option);
    
        console.log('websocket client connecting to push server:');

        socket.on('connect', function(){
            g_isConnect = 1;
            console.log('websocket client connect to push server:' + socket.socket.sessionid);

            // 需要什么数据就可以注册对应的消息。
            // 比特币
            // 请求top市场深度
//            var strMsg = '{"symbolId":"btccny","version":1,"msgType":"reqMarketDepthTop","requestIndex":1405131204513}';

            // 实时数据推送
			var strMsg = '{"symbolList":{"lastTimeLine":[{"symbolId":"btccny","pushType":"pushLong"}],'
					+                   '"lastKLine":[{"symbolId":"btccny","pushType":"pushLong","period":"1min"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"5min"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"15min"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"30min"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"60min"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"1day"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"1week"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"1mon"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","period":"1year"}'
					+                                  '],'
					+                   '"marketDepthDiff":[{"symbolId":"btccny","pushType":"pushLong","percent":"10"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","percent":"20"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","percent":"50"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","percent":"80"},'
					+                                  '{"symbolId":"btccny","pushType":"pushLong","percent":"100"}'
					+                                  '],'
					+                   '"marketDepthTopDiff":[{"symbolId":"btccny","pushType":"pushLong"}],'
					+                   '"marketDetail":[{"symbolId":"btccny","pushType":"pushLong"}],'
					+                   '"tradeDetail":[{"symbolId":"btccny","pushType":"pushLong"}],'
					+                   '"marketOverview":[{"symbolId":"btccny","pushType":"pushLong"}]'
					+                  '},"version":1,"msgType":"reqMsgSubscribe","requestIndex":1404103038520}';

            
//            // 莱特币
//			var strMsg = '{"symbolList":{"lastTimeLine":[{"symbolId":"ltccny","pushType":"pushLong"}],'
//					+                   '"lastKLine":[{"symbolId":"ltccny","pushType":"pushLong","period":"1min"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"5min"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"15min"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"30min"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"60min"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"1day"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"1week"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"1mon"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","period":"1year"}'
//					+                                  '],'
//					+                   '"marketDepthDiff":[{"symbolId":"ltccny","pushType":"pushLong","percent":"10"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","percent":"20"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","percent":"50"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","percent":"80"},'
//					+                                  '{"symbolId":"ltccny","pushType":"pushLong","percent":"100"}'
//					+                                  '],'
//					+                   '"marketDepthTopDiff":[{"symbolId":"ltccny","pushType":"pushLong"}],'
//					+                   '"marketDetail":[{"symbolId":"ltccny","pushType":"pushLong"}],'
//					+                   '"tradeDetail":[{"symbolId":"ltccny","pushType":"pushLong"}],'
//					+                   '"marketOverview":[{"symbolId":"ltccny","pushType":"pushLong"}]'
//					+                  '},"version":1,"msgType":"reqMsgSubscribe","requestIndex":1404103038520}';

            
            var json = JSON.parse(strMsg);
            socket.emit('request', json);
        });
        
        socket.on('disconnect', function(){
            g_isConnect = 2;
            console.log('websocket client disconnect from push server:' + socket.socket.sessionid);
        });
    
        socket.on('reconnect', function(){
            g_isConnect = 1;
            console.log('websocket client reconnect from push server:' + socket.socket.sessionid);
        });
        
        socket.on('message', function(data) {
            console.log(JSON.stringify(data));
        });
        
        socket.on('request', function(data) {
            console.log(JSON.stringify(data));
        });
        console.log(strMsg)
    } catch(err) {
        var errMsg = exports.dumpError(err);
        exports.quicklog(errMsg);
    }
};


exports.connect();

var g_checkTimerEvent = setInterval(exports.checkConnection,
            5000);
