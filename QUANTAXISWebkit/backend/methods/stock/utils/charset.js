'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol ? "symbol" : typeof obj; };

/* eslint-disable global-require */
/* eslint-disable import/newline-after-import */
var charset = exports.charset = function charset(enc) {
  return function (res) {
    // if under nodejs environment
    if ((typeof module === 'undefined' ? 'undefined' : _typeof(module)) !== undefined && module.exports) {
      var _ret = function () {
        var iconv = require('iconv-lite');
        return {
          v: res.buffer().then(function (buffer) {
            return iconv.decode(buffer, enc);
          })
        };
      }();

      if ((typeof _ret === 'undefined' ? 'undefined' : _typeof(_ret)) === "object") return _ret.v;
    }
    return res.blob().then(function (blob) {
      var reader = new FileReader();
      reader.readAsText(blob, enc);
      return new Promise(function (resolve) {
        reader.onloadend(function () {
          return resolve(reader.result);
        });
      });
    });
  };
};