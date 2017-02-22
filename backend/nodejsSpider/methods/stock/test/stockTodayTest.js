const stock = require('../index').stock;

stock.getTodayAll().then(({ data }) => {
  console.log(data);
});


const query = {
  pageSize: 80,
  pageNo: 1,
};
stock.getTodayAll(query).then(({ data }) => {
  console.log(data);
});
