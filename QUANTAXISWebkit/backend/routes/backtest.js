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

router.get('/backtest',function(req, res, next) {
  console.log('backtest')
  console.log('req.query.name')

})


module.exports = router;
 