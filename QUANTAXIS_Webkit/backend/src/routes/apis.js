export default function (router) {
  router.get('/queryContentbyName', async function (ctx, next) {
    console.log('get data');
    console.log(req.query.name);
    if (req.query.name) {
      var name = new RegExp(req.query.name); //模糊查询参数
      console.log(name);
    }
    const cursor = ctx.db.collection('articles').find({'content': name});
    const docs = await cursor.toArray();
    console.log(docs)
    ctx.body = docs;
  });

  router.get('/queryTitlebyName', async function (ctx, next) {
    console.log('get data');
    console.log(req.query.name);

    if (req.query.name) {
      var name = new RegExp(req.query.name); //模糊查询参数
      console.log(name);
    }
    const cursor = ctx.db.collection('articles').find({'title': name});
    const docs = await cursor.toArray();
    var len = docs.length;
    console.log(len);
    var result = [];
    for (i = 0; i < len; i++) {
        result[i] = (docs[i].title)
    }
    ctx.body = (result);
  });

  router.get('/queryContentbyTitle', async function (ctx, next) {
    console.log('get data');
    console.log(req.query.title);
    if (req.query.title) {
        var title = new RegExp(req.query.title); //模糊查询参数
        console.log(title);
    }
    const cursor = ctx.db.collection('articles').find({'title': title});
    const docs = await cursor.toArray();
    var result = docs[0].content;
    ctx.body = (result);
  });
}
