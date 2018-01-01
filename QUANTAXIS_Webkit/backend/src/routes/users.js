export default function (router) {
  //var User = db.model('user_list', UserSchema);
  router.get('/users/signup', async (ctx, next) => {
    if (ctx.query.name) {
      var name = ctx.query.name;
      console.log(name);
      if (ctx.query.password) {
        var password = ctx.query.password;
        console.log(password)

        ctx.db.collection('user_list')
          .find({'username': name})
          .toArray(function (err, docs) {
            if (docs[0] == undefined) {
              console.log('none username')
              ctx.db.collection('user_list').insert({
                'username': name,
                'password': password
              }, function (err, docs) {
                console.log(docs)
                ctx.body = 'success';
              })
            }
          });
      }
    }
  });

  router.get('/users/login', async (ctx, next) => {
    if (ctx.query.name) {
      var name = ctx.query.name;
      ctx.db.collection('user_list').find({'username': name})
        .toArray(function (err, docs) {
          console.log(docs[0])
          if (docs[0] != undefined) {
            var password = docs[0].password
            console.log(ctx.query.password)
            console.log(password)
            if (ctx.query.password) {
              if (password == ctx.query.password) {
                ctx.body = 'success'
              } else {
                ctx.body = 'wrong password'
                console.log('wrong password')
              }
            } else ctx.body = 'no password'
          }
        });
    } else ctx.body = 'no user name';
  });
}
