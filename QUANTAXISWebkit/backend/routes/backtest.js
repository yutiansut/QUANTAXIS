var express = require('express');
var router = express.Router();
var fs = require('fs');
var superagent = require('superagent');
var cheerio = require('cheerio');
var axios = require('axios');
var http = require('http'); 
var events = require('events');
var mongodb=require('mongodb')
var request = require('superagent');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Backtest' });
});

router.get('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});

//http://localhost:3000/backtest/info?name=yutiansut
router.get('/info',function(req, res, next) {
  console.log('backtest')
  name=req.query.name
  console.log(req.query.name)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
        conn.collection('backtest_info', function (err, coll) {
          coll.find({'user': name }).toArray(function (err, docs) {
            res.send(docs)
          
        })
      })

})
});

router.get('/history',function(req, res, next) {
  
  cookie=req.query.cookie
  console.log(cookie)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
        conn.collection('backtest_history', function (err, coll) {
          coll.find({'cookie':cookie}).toArray(function (err, docs) {
            console.log(docs.length)
            res.send(docs[docs.length-1])
          
        })
      })

})
});
module.exports = router;