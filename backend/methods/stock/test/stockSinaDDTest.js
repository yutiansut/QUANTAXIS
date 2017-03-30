const stock = require('../index').stock;


const query = {
  code: '600848',
  volume: 70,
  date: '2016-08-26',
};
stock.getSinaDD(query).then(({ data }) => {
  console.log(data);
});

