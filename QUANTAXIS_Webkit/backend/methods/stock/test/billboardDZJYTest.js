const stock = require('../index').stock;





const options = {
  start: '2016-01-15',
  end: '2016-01-15',
};
stock.blockTrade(options).then(({ data }) => {
  console.log(data);
});

