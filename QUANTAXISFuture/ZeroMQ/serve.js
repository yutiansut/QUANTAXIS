// DEBUG=* node serve.js
if (process.argv[2] == 'secure') {
  var fs = require('fs');
  var path = require('path');
  var app = require('https').createServer({
    key: fs.readFileSync(path.resolve(__dirname, 'ssl.key')),
    cert: fs.readFileSync(path.resolve(__dirname, 'ssl.crt'))
  }, serve);
} else {
  var app = require('http').createServer(serve);
}
app.listen(8000);

var io = require('socket.io')(app);
var PAYLOAD = {'xxx': 'yyy'};
var UNICODE_PAYLOAD = {'인삼': '★ 뿌리 ★'};

// Travis currently does not support Buffer.from
function getBuffer(array) {
  var buffer = new Buffer(array.length);
  for (var i = 0; i < array.length; i++) {
    buffer[i] = array[i];
  }
  return buffer;
}
var BINARY_DATA = getBuffer([255, 255, 255]);
var BINARY_PAYLOAD = {
    'data': BINARY_DATA,
    'array': [getBuffer([238]), getBuffer([221])]
}

io.on('connection', function(socket) {
  socket.on('message', function(data, fn) {
    if (fn) {
      // Client requests callback
      if (data) {
        fn(data);
      } else {
        fn();
      }
    } else if (typeof data === 'object') {
      // Data has type object or is null
      socket.json.send(data ? data : 'message_response');
    } else {
      // Data has type string or is ''
      socket.send(data ? data : 'message_response');
    }
  });
  socket.on('emit', function() {
    socket.emit('emit_response');
  });
  socket.on('emit_with_payload', function(payload) {
    socket.emit('emit_with_payload_response', payload);
  });
  socket.on('emit_with_multiple_payloads', function(payload1, payload2) {
    socket.emit('emit_with_multiple_payloads_response', payload1, payload2);
  });
  socket.on('emit_with_callback', function(fn) {
    fn();
  });
  socket.on('emit_with_callback_with_payload', function(fn) {
    fn(PAYLOAD);
  });
  socket.on('emit_with_callback_with_multiple_payloads', function(fn) {
    fn(PAYLOAD, PAYLOAD);
  });
  socket.on('emit_with_callback_with_unicode_payload', function(fn) {
    fn(UNICODE_PAYLOAD);
  });
  socket.on('emit_with_callback_with_binary_payload', function(fn) {
    fn(BINARY_PAYLOAD);
  });
  socket.on('emit_with_event', function(payload) {
    socket.emit('emit_with_event_response', payload);
  });
  socket.on('trigger_server_expects_callback', function(payload) {
    socket.emit('server_expects_callback', payload, function(payload) {
      socket.emit('server_received_callback', payload);
    });
  });
  socket.on('aaa', function() {
    socket.emit('aaa_response', PAYLOAD);
  });
  socket.on('bbb', function(payload, fn) {
    if (fn) fn(payload);
  });
});

io.of('/chat').on('connection', function(socket) {
  socket.on('emit_with_payload', function(payload) {
    socket.emit('emit_with_payload_response', payload);
  });
  socket.on('aaa', function() {
    socket.emit('aaa_response', 'in chat');
  });
  socket.on('trigger_server_expects_callback', function(payload) {
    socket.emit('server_expects_callback', payload, function(payload) {
      socket.emit('server_received_callback', payload);
    });
  });
});

io.of('/news').on('connection', function(socket) {
  socket.on('emit_with_payload', function(payload) {
    socket.emit('emit_with_payload_response', payload);
  });
  socket.on('aaa', function() {
    socket.emit('aaa_response', 'in news');
  });
});

function serve(req, res) {
  fs.readFile(__dirname + '/index.html', function(err, data) {
    res.writeHead(200);
    res.end(data);
  });
}