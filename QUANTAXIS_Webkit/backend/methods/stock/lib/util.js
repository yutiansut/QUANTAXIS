'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.checkStatus = undefined;
exports.codeToSymbol = codeToSymbol;
exports.csvToObject = csvToObject;
exports.arrayObjectMapping = arrayObjectMapping;

var _cons = require('./cons');

function codeToSymbol(code) {
  var symbol = '';
  if (_cons.INDEX_LABELS.indexOf(code) >= 0) {
    symbol = _cons.INDEX_LIST[code];
  } else if (code.length === 6) {
    symbol = ['5', '6', '9'].indexOf(code.charAt(0)) >= 0 ? 'sh' + code : 'sz' + code;
  } else {
    symbol = code;
  }

  return symbol;
}

function csvToObject(csv) {
  var csvArr = csv.trim().split('\r\n');
  var headers = csvArr.splice(0, 1);

  headers = headers[0].split(',');
  csvArr = csvArr.map(function (ele) {
    var obj = {};
    ele.split(',').forEach(function (s, i) {
      obj[headers[i]] = s;
    });
    return obj;
  });

  return csvArr;
}

function arrayObjectMapping(fields, items) {
  items = items.map(function (ele) {
    var obj = {};
    ele.forEach(function (s, i) {
      var field = fields[i];
      if (field === 'volume') {
        obj[field] = s / 100;
      } else if (field === 'amount') {
        obj[field] = s / 10000;
      } else {
        obj[field] = s;
      }
    });
    return obj;
  });

  return items;
}

var checkStatus = exports.checkStatus = function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }

  var error = new Error(response.statusText);
  error.response = response;
  throw error;
};