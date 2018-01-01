export default function (router) {
  //http://localhost:3000/notebook/new
  router.get('/notebook/new', function (ctx, next) {
    console.log('backtest')
    var title = ctx.query.title
    console.log(ctx.query.title)
    ctx.db.collection('notebook').insert({'title': title}, (err, result) =>{
      ctx.body = (result['ops'][0])
    });
  });

  router.get('/notebook/query', function (ctx, next) {
    var id = ctx.query.id
    var id_ = new mongodb.ObjectID(id)
    ctx.db.collection('notebook').find({'_id': id_}).toArray((err, docs) =>{
      ctx.body = (docs[0])
    });
  });

  router.get('/notebook/querycontent', function (ctx, next) {
    var content = new RegExp(ctx.query.content)
    ctx.db.collection('notebook').find({'content': content})
      .toArray((err, docs) =>{
        ctx.body = (docs)
      });
  });

  router.get('/notebook/queryall', function (ctx, next) {
    var id = ctx.query.id
    var id_ = new mongodb.ObjectID(id)
    ctx.db.collection('notebook').find({}).toArray((err, docs) => {
      ctx.body = (docs);
    });
  });


  router.get('/notebook/modify', function (ctx, next) {
    var id = ctx.query.id
    var id_ = new mongodb.ObjectID(id)
    var title = ctx.query.title
    var content = ctx.query.content

    console.log(content)
    ctx.db.collection('notebook').findOneAndUpdate({
        '_id': id_
      }, {
        $set: {
          title: title,
          content: content
        }
      }, {
        returnOriginal: false,
        upsert: true
      }, function(err, object) {
        if (err){
          // returns error if no matching object found
          console.warn(err.message);
        } else {
          ctx.body = (object);
        }
      });
  });
}