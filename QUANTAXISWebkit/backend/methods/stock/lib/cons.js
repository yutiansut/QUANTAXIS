'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.DATE_NOW = exports.INDEX_LIST = exports.INDEX_LABELS = exports.K_TYPE = undefined;

var _moment = require('moment');

var _moment2 = _interopRequireDefault(_moment);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var K_TYPE = exports.K_TYPE = {
  day: 'akdaily',
  week: 'akweekly',
  month: 'akmonthly',
  minute: 'akmin'
};

var INDEX_LABELS = exports.INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500'];

var INDEX_LIST = exports.INDEX_LIST = {
  sh: 'sh000001',
  sz: 'sz399001',
  hs300: 'sz399300',
  sz50: 'sh000016',
  zxb: 'sz399005',
  cyb: 'sz399006',
  zx300: 'sz399008',
  zh500: 'sh000905'
};

var DATE_NOW = exports.DATE_NOW = (0, _moment2.default)().format('YYYY-MM-DD');