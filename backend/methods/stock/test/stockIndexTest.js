const stock = require('../index').stock;

stock.getIndex().then(({ data }) => {
  console.log(data);
});
