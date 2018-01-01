export default function (router) {
	/* GET home page. */
	router.get('/assests', function (req, res, next) {
	  res.render('index', {
	    title: 'Backtest'
	  });
	});
}
