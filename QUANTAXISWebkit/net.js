
var http = require('http');
var https = require('https');
var url=require("url");
var pass = require('stream').PassThrough;

var getHeader = function (req) {
    var ret = {};
    for (var i in req.headers) {
        if (!/host|connection|Access-|origin|referer|user-agent|__user|__path|__url|__method|__headers/i.test(i)) {
            ret[i] = req.headers[i];
        }
    }
    var headers=req.headers["__headers"];
    if(headers)
    {
        headers=JSON.parse(headers);
        for(var key in headers)
        {
            ret[key]=headers[key];
        }
    }
    return ret
};

var filterResHeader = function (headers) {
    var ret = {};
    for (var i in headers) {
        if (!/Access-/i.test(i)) {
            ret[i] = headers[i];
        }
    }
    return ret;
};

var getPath = function (req) {
    var url = req.url;
    if (url.substr(0, 7).toLowerCase() === 'http://') {
        var i = url.indexOf('/', 7);
        if (i !== -1) {
            url = url.substr(i);
        }
    }
    return url;
};

function getHost(req) {
    var url=req.headers["__url"];
    url=url.replace(/^(http:\/\/|https:\/\/)/i,"");
    var arr=url.split(":");
    return arr[0];
}

function getPort(req) {
    var url=req.headers["__url"];
    var defaultPort;
    if(req.headers["__url"].toLowerCase().startsWith("https://"))
    {
        defaultPort=443;
    }
    else
    {
        defaultPort=80;
    }
    url=url.replace(/^(http:\/\/|https:\/\/)/i,"");
    var arr=url.split(":");
    return arr.length>1?arr[1]:defaultPort;
}

var onProxy = function (req, res) {
    handleHeader(req,res);
    if(req.method=="OPTIONS")
    {
        return;
    }
    if(!req.headers["__url"])
    {
        mock(req,res);
    }
    else
    {
        proxy(req,res);
    }
};

function mock(req,res) {
    var obj=url.parse(mockUrl);
    var path=req.headers.path || url.parse(req.url).path;
    var opt={
        host:     obj.hostname,
        path:     (obj.pathname=="/"?"":obj.pathname)+path,
        method:   req.method,
        headers:  getHeader(req),
        port:obj.port?obj.port:80,
    }
    if(opt.headers["content-length"])
    {
        delete opt.headers["content-length"]
    }
    var req2 = http.request(opt, function (res2) {
        if(!realUrl || res2.headers["__finish"]=="0")
        {
            res.writeHead(res2.statusCode, filterResHeader(res2.headers));
            res2.pipe(res);
            res2.on('end', function () {

            });
        }
        else
        {
            var headers=getHeader(req);
            var objUrl=url.parse(realUrl);
            var request1,opt1;
            if(objUrl.protocol=="http:")
            {
                opt1={
                    host:  objUrl.hostname,
                    path:     (objUrl.pathname=="/"?"":objUrl.pathname)+path,
                    method:   req.method,
                    port:objUrl.port?objUrl.port:80,
                    headers:headers
                }
                request1=http.request;
            }
            else
            {
                opt1={
                    host:  objUrl.hostname,
                    path:     (objUrl.pathname=="/"?"":objUrl.pathname)+path,
                    method:   req.method,
                    port:objUrl.port?objUrl.port:443,
                    headers:headers,
                    rejectUnauthorized: false,
                    requestCert: true,
                }
                request1=https.request;
            }
            var req3=request1(opt1,function (res3) {
                res.writeHead(res3.statusCode, filterResHeader(res3.headers));
                res3.pipe(res);
                res3.on('end', function () {

                });
            })
            if (/POST|PUT/i.test(req.method)) {
                stream.pipe(req3);
            } else {
                req3.end();
            }
            req3.on('error', function (err) {
                res.end(err.stack);
            });
        }
    });
    var stream;
    if (/POST|PUT/i.test(req.method))
    {
        stream=new pass();
        req.pipe(stream);
        req.pipe(req2);
    }
    else
    {
        req2.end();
    }
    req2.on('error', function (err) {
        res.end(err.stack);
    });
}

function handleHeader(req,res) {
    if(!req.headers.origin)
    {
        return;
    }
    res.setHeader("Access-Control-Allow-Origin", req.headers.origin);
    res.setHeader("Access-Control-Allow-Headers", "X-Requested-With");
    res.setHeader("Access-Control-Allow-Methods","PUT,POST,GET,DELETE");
    res.setHeader("Access-Control-Allow-Credentials","true");
    if(req.headers["access-control-request-headers"])
    {
        res.setHeader("Access-Control-Allow-Headers",req.headers["access-control-request-headers"])
    }
    res.setHeader("Access-Control-Expose-Headers","connection,content-length,date,x-powered-by,content-encoding,server,etag,accept-ranges,allow,content-language,set-cookie");
    if(req.method=="OPTIONS")
    {
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end();
        return;
    }
}

function redirect(res,bHttps,opt,location) {
    var urlRedirect=location;
    if(urlRedirect.startsWith("/"))
    {
        urlRedirect=(bHttps?"https://":"http://")+opt.host+urlRedirect;
    }
    var objUrl=url.parse(urlRedirect);
    var request1,opt1;
    if(objUrl.protocol=="http:")
    {
        opt1={
            host:  objUrl.hostname,
            path:     objUrl.path,
            method:   "GET",
            port:objUrl.port?objUrl.port:80,
            headers:opt.headers
        }
        request1=http.request;
        bHttps=false;
    }
    else
    {
        opt1={
            host:  objUrl.hostname,
            path:     objUrl.path,
            method:   "GET",
            port:objUrl.port?objUrl.port:443,
            headers:opt.headers,
            rejectUnauthorized: false,
            requestCert: true,
        }
        request1=https.request;
        bHttps=true;
    }
    var req3=request1(opt1,function (res3) {
        if(res3.statusCode==302)
        {
            redirect(res,bHttps,opt,res3.headers.location)
        }
        else
        {
            res.writeHead(res3.statusCode, filterResHeader(res3.headers));
            res3.pipe(res);
            res3.on('end', function () {

            });
        }
    })
    req3.end();
    req3.on('error', function (err) {
        res.end(err.stack);
    });
}

function proxy(req,res) {
    var bHttps=false;
    if(req.headers["__url"].toLowerCase().startsWith("https://"))
    {
        bHttps=true;
    }
    var opt,request;
    if(bHttps)
    {
        opt= {
            host:     getHost(req),
            path:     req.headers["__path"],
            method:   req.headers["__method"],
            headers:  getHeader(req),
            port:getPort(req),
            rejectUnauthorized: false,
            requestCert: true,
        };
        request=https.request;
    }
    else
    {
        opt= {
            host:     getHost(req),
            path:     req.headers["__path"],
            method:   req.headers["__method"],
            headers:  getHeader(req),
            port:getPort(req)
        };
        request=http.request;
    }
    var req2 = request(opt, function (res2) {
        if(res2.statusCode==302)
        {
            redirect(res,bHttps,opt,res2.headers.location)
        }
        else
        {
            res.writeHead(res2.statusCode, filterResHeader(res2.headers));
            res2.pipe(res);
            res2.on('end', function () {

            });
        }
    });
    if (/POST|PUT/i.test(req.method)) {
        req.pipe(req2);
    } else {
        req2.end();
    }
    req2.on('error', function (err) {
        res.end(err.stack);
    });
}

var arguments = process.argv.splice(2);
var mockUrl=arguments[0];
var realUrl=arguments[1];
var server = http.createServer(onProxy);
server.listen(36742);
console.log(arguments.length>0?"内网测试，Mock数据正待命运行中！":"正在运行中，请用SBDoc的接口测试页面进行内网测试！");



