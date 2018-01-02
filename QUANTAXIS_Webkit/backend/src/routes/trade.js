export default function (router) {
  /* GET home page. */
  router.get('/trade', function (ctx, next) {
    ctx.body = {
      title: '实盘查询接口'
    };
  })

  router.get('/trade/history', async function (ctx, next) {
    //console.log('backtest')
    const cursor = ctx.db.collection('trade_stock').find();
    let docs = await cursor.toArray();
    res.send(docs)
  });

  router.get('/trade/lastest', async function (ctx, next) {
    //console.log('backtest')
    const cursor = ctx.db.collection('trade_stock').find();
    let docs = await cursor.toArray();
    res.send(docs[docs.length - 1]);
  });
}
