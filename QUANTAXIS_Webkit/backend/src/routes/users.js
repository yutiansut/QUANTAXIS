export default function (router) {
  //var User = db.model('user_list', UserSchema);
  router.get('/users/signup', async (ctx) => {
    if (!ctx.query.name) {
      ctx.body = 'no user name';
      return;
    }
    var name = ctx.query.name;
    console.log(name);
    if (ctx.query.password) {
      var password = ctx.query.password;
      console.log(password)

      const cursor = ctx.db.collection('user_list').find({'username': name});
      let docs = await cursor.toArray();
      if (docs[0] == undefined) {
        console.log('none username')
        await ctx.db.collection('user_list').insert({
          'username': name,
          'password': password
        });
        ctx.body = 'success';
      }
    }
  });

  router.get('/users/login', async (ctx) => {
    if (ctx.query.name) {
      var name = ctx.query.name;
      const cursor = ctx.db.collection('user_list').find({'username': name});
      let docs = await cursor.toArray();
      if (docs != null && docs.length > 0) {
        let doc = docs[0]
        var password = doc.password
        console.log(ctx.query)
        if (ctx.query.password) {
          if (password == ctx.query.password) {
            ctx.body = 'success'
          } else {
            ctx.body = 'wrong password'
            console.log('wrong password')
          }
        } else {
          ctx.body = 'no password'
        }
      } else ctx.body = 'user not found';
    } else ctx.body = 'no user name';
  });
}
