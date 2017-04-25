'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.getSinaDD = exports.getIndex = exports.getTodayTick = exports.getLiveData = exports.getTodayAll = exports.getTick = exports.getHistory = undefined;

var _superagentCharset = require('superagent-charset');

var _superagentCharset2 = _interopRequireDefault(_superagentCharset);

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

var _urls = require('./urls');

var _util = require('./util');

var _charset = require('../utils/charset');

require('../utils/fetch');

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

/**
 * getHistory: 获取个股历史数据
 * 返回数据格式 - 日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
 *
 * @param {Object} options = {} - options
 * @param {String} options.code - 股票代码, 例如： '600848'
 * @param {String} options.start - 开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
 * @param {String} options.end - 结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
 * @param {String} options.ktype - 数据类型，day=日k线 week=周 month=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为day
 * @param cb
 * @return {undefined}
 */
var getHistory = exports.getHistory = function getHistory() {
  var query = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  var defaults = {
    code: null,
    start: null,
    end: null,
    ktype: 'day'
  };
  var options = Object.assign({}, defaults, query);

  var symbol = (0, _util.codeToSymbol)(options.code);
  var url = (0, _urls.priceUrl)(options.ktype, symbol);

  return fetch(url).then(_util.checkStatus).then(function (res) {
    return res.json();
  }).then(function (json) {
    return { data: json };
  }).catch(function (error) {
    return { error: error };
  });
};

/**
 * getTick - 获取历史分笔数据
 * 返回格式：成交时间 成交价  涨跌幅  价格变动  成交量(手)  成交额(元)  性质
 *
 * @param {Object} options
 * @param {string} options.code - 股票代码, 例如： '600848'
 * @param {string} options.date - 日期 格式：YYYY-MM-DD
 * @param cb
 * @return {undefined}
 */
var getTick = exports.getTick = function getTick() {
  var query = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  var defaults = {
    code: null,
    date: null
  };
  var options = Object.assign({}, defaults, query);

  var symbol = (0, _util.codeToSymbol)(options.code);
  var url = (0, _urls.tickUrl)(options.date, symbol);
  var mapData = function mapData(data) {
    var result = [];
    data.split('\n').forEach(function (line, i) {
      if (i !== 0 && line !== '') {
        result.push(line.split('\t'));
      }
    });
    return { data: result };
  };

  return fetch(url).then(_util.checkStatus).then((0, _charset.charset)('GBK')).then(mapData).catch(function (error) {
    return { error: error };
  });
};

/**
 * getTodayAll - 一次性获取最近一个日交易日所有股票的交易数据
 * 返回数据格式：代码，名称，涨跌幅，现价，开盘价，最高价，最低价，最日收盘价，成交量，换手率
 *
 * @param options - (可选) 若为空，则返回A股市场今日所有数据
 * @param {Number} options.pageSize - 分页的大小，如：80， 默认10000，即返回所有数据
 * @param {Number} options.pageNo - 分页页码，默认1
 * @param cb
 * @return {undefined}
 */
/* eslint-disable no-eval */
var getTodayAll = exports.getTodayAll = function getTodayAll() {
  var query = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  var defaults = {
    pageSize: 10000,
    pageNo: 1
  };
  var options = Object.assign({}, defaults, query);
  var url = (0, _urls.todayAllUrl)(options.pageSize, options.pageNo);

  return fetch(url).then(_util.checkStatus).then(function (res) {
    return res.text();
  }).then(function (data) {
    return { data: eval(data) };
  }).catch(function (error) {
    return { error: error };
  });
};

/**
 * getLiveData - 获取实时交易数据
 * 返回数据：{Array}
 * 0：股票代码
 * 1：股票名字
 * 2：今日开盘价
 * 3：昨日收盘价
 * 4：当前价格
 * 5：今日最高价
 * 6：今日最低价
 * 7：竞买价，即“买一”报价
 * 8：竞卖价，即“卖一”报价
 * 9：成交量 maybe you need do volume/100
 * 10：成交金额（元 CNY）
 * 11：委买一（笔数 bid volume）
 * 12：委买一（价格 bid price）
 * 13：“买二”
 * 14：“买二”
 * 15：“买三”
 * 16：“买三”
 * 17：“买四”
 * 18：“买四”
 * 19：“买五”
 * 20：“买五”
 * 21：委卖一（笔数 ask volume）
 * 22：委卖一（价格 ask price）
 * ...
 * 31：日期；
 * 32：时间；
 *
 * @param {Object} options
 * @param {Array} options.codes - 股票代码数组，例如['600848', '600000', '600343']
 * @param cb
 * @return {undefined}
 */
var getLiveData = exports.getLiveData = function getLiveData() {
  var query = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  var defaults = { codes: ['600000'] };
  var options = Object.assign({}, defaults, query);
  var codes = options.codes.map(function (code) {
    return (0, _util.codeToSymbol)(code);
  });
  var url = (0, _urls.liveDataUrl)(codes);
  var mapData = function mapData(data) {
    var result = data.split('\n').filter(function (item) {
      return item !== '';
    }).map(function (item) {
      var matches = item.match(/(sz|sh)(\d{6}).*"(.*)"/i);
      var symbol = matches[1] + matches[2];
      var records = matches[3].split(',');
      return [symbol].concat(_toConsumableArray(records));
    });

    return { data: result };
  };

  return fetch(url).then(_util.checkStatus).then((0, _charset.charset)('GBK')).then(mapData).catch(function (error) {
    return { error: error };
  });
};

/**
 * getTodayTick - 获取当日分笔明细数据，用于在交易进行的时候获取
 * 返回数据：
 * {
 *  begin: 开始时间,
 *  end: 结束时间,
 *  zhubi_list: [
 *    {
 *      TRADE_TYPE: 交易类型, 1: 买盘，0：中性盘，-1：卖盘
 *      PRICE_PRE: 上一档价格
 *      PRICE: 当前价格
 *      VOLUME_INC: 成交量(股)
 *      TURNOVER_INC: 成交额
 *      TRADE_TYPE_STR: 交易类型：买盘、卖盘、中性盘
 *      DATE_STR: 时间
 *    }
 *  ]
 * }
 *
 * @param {Object} options
 * @param {String} options.code - 六位股票代码
 * @param {String} options.end - 结束时间。例如：15:00:00, 那么就会获取14:55:00 - 15:00:00之间的分笔数据，也就是end指定时间之前的五分钟
 * @param cb
 * @return {undefined}
 */
var getTodayTick = exports.getTodayTick = function getTodayTick() {
  var query = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  var defaults = {
    code: '600000',
    end: '15:00:00'
  };
  var options = Object.assign({}, defaults, query);
  var url = (0, _urls.todayTickUrl)(options.code, options.end);

  return fetch(url).then(_util.checkStatus).then(function (res) {
    return res.json();
  }).then(function (json) {
    return { data: json };
  }).catch(function (error) {
    return { error: error };
  });
};

var getIndex = exports.getIndex = function getIndex() {
  var url = (0, _urls.indexUrl)();
  var mapData = function mapData(data) {
    var result = data.split('\n').filter(function (item) {
      return item !== '';
    }).map(function (item) {
      var matches = item.match(/(sz|sh)(\d{6}).*"(.*)"/i);
      var symbol = matches[1] + matches[2];
      var records = matches[3].split(',');
      return {
        code: symbol,
        name: records[0],
        open: records[1],
        preclose: records[2],
        close: records[3],
        high: records[4],
        low: records[5],
        volume: records[8],
        amount: records[9]
      };
    });
    return { data: result };
  };

  return fetch(url).then(_util.checkStatus).then((0, _charset.charset)('GBK')).then(mapData).catch(function (error) {
    return { error: error };
  });
};

/**
 * getSinaDD - 获取新浪大单数据
 * 返回数组：
 * [
 *  {
 *    symbol: 股票代码
 *    name: 股票名字
 *    time: 时间
 *    price: 成交价格
 *    volume: 成交量（手）
 *    preprice: 前一价格
 *    type: 类型，买盘、卖盘、中性盘
 *  }
 * ]
 *
 * @param {Object} options
 * @param {String} options.code - 六位股票代码
 * @param {String} options.volume - 设置多少手以上算大单，例如: 400，则返回400手以上交易量的大单
 * @param {String} options.date - 日期，格式YYYY-MM-DD， 默认当日日期
 * @param cb
 * @return {undefined}
 */
var getSinaDD = exports.getSinaDD = function getSinaDD() {
  var query = arguments.length <= 0 || arguments[0] === undefined ? {} : arguments[0];

  var defaults = {
    code: '600000',
    volume: 400,
    date: _util.DATE_NOW
  };
  var options = Object.assign({}, defaults, query);
  var url = (0, _urls.sinaDDUrl)((0, _util.codeToSymbol)(options.code), options.volume * 100, options.date);
  var mapData = function mapData(data) {
    var result = data.split('\n').filter(function (item, idx) {
      return item !== '' && idx !== 0;
    }).map(function (item) {
      var ddArr = item.split(',');
      return {
        symbol: ddArr[0],
        name: ddArr[1],
        time: ddArr[2],
        price: ddArr[3],
        volume: ddArr[4] / 100,
        preprice: ddArr[5],
        type: ddArr[6]
      };
    });
    return { data: result };
  };

  return fetch(url).then(_util.checkStatus).then((0, _charset.charset)('GBK')).then(mapData).catch(function (error) {
    return { error: error };
  });
};