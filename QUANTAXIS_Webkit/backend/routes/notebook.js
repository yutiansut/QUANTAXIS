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

/* GET home page. */

router.get('*', function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
  res.header("X-Powered-By", ' 3.2.1')
  res.header("Content-Type", "application/json;charset=utf-8");
  next();
});




//http://localhost:3000/notebook/new
router.get('/new', function (req, res, next) {
  console.log('backtest')
  var title = req.query.title
  console.log(req.query.title)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('notebook', function (err, coll) {
      coll.insert({
        'title': title
      }, function (err, result) {
        res.send(result['ops'][0])
      })

    })
  })
});
router.get('/query', function (req, res, next) {
  var id = req.query.id
  var id_ = new mongodb.ObjectID(id)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('notebook', function (err, coll) {
      coll.find({
        '_id': id_
      }).toArray(function (err, docs) {
        res.send(docs[0])

      })
    })

  })
});
router.get('/querycontent', function (req, res, next) {
  var content = new RegExp(req.query.content)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('notebook', function (err, coll) {
      coll.find({
        'content': content
      }).toArray(function (err, docs) {
        res.send(docs)

      })
    })

  })
});
router.get('/queryall', function (req, res, next) {
  var id = req.query.id
  var id_ = new mongodb.ObjectID(id)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('notebook', function (err, coll) {
      coll.find({
      }).toArray(function (err, docs) {
        res.send(docs)

      })
    })

  })
});


router.get('/modify', function (req, res, next) {
  var id = req.query.id
  var id_ = new mongodb.ObjectID(id)
  var title = req.query.title
  var content = req.query.content

  console.log(content)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
    conn.collection('notebook', function (err, coll) {
      coll.findOneAndUpdate({
        '_id': id_
      }, {
        $set: {
          title: title,
          content: content
        }
      }, {
        returnOriginal: false,
        upsert: true
      },  function(err, object) {
        if (err){
            console.warn(err.message);  // returns error if no matching object found
        }else{
           res.send(object)
        }
    })
  })
  })
});




module.exports = router;