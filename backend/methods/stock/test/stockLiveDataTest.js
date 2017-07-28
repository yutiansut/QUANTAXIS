const stock = require('../index').stock;

const query = {
  codes:'600848'
};
stock.getLiveData(query).then(({ data }) => {
  console.log(data);
});

