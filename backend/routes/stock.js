var express = require('express');
var router = express.Router();
var stock = require('../methods/stock/index').stock;
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

router.get('/history/time', function(req, res, next) {

  var code=req.query.code;
  var options={
    code:code
  };
  var start=req.query.start;
  var end=req.query.end;
  console.log(options)
  stock.getHistory(options).then(({ data }) => {
    var datas=data.record;
    console.log(end)
    var datas=data.record;
    function getid(date){
    for(i=0;i<datas.length;i++){
      if (datas[i][0]==date){
        console.log('i'+i)
        return i
      }
    }
    }
    var sId=getid(start);
    console.log('sId'+sId);
    var eId=getid(end);
    console.log('eId'+eId);
    if (sId=='undefined'){
      res.send("Wrong Date or No data")
    }
    else if (eId=='undefined'){
      res.send("Wrong Date or No data")
    }
    else{
      var newarray=datas.slice(sId,eId+1)
      res.send(newarray)
    }
    
  });
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
