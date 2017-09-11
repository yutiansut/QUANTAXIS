var express = require('express');
var router = express.Router();
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
    title: 'QUANTAXIS EVENT SERVER'
  });
})

router.get('/status', function (req, res, next) {
  res.send(200)
})


module.exports = router;