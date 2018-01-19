const stock = require('../index').stock;


stock.getAllStocks().then(({ data }) => {
  console.log(JSON.stringify(data));
});

