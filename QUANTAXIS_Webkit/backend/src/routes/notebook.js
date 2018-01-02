import { ObjectID } from 'mongodb';

export default function (router) {
  //http://localhost:3000/notebook/new
  router.get('/notebook/new', async function (ctx, next) {
    console.log('backtest')
    var title = ctx.query.title
    console.log(ctx.query.title)
    const result = await ctx.db.collection('notebook').insert({'title': title});
    ctx.body = (result['ops'][0]);
  });

  router.get('/notebook/query', async function (ctx, next) {
    var id = ctx.query.id
    var id_ = new ObjectID(id)
    const cursor = ctx.db.collection('notebook').find({'_id': id_});
    let docs = await cursor.toArray();
    ctx.body = (docs[0]);
  });

  router.get('/notebook/querycontent', async function (ctx, next) {
    var content = new RegExp(ctx.query.content)
    const cursor = ctx.db.collection('notebook').find({'content': content});
    let docs = await cursor.toArray();
    ctx.body = (docs);
  });

  router.get('/notebook/queryall', async function (ctx, next) {
    var id = ctx.query.id
    var id_ = new ObjectID(id)
    const cursor = ctx.db.collection('notebook').find({});
    let docs = await cursor.toArray();
    ctx.body = (docs);
  });


  router.get('/notebook/modify', async function (ctx, next) {
    var id = ctx.query.id
    var id_ = new ObjectID(id)
    var title = ctx.query.title
    var content = ctx.query.content

    console.log(content)
    const {lastErrorObject, value, ok} = await ctx.db.collection('notebook').findOneAndUpdate(
      {'_id': id_},
      {
        $set: {
          title: title,
          content: content
        }
      },
      {returnOriginal: false, upsert: true}
    );
    if (ok !== 1){
      // returns error if no matching object found
      console.warn(lastErrorObject);
    } else {
      ctx.body = value;
    }
  });
}