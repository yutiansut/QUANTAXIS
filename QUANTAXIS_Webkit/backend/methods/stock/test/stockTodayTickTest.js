const stock = require('../index').stock;

const query = {
  code: '600848',
  end: '15:00:00',
};
stock.getTodayTick(query).then(({ data }) => {
  console.log(data);
});

