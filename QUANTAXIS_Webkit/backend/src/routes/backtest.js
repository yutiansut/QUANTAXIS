export default function (router) {
  /* GET home page. */
  router.get('/backtest', function (ctx, next) {
    ctx.body = 'Backtest';
  });

  //http://localhost:3000/backtest/info?name=yutiansut
  router.get('/backtest/info', async function (ctx, next) {
    console.log('backtest')
    if (ctx.query.strategy)
      query = {strategy: ctx.query.strategy};
    if (ctx.query.name)
      query = {name: ctx.query.name};
    console.log(query)
    const cursor = ctx.db.collection('backtest_info').find(query);
    const docs = await cursor.toArray();
    ctx.body = (docs);
  });

  router.get('/backtest/info_all', async function (ctx, next) {
    console.log('backtest');
    const cursor = ctx.db.collection('backtest_info').find({});
    const docs = await cursor.toArray();
    ctx.body = (docs);
  });

  router.get('/backtest/info_code', async function (ctx, next) {
    console.log('backtest')

    var code = new RegExp(ctx.query.code);
    console.log(code)
    const cursor = ctx.db.collection('backtest_info').find({
      'stock_list': code});
    const docs = await cursor.toArray();
    ctx.body = (docs);
  });


  router.get('/backtest/info_cookie', async function (ctx, next) {
    console.log('backtest')
    cookie = ctx.query.cookie
    console.log(ctx.query.cookie)
    const cursor = ctx.db.collection('backtest_info').find({
      'account_cookie': cookie});
    const docs = await cursor.toArray();
    ctx.body = (docs[0]);
  });


  router.get('/backtest/history', async function (ctx, next) {
    cookie = ctx.query.cookie
    console.log(cookie)
    const cursor = ctx.db.collection('backtest_info').find({
          'cookie': cookie});
    const docs = await cursor.toArray();
    console.log(docs);
    ctx.body = (docs);
  });


  router.get('/backtest/strategy', async function (ctx, next) {
    cookie = ctx.query.cookie
    console.log(cookie)
    const cursor = ctx.db.collection('backtest_info').find({
          'cookie': cookie});
    const docs = await cursor.toArray();
    console.log(docs);
    ctx.body = (docs);
  });
}
