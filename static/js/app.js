$(document).ready(function(){
    //connect to the socket server.

    var socketio = io.connect('http://' + document.domain + ':' + location.port);
    
    /*
    var socketio = io.connect('http://' + document.domain + ':' + location.port + '/web', {
        'transports': ['polling']
    });
    */
    /*
    var socketio = io.connect('http://' + document.domain + ':' + location.port, {
        'transports': ['polling']
    });
    */
    
    socketio.on('connect', function() {
        socketio.emit('web_pull', {web_message: 'hey'});
        console.log("I'm connected");
    });

    socketio.on('connect_callback', function(msg) {
        server_message = msg.message
        console.log(server_message);
    });

    socketio.on('low_water', function(msg) {
        //low_water_value = msg.low_water
        //console.log(msg);
    });

    socketio.on('water_full', function(msg) {
        //water_full_value = msg.water_full
        //console.log(msg);
    });

    socketio.on('tree_update', function(msg) {
        //low_water_value = msg.low_water
        //water_full_value = msg.water_full
        console.log(msg)
    });

});