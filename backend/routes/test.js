var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'test' });
});
router.get('/user', function(req, res, next) {
  res.render('./test/user', { title: 'test' });
});

module.exports = router;
