const stock = require('../index').stock;


const options = {
  period: 'month',
  pageNo: 1,
  pageSize: 100,
};
stock.longPeriodRank(options).then(({ data }) => {
  console.log(data);
});



const options2 = {
  period: 'quarter',
  pageNo: 1,
  pageSize: 100,
};
stock.longPeriodRank(options2).then(({ data }) => {
  console.log(data);
});
