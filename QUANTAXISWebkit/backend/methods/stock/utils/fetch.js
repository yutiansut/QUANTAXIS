'use strict';

var _typeof = typeof Symbol === "function" && typeof Symbol.iterator === "symbol" ? function (obj) { return typeof obj; } : function (obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol ? "symbol" : typeof obj; };

/* eslint-disable */
if ((typeof module === 'undefined' ? 'undefined' : _typeof(module)) !== undefined && module.exports) {
  var realFetch = require('no-fetch');
  module.exports = function (url, options) {
    if (/^\/\//.test(url)) {
      url = 'https:' + url;
    }
    return realFetch.call(this, url, options);
  };

  if (!global.fetch) {
    global.fetch = module.exports;
    global.Response = realFetch.Response;
    global.Headers = realFetch.Headers;
    global.Request = realFetch.Request;
  }
} else {
  require('whatwg-fetch');
  module.exports = self.fetch.bind(self);
}