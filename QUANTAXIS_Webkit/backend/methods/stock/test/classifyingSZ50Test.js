const stock = require('../index').stock;

stock.getSZ50().then(({ data }) => {
  console.log(data);
});

