export default function (router) {
  /* GET home page. */
  router.get('/backtest', function (ctx, next) {
    ctx.body = 'Backtest';
  });

  //http://localhost:3000/backtest/info?name=yutiansut
  router.get('/backtest/info', function (ctx, next) {
    console.log('backtest')
    if (ctx.query.strategy)
      query = {strategy: ctx.query.strategy};
    if (ctx.query.name)
      query = {name: ctx.query.name};
    console.log(query)
    ctx.db.collection('backtest_info').find(query).toArray(function (err, docs) {
          ctx.body = (docs)
        })
  });

  router.get('/backtest/info_all', function (ctx, next) {
    console.log('backtest')

    ctx.db.collection('backtest_info').find({}).toArray(function (err, docs) {
      ctx.body = (docs)
    })
  });

  router.get('/backtest/info_code', function (ctx, next) {
    console.log('backtest')

    var code = new RegExp(ctx.query.code);
    console.log(code)
    ctx.db.collection('backtest_info').find({
          'stock_list': code
        }).toArray(function (err, docs) {
          ctx.body = (docs)
        });
  });


  router.get('/backtest/info_cookie', function (ctx, next) {
    console.log('backtest')
    cookie = ctx.query.cookie
    console.log(ctx.query.cookie)
    ctx.db.collection('backtest_info').find({
          'account_cookie': cookie
        }).toArray(function (err, docs) {
          ctx.body = (docs[0])
        });
  });


  router.get('/backtest/history', function (ctx, next) {
    cookie = ctx.query.cookie
    console.log(cookie)
    ctx.db.collection('backtest_history').find({
          'cookie': cookie
        }).toArray(function (err, docs) {
          console.log(docs)
          ctx.body = (docs)
        });
  });


  router.get('/backtest/strategy', function (ctx, next) {
    cookie = ctx.query.cookie
    console.log(cookie)
    ctx.db.collection('strategy').find({
          'cookie': cookie
        }).toArray(function (err, docs) {
          console.log(docs)
          ctx.body = (docs)
        })
  });
}
