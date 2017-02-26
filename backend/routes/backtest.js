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

router.get("/init",function(req,res,next){
  var username=req.query.username;
  var password=req.query.password;
  var account=req.query.account;

  var querys="name="+username+"&password="+password;
  superagent.get("")
  request
    .post('/users/login')
    .send({ name: username, password: password })
    .set('Accept', 'application/json')
    .end(function(err, res){

      if(res.body=="success"){
         console.log("success")
        
      }
      // Calling the end function will send the request
    });

});
router.get("/ts",function(req,res,next){
  var username=req.query.username;
  var password=req.query.password;
  var variety=req.query.variety;
  var bidCode=req.query.bidCode;
  var bidPrice=req.query.bidPrice;
  var bidTime=req.query.bidTime;
  var bidAmount=req.query.bidAmount;
  var bidTowards=req.query.bidTowards;
  var querys="name="+username+"&password="+password;
  superagent.get("")
  request
    .post('/users/login')
    .send({ name: username, password: password })
    .set('Accept', 'application/json')
    .end(function(err, res){

      if(res.body==success){

      }
      // Calling the end function will send the request
    });

});
router.get("/tick",function(req,res,next){
  var username=req.query.username;
  var password=req.query.password;
  var variety=req.query.variety;
  var bidCode=req.query.bidCode;
  var bidPrice=req.query.bidPrice;
  var bidTime=req.query.bidTime;
  var bidAmount=req.query.bidAmount;
  var bidTowards=req.query.bidTowards;

  


});



module.exports = router;
 