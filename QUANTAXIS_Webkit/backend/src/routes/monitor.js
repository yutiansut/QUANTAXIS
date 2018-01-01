var stock = require('../methods/stock/index').stock;

export default function (router) {
    router.get('/monitor/code', function (req, res, next) {
        const query = {
            code: req.query.name
        };
        console.log(query)
        stock.getHistory(query).then(({
            data
        }) => {
            res.send(data);
        });
    })
}