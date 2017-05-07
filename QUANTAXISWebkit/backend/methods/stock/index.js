'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.stock = undefined;

var _stock = require('./lib');

var stock = _interopRequireWildcard(_stock);

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) newObj[key] = obj[key]; } } newObj.default = obj; return newObj; } }

exports.stock = stock;