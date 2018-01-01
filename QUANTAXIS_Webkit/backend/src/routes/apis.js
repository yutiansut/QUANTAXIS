export default function (router) {
  router.get('/queryContentbyName', function (ctx, next) {
    console.log('get data');
    console.log(req.query.name);
    if (req.query.name) {
      var name = new RegExp(req.query.name); //模糊查询参数
      console.log(name);
    }
    ctx.db.collection('articles').find({'content': name})
      .toArray(function (err, docs) {
        console.log(docs)
        ctx.body = docs;
      });
  });

  router.get('/queryTitlebyName', function (ctx, next) {
    console.log('get data');
    console.log(req.query.name);

    if (req.query.name) {
      var name = new RegExp(req.query.name); //模糊查询参数
      console.log(name);
    }
    ctx.db.collection('articles').find({'title': name}).toArray((err, docs) => {
      var len = docs.length;
      console.log(len);
      var result = [];
      for (i = 0; i < len; i++) {
          result[i] = (docs[i].title)
      }
      ctx.body = (result);
    });
  });

  router.get('/queryContentbyTitle', function (ctx, next) {
    console.log('get data');
    console.log(req.query.title);
    if (req.query.title) {
        var title = new RegExp(req.query.title); //模糊查询参数
        console.log(title);
    }
    ctx.db.collection('articles').find({'title': title})
      .toArray(function (err, docs) {
        var result = docs[0].content;
        ctx.body = (result);
      });
  });
}
