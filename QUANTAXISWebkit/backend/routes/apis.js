var express = require('express');
var router = express.Router();
var mongodb=require('mongodb');

/* GET home page. */
router.get('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});


router.get('/queryContentbyName', function(req, res, next) {
    console.log('get data');
    console.log(req.query.name);
     if(req.query.name) {
    var name=new RegExp(req.query.name);//模糊查询参数
        console.log(name);
    }
    mongodb.connect('mongodb://localhost:27017/wsc', function(err, conn){
         conn.collection('articles', function(err, coll){ 
              coll.find({'content':name}).toArray(function(err,docs){
                  console.log(docs)
                  res.json(docs)
         })
        })
    })
}); 
router.get('/queryTitlebyName', function(req, res, next) {
    console.log('get data');
    console.log(req.query.name);

     if(req.query.name) {
    var name=new RegExp(req.query.name);//模糊查询参数
        console.log(name);
    }
    mongodb.connect('mongodb://localhost:27017/wsc', function(err, conn){
         conn.collection('articles', function(err, coll){ 
              coll.find({'title':name}).toArray(function(err,docs){
                  var len=docs.length
                  console.log(len)
                  var result=[];
                  for(i=0;i<len;i++){
                      result[i]=(docs[i].title)
                  }
                  res.send(result)
         })
        })
    })
});
router.get('/queryContentbyTitle',function(req,res,next){
        console.log('get data');
    console.log(req.query.title);
     if(req.query.title) {
    var title=new RegExp(req.query.title);//模糊查询参数
        console.log(title);
    }
    mongodb.connect('mongodb://localhost:27017/wsc', function(err, conn){
         conn.collection('articles', function(err, coll){ 
              coll.find({'title':title}).toArray(function(err,docs){
                  var result=docs[0].content;
                  res.send(result)
         })
        })
    })
})



module.exports = router;
