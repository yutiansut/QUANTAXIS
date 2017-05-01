var express = require('express');
var router = express.Router();
var mongodb=require('mongodb');
var exec = require('child_process').exec;

/* GET home page. */
router.get('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});

router.get('/python/getfuture',function(req,res,next){
    var cmd = 'python C:/quantaxis/data/wind/getfuture.py';
    exec(cmd, function callback(error, stdout, stderr) {
        console.log(stdout);
        res.send(stdout)
    });
});

router.get('/python/spider',function(req,res,next){
    var cmd = 'python C:/quantaxis/data/spider/wallstreetcn/begin.py';
    exec(cmd, function callback(error, stdout, stderr) {
        console.log(stdout);
        res.send(stdout)
    });
});

module.exports = router;
