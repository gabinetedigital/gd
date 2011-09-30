function Buzz(sockAddr, templateId) {
    var socket = new io.Socket(sockAddr);
    socket.connect();

    socket.on('connect', function () {
        console.debug('connected');
    });

    socket.on('message', function (msg) {
        var parsed = JSON.parse(msg);
        var $el = $(tmpl(templateId, parsed));
        $('#buzz').prepend($el);
    });

    socket.on('disconnect', function () {
        console.debug('disconnected');
    });
}

