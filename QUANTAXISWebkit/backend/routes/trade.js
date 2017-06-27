var express = require('express');
var router = express.Router();
var fs = require('fs');
var superagent = require('superagent');
var cheerio = require('cheerio');
var axios = require('axios');
var http = require('http');
var events = require('events');
var mongodb = require('mongodb')
var request = require('superagent');
router.get('*', function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
  res.header("X-Powered-By", ' 3.2.1')
  res.header("Content-Type", "application/json;charset=utf-8");
  next();
});

/* GET home page. */
router.get('/', function (req, res, next) {
  res.render('index', {
    title: '实盘查询接口'
  });
})

router.get('/history', function (req, res, next) {
  //console.log('backtest')

  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('trade_stock', function (err, coll) {
      coll.find().toArray(function (err, docs) {
        res.send(docs)

      })
    })

  })
});

router.get('/lastest', function (req, res, next) {
  //console.log('backtest')

  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('trade_stock', function (err, coll) {
      coll.find().toArray(function (err, docs) {
        res.send(docs[docs.length - 1])

      })
    })

  })
});



module.exports = router;