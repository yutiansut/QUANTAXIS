// subber.js
var zmq = require('zmq')
  , sock = zmq.socket('sub');

sock.connect('tcp://127.0.0.1:5556');
sock.subscribe('PO');
console.log('Subscriber connected to port 5556');

sock.on('message', function(topic, message) {
  console.log('received a message related to:', topic, 'containing message:', message);
});