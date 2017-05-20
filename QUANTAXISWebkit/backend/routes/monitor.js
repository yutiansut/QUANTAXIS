var stock = require('../methods/stock/index').stock;
var express = require('express');
var router = express.Router();




router.get('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
});


router.get('/code',function(req,res,next){
    const query = { code: req.query.name };
    console.log(query)
    stock.getHistory(query).then(({ data }) => {
        res.send(data);
    });
})


module.exports = router;
