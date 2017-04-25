var express = require('express');
var router = express.Router();
var stock = require('../methods/stock/index').stock;
var mongodb =require('mongodb')
/* GET users listing. */
router.get('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});
router.get('/', function(req, res, next) {
  res.send('respond with a resource');
});

router.get('/history/all', function(req, res, next) {
  console.log(req.query.code);
  console.log(req.query.feq);
  var code=req.query.code;
  var options={};
  if (req.query.feq){
    var ktype=req.query.feq;
    options={
    code: code,
    ktype: ktype,
  }
  }
  else options={
    code: code
  };

  console.log(options)
  stock.getHistory(options).then(({ data }) => {
    res.send(data.record);
  });
});



router.get('/market',function(req, res, next) {
  
  cookie=req.query.cookie
  console.log(cookie)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
        conn.collection('backtest_history', function (err, coll) {
          coll.find({'cookie':cookie}).toArray(function (err, docs) {
            //console.log(docs.length)
            data=[]
            for (id in docs){
              data.push({'market':docs[id]['market'],'bid':docs[id]['bid']})
            }
            res.send(data)
          
        })
      })

})
});




router.get('/history/time', function(req, res, next) {

  var code=req.query.code;
  var code=code.slice(0,6)
  var start=req.query.start;
  var end=req.query.end;
  var start_stamp=new Date(start).getTime();
  var end_stamp=new Date(end).getTime();
  console.log(code)
  mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
        conn.collection('stock_day', function (err, coll) {
          coll.find({"code":code,"date_stamp":{$gte:start_stamp/1000-50,$lte:end_stamp/1000}}).toArray(function (err, docs) {
            //console.log(err)
            //console.log(docs)
            data=[]
            for (id in docs){
              data.push(docs[id])
            }
            res.send(data)
          
        })
      })

})
});

router.get('/index', function(req, res, next) {

  stock.getIndex().then(({ data }) => {
  res.send(data);
  });
});



router.get('/live', function(req, res, next) {
  var code=req.query.code;
  var query = {
    codes:code
  };
  stock.getLiveData(query).then(({ data }) => {
    res.send(data);
  });
});






module.exports = router;
