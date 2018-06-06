'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.sz50Url = exports.hs300Url = exports.allStockUrl = exports.sinaConceptsIndexUrl = exports.sinaClassifyDetailUrl = exports.sinaIndustryIndexUrl = exports.sinaDDUrl = exports.indexUrl = exports.todayTickUrl = exports.liveDataUrl = exports.todayAllUrl = exports.tickUrl = exports.priceUrl = undefined;
exports.lhbUrl = lhbUrl;
exports.blockTradeUrl = blockTradeUrl;
exports.longPeriodRankUrl = longPeriodRankUrl;

var _cons = require('./cons');

var priceUrl = exports.priceUrl = function priceUrl(ktype, symbol) {
  var _ktype = _cons.K_TYPE[ktype] ? _cons.K_TYPE[ktype] : _cons.K_TYPE.minute;
  var type = _ktype === _cons.K_TYPE.minute ? ktype : 'last';
  var codeStr = _ktype === _cons.K_TYPE.minute ? 'scode' : 'code';
  return 'http://api.finance.ifeng.com/' + _ktype + '/?' + codeStr + '=' + symbol + '&type=' + type;
};

var tickUrl = exports.tickUrl = function tickUrl(date, symbol) {
  return 'http://market.finance.sina.com.cn/downxls.php?date=' + date + '&symbol=' + symbol;
};

var todayAllUrl = exports.todayAllUrl = function todayAllUrl(pageSize, pageNo) {
  return 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?num=' + pageSize + '&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page&page=' + pageNo;
};

var liveDataUrl = exports.liveDataUrl = function liveDataUrl(symbols) {
  return 'http://hq.sinajs.cn/list=' + symbols.join(',');
};

var todayTickUrl = exports.todayTickUrl = function todayTickUrl(code) {
  var end = arguments.length <= 1 || arguments[1] === undefined ? '15:00:00' : arguments[1];
  return 'http://quotes.money.163.com/service/zhubi_ajax.html?symbol=' + code + '&end=' + end;
};

var indexUrl = exports.indexUrl = function indexUrl() {
  return 'http://hq.sinajs.cn/rn=xppzh&list=sh000001,sh000002,sh000003,sh000008,sh000009,sh000010,sh000011,sh000012,sh000016,sh000017,sh000300,sz399001,sz399002,sz399003,sz399004,sz399005,sz399006,sz399100,sz399101,sz399106,sz399107,sz399108,sz399333,sz399606';
};

var sinaDDUrl = exports.sinaDDUrl = function sinaDDUrl(symbol, volume, date) {
  return 'http://vip.stock.finance.sina.com.cn/quotes_service/view/cn_bill_download.php?symbol=' + symbol + '&num=60&page=1&sort=ticktime&asc=0&volume=' + volume + '&amount=0&type=0&day=' + date;
};

var sinaIndustryIndexUrl = exports.sinaIndustryIndexUrl = function sinaIndustryIndexUrl() {
  return 'http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php';
};

var sinaClassifyDetailUrl = exports.sinaClassifyDetailUrl = function sinaClassifyDetailUrl(tag) {
  return 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=400&sort=symbol&asc=1&node=' + tag + '&symbol=&_s_r_a=page';
};

var sinaConceptsIndexUrl = exports.sinaConceptsIndexUrl = function sinaConceptsIndexUrl() {
  return 'http://money.finance.sina.com.cn/q/view/newFLJK.php?param=class';
};

var allStockUrl = exports.allStockUrl = function allStockUrl() {
  return 'http://218.244.146.57/static/all.csv';
};

var hs300Url = exports.hs300Url = function hs300Url() {
  var pageNo = arguments.length <= 0 || arguments[0] === undefined ? 1 : arguments[0];
  var pageSize = arguments.length <= 1 || arguments[1] === undefined ? 300 : arguments[1];
  return 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[["jjhq",' + pageNo + ',' + pageSize + ',"",0,"hs300"]]';
};

var sz50Url = exports.sz50Url = function sz50Url() {
  var pageNo = arguments.length <= 0 || arguments[0] === undefined ? 1 : arguments[0];
  var pageSize = arguments.length <= 1 || arguments[1] === undefined ? 50 : arguments[1];
  return 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[["jjhq",' + pageNo + ',' + pageSize + ',"",0,"zhishu_000016"]]';
};

function lhbUrl(start, end) {
  var pageNo = arguments.length <= 2 || arguments[2] === undefined ? 1 : arguments[2];
  var pageSize = arguments.length <= 3 || arguments[3] === undefined ? 150 : arguments[3];

  var url = 'http://quotes.money.163.com/hs/marketdata/service/lhb.php?page=' + (pageNo - 1) + '&query=start:' + start + ';end:' + end + '&sort=TDATE&order=desc&count=' + pageSize;
  return url;
}

function blockTradeUrl(start, end) {
  var pageNo = arguments.length <= 2 || arguments[2] === undefined ? 1 : arguments[2];
  var pageSize = arguments.length <= 3 || arguments[3] === undefined ? 150 : arguments[3];

  var url = 'http://quotes.money.163.com/hs/marketdata/service/dzjy.php?page=' + (pageNo - 1) + '&query=start:' + start + ';end:' + end + ';&order=desc&count=' + pageSize + '&sort=PUBLISHDATE';
  return url;
}

function longPeriodRankUrl() {
  var period = arguments.length <= 0 || arguments[0] === undefined ? 'month' : arguments[0];
  var pageNo = arguments.length <= 1 || arguments[1] === undefined ? 1 : arguments[1];
  var pageSize = arguments.length <= 2 || arguments[2] === undefined ? 100 : arguments[2];

  var rankBy = '';
  switch (period) {
    case 'week':
      rankBy = 'WEEK_PERCENT';
      break;
    case 'month':
      rankBy = 'MONTH_PERCENT';
      break;
    case 'quarter':
      rankBy = 'QUARTER_PERCENT';
      break;
    case 'year':
      rankBy = 'YEAR_PERCENT';
      break;
    default:
      rankBy = 'PERCENT';
  }
  var url = 'http://quotes.money.163.com/hs/realtimedata/service/rank.php?page=' + (pageNo - 1) + '&query=LONG_PERIOD_RANK:_exists_&fields=RN,CODE,SYMBOL,NAME,PRICE,LONG_PERIOD_RANK,PERCENT&sort=LONG_PERIOD_RANK.' + rankBy + '&order=desc&count=' + pageSize;
  return url;
}