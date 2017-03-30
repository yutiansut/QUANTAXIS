var stock = require('./stock/index').stock;

stock.getTodayAll().then(({ data }) => {
  console.log(data);
});

