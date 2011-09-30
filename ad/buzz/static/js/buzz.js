function Buzz(sockAddr, templateId) {
    var socket = new io.Socket(sockAddr);
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
}

new Buzz();
