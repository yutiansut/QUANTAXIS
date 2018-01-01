import { MongoClient } from 'mongodb';

const defaultOptions = {
  host: 'localhost',
  port: 27017,
  db: 'test',
  max: 100,
  min: 1
};

const mongo = (ctx, options) => {
  options = Object.assign({}, defaultOptions, options);
  let mongoUrl = options.uri || options.url;
  if (!mongoUrl) {
    if (options.user && options.pass) {
      mongoUrl = `mongodb://${options.user}:${options.pass}@${options.host}:${options.port}/${options.db}`;
    } else {
      mongoUrl = `mongodb://${options.host}:${options.port}/${options.db}`;
    }
  }

  MongoClient.connect(mongoUrl, (err, db) => {
    if (null === err) {
      console.log("Connected successfully to server")
      ctx.db = db;
    }
  });
};

export default mongo;
