var express = require('express');
var router = express.Router();

var mongodb = require('mongodb')
var assert = require('assert')
/**

*/

//var User = db.model('user_list', UserSchema);
router.get('*', function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
  res.header("X-Powered-By", ' 3.2.1')
  res.header("Content-Type", "application/json;charset=utf-8");
  next();
});
router.get('/', function (req, res, next) {
  res.send('xxx')
});


router.get('/signup', function (req, res, next) {
  if (req.query.name) {
    var name = req.query.name;
    console.log(name)
    if (req.query.password) {
      var password = req.query.password;
      console.log(password)
      
      mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
        conn.collection('user_list', function (err, coll) {
          coll.find({ 'username': name }).toArray(function (err, docs) {
            if (docs[0]==undefined) {
              console.log('none username')
              coll.insert({ 'username': name, 'password': password }, function (err, docs) {
                console.log(docs)
                res.send('success')

              })
            }
          })
        })
      })
    }
  }

});
router.get('/login', function (req, res, next) {
  if (req.query.name) {
    var name = req.query.name;
    mongodb.connect('mongodb://localhost:27017/quantaxis', function (err, conn) {
      conn.collection('user_list', function (err, coll) {
        coll.find({ 'username': name }).toArray(function (err, docs) {
          console.log(docs[0])
          if (docs[0]!=undefined){
              var password = docs[0].password
              console.log(req.query.password)
              console.log(password)
              if (req.query.password) {
                if (password == req.query.password) {
                  res.send('success')
                } else {
                  res.send('wrong password')
                  console.log('wrong password')
                }
              } else res.send('no password')


          }


        })
      })
    })
  } else res.send('no user name')
});
module.exports = router;