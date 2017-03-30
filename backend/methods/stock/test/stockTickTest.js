const stock = require('../index').stock;

const query = {
  code: '600010',
  date: '2017-2-13',
};
stock.getTick(query).then(({ data }) => {
  console.log(data);
});

