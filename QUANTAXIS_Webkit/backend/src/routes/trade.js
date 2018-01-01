export default function (router) {
  /* GET home page. */
  router.get('/trade', function (ctx, next) {
    ctx.body = {
      title: '实盘查询接口'
    };
  })

  router.get('/trade/history', function (req, res, next) {
    //console.log('backtest')
    ctx.db.collection('trade_stock').find().toArray(function (err, docs) {
      res.send(docs)
    })
  });

  router.get('/trade/lastest', function (req, res, next) {
    //console.log('backtest')
    ctx.db.collection('trade_stock').find().toArray(function (err, docs) {
      res.send(docs[docs.length - 1]);
    });
  });
}
