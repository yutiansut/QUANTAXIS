var express = require('express');
var router = express.Router();
var sqlexec = require('../mysql/sqlexec.js');
var fs = require("fs");

router.get('/', function (req, res, next) {
    //res.send('respond with a resource');
    sqlexec.querytable(req, res, next);
});

router.get('/show', function (req, res, next) {
    //res.send('respond with a resource');

    console.log('按ID查询数据');
    console.log('req.url=' + req.url);
    console.log('req.body=' + req.body);
    
    fs.writeFile("aa.txt", req, function (err) {
        if (err) throw err;
        console.log("File Saved !"); //文件被保存
    });
    console.log('req.body.name=' + JSON.stringify(req.body));
    
    //   sqlexec.queryByName(req, res, next);

});
module.exports = router;