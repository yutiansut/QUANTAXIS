var stock = require('../methods/stock/index').stock;
export default function (router) {
  router.get('/stock/history/all', function (ctx, next) {
    console.log(ctx.query.code);
    console.log(ctx.query.feq);
    var code = ctx.query.code;
    var options = {};
    if (ctx.query.feq) {
      var ktype = ctx.query.feq;
      options = {
        code: code,
        ktype: ktype,
      }
    } else options = {
      code: code
    };

    console.log(options)
    stock.getHistory(options).then(({
      data
    }) => {
      ctx.body = (data.record);
    });
  });

  router.get('/stock/history/time', async function (ctx, next) {

    var code = ctx.query.code;
    var code = code.slice(0, 6)
    var start = ctx.query.start;
    var end = ctx.query.end;
    var start_stamp = new Date(start).getTime();
    var end_stamp = new Date(end).getTime();
    console.log(code)
    const cursor = ctx.db.collection('stock_day').find({
      "code": code,
      "date_stamp": {
        $gte: start_stamp / 1000 - 50,
        $lte: end_stamp / 1000
      }
    });
    let docs = await cursor.toArray();
    //console.log(err)
    //console.log(docs)
    data = []
    for (id in docs) {
      data.push(docs[id])
    }
    ctx.body = (data)
  });

  router.get('/stock/index', function (ctx, next) {

    stock.getIndex().then(({
      data
    }) => {
      ctx.body = (data);
    });
  });

  router.get('/stock/live', function (ctx, next) {
    var code = ctx.query.code;
    var query = {
      codes: code
    };
    stock.getLiveData(query).then(({
      data
    }) => {
      ctx.body = (data);
    });
  });
}