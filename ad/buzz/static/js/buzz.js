var socket = new io.Socket(WEBSOCKET_ADDR);
socket.connect();

socket.on('connect', function () {
    console.debug('connected');
});

socket.on('message', function (msg) {
    console.debug('message received: ' + msg);
});

socket.on('disconnect', function () {
    console.debug('disconnected');
});
