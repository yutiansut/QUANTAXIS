// subber.js
var io = require('socket.io').listen(5556);


console.log('Subscriber connected to port 5556');

io.sockets.on('connection', function (socket) {
  socket.emit('PO', { hello: 'world' });
  socket.on('PO', function (data) {
    console.log(data);
  });
});