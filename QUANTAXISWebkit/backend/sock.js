util = require('util');
util.debuglog = require('debuglog');
var http = require('http');
var request = require('superagent');
var Agent = require('agentkeepalive');

var keepaliveAgent = new Agent({
  maxSockets: 100,
  maxFreeSockets: 10,
  timeout: 60000,
  keepAliveTimeout: 30000 // free socket keepalive for 30 seconds
});


request
  .get('localhost:5050')
  .agent(keepaliveAgent)
  .send('my event')
  .end(function (err, res) {
    console.log(res);
  });