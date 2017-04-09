var express = require('express');
var router = express.Router();

var mongodb= require('mongodb')

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
  res.render('user/index', {
    title: 'UserS'
  });
});


router.get('/signup', function (req, res, next) {
  if (req.query.name) {
    var name = req.query.name;
    console.log(name)
    if (req.query.password) {
      var password = req.query.password;
      console.log(password)
      User.findOne({
        username: name
      }, function (err, doc) {
        if (err) {

        } else {
          if (doc === null) {
            var user = new User({
              username: name,
              password: password

            });
            user.save(function (err, doc) {
              if (err) {
                console.log('error')
                res.send('failed to register')
              } else {
                console.log('success, new user name' + name + ',password' + password);
                res.send('success');
              }
            })
          } else res.send('already exist')
        }

      })
    }
  }

});
router.get('/login', function (req, res, next) {
  if (req.query.name) {
    var name = req.query.name;
    mongodb.connect('mongodb://localhost:27017/quantaxis', function(err, conn){
         conn.collection('user_list', function(err, coll){ 
              coll.find({'username':name}).toArray(function(err,docs){
                  var password=docs.password
                  console.log(password)
                  if (req.query.password){
                    if (password==req.query.password){
                      res.send('success')
                    }else {
                      res.send('wrong password')
                      console.log('wrong password')
                  }
                }else res.send('no password')
                 
         })
        })
    })
  } else res.send('no user name')
});
module.exports = router;