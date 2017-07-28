const stock = require('../index').stock;

stock.getSinaConceptsClassified().then(({ data }) => {
  console.log(JSON.stringify(data));
});
