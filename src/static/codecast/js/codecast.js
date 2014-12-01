$(document).ready(function() {
    WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
    WEB_SOCKET_DEBUG = true;

    // Socket.io specific code
    socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        socket.emit('connect');
    });

    socket.on('disconnect', function() {
        socket.emit('disconnect');
    });

    socket.on('data', function(data) {
        console.log(data);
    });

    socket.on('output-code-stream', function(payload_) {
        var payload = JSON.parse(payload_);
        var deltas = [JSON.parse(payload['data'])];

        var nick = payload.nick;

        ace_readers[nick].getSession().getDocument().applyDeltas(deltas);
        $('#link-tab-' + nick).addClass('bold');
    });
});
