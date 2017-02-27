var express = require('express');
var router = express.Router();
var fs = require('fs');
var superagent = require('superagent');
var cheerio = require('cheerio');
var axios = require('axios');
var http = require('http'); 
var events = require('events');
var mongoose =require('mongoose')
var request = require('superagent');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Backtest' });
});

router.get("/ts",function(req,res,next){
  var variety=req.query.variety;
  var bidCode=req.query.bidCode;
  var bidPrice=req.query.bidPrice;
  var bidTime=req.query.bidTime;
  var db= mongoose.createConnection('localhost','stock');
  db.on('error',console.error.bind(console,'连接错误:'));
  var tsModel=new mongoose.Schema({
    code:String,
    date:String,
    high:Number,
    low:Number
  });
  var tsx=db.model('ts', tsModel);
      tsx.findOne({'code':bidCode,'date':bidTime},function(err,datas){
        if (err==null){
          console.log(datas.high)
          console.log(datas.low)
          if(datas.low<=bidPrice & bidPrice<=datas.high){
            console.log("success")
            res.send("success")
          }
          else{
            console.log("failed")
            res.send("failed")
          }
        }
        else{
          console.log(err)
        }
        
      //如果err==null，则person就能取到数据
    });

});
router.get("/tick",function(req,res,next){
  var variety=req.query.variety;
  var bidCode=req.query.bidCode;
  var bidPrice=req.query.bidPrice;
  var bidTime=req.query.bidTime;
  var bidAmount=req.query.bidAmount;
  var bidTowards=req.query.bidTowards;

  


});



module.exports = router;
 