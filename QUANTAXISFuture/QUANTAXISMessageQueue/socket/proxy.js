var proxy = require('http-proxy').createProxyServer({
  target: {host: 'localhost', port: 9000}
}).on('error', function(err, req, res) {
  console.log('[ERROR] %s', err);
  res.end();
});
var server = require('http').createServer(function(req, res) {
  console.log('[REQUEST.%s] %s', req.method, req.url);
  console.log(req['headers']);
  if (req.method == 'POST') {
    var body = '';
    req.on('data', function (data) {
      body += data;
    });
    req.on('end', function () {
      print_body('[REQUEST.BODY] ', body);
    });
  }
  var write = res.write;
  res.write = function(data) {
    print_body('[RESPONSE.BODY] ', data);
    write.call(res, data);
  }
  proxy.web(req, res);
});
function print_body(header, body) {
  var text = String(body);
  console.log(header + text);
  if (text.charCodeAt(0) != 0) return;
  for (var i = 0; i < text.length; i++) {
    var character_code = text.charCodeAt(i);
    console.log('body[%s] = %s = %s', i, text[i], character_code);
    if (character_code == 65533) break;
  }
}
server.listen(8000);