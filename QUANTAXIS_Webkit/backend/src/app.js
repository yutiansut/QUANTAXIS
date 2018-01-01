import Koa from 'koa';
import logger from 'koa-logger';
import router from "./routes";
import mongo from './database';

let mongo_opt = {
  host: process.env.MONGO_HOST || 'localhost',
  port: process.env.MONGO_PORT || 27017,
  db: process.env.MONGO_DB || 'quantaxis'
}
if (process.env.MONGO_USER && process.env.MONGO_PASS) {
  opts.user = process.env.MONGO_USER;
  opts.pass = process.env.MONGO_PASS;
}

const app = new Koa();
app.use(logger('dev'));
app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = err.status || 500;
    ctx.body = err.message;
    ctx.app.emit('error', err, ctx);
  }
});
mongo(app.context, mongo_opt) ;

app.use((ctx, next) => {
  if (ctx.db) {
    next()
  } else {
    ctx.body = 'Database is not connected. Please check your DB config.';
  }
});
app.use(router.routes());
app.use(router.allowedMethods());

module.exports = app;

if (!module.parent) {
  app.listen(process.env.PORT || '3000');
};
