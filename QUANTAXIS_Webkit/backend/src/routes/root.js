export default function (router) {
  router.all('*', async (ctx, next) => {
    ctx.set("Access-Control-Allow-Origin", "*");
    ctx.set("Access-Control-Allow-sets", "X-Requested-With");
    ctx.set("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    ctx.set("X-Powered-By", ' 3.2.1')
    ctx.set("Content-Type", "application/json;charset=utf-8");
    await next();
  });

  /* GET home page. */
  router.get('/', function (ctx, next) {
    ctx.body = {
      title: 'QUANTAXIS EVENT SERVER'
    };
  })

  router.get('/status', function (ctx, next) {
    ctx.status = 200;
  })
}
