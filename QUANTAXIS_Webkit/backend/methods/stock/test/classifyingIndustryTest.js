const stock = require('../index').stock;

stock.getSinaIndustryClassified().then(({ data }) => {
  console.log(data);
});

