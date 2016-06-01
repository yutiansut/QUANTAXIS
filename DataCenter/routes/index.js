var express = require('express');
var router = express.Router();
var sqlexec = require('../mysql/sqlexec.js');
var fs = require("fs");

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/testajax', function(req, res, next) {
  res.render('test/testajax', { title: 'Exs' });
});

router.get('/ajax',function(req,res,next){
  console.log('Using Ajax methods');
 
  sqlexec.querytable(req, res, next);
});
router.get('/querybyid',function(req,res,next){
  console.log('querybyid methods');
  
  sqlexec.queryTableById(req, res, next);
  fs.writeFile("aa.json", res, function (err) {
        if (err) throw err;
        console.log("File Saved !"); //文件被保存
    });
});
module.exports = router;
