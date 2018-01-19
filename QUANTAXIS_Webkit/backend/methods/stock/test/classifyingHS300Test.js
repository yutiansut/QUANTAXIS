const stock = require('../index').stock;

stock.getHS300().then(({ data }) => {
  console.log(data);
});

