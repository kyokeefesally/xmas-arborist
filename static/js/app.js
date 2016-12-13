$(document).ready(function(){

    // initialize bootstrap-switch
    $("[name='light-switch']").bootstrapSwitch();
    $('.bootstrap-switch-id-light-switch').hide();

    //connect to the socket server.

    var socketio = io.connect('http://' + document.domain + ':' + location.port + '/web');
    
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
        //socketio.emit('web_pull', {web_message: 'hey'});
        console.log("I'm connected");
    });

    socketio.on('tree_update', function(msg) {
        low_water = msg.low_water
        water_full = msg.water_full
        pump_on = msg.pump_on
        lights_on = msg.lights_on
        console.log(msg)
        $('#light-switch').bootstrapSwitch('state', lights_on); // true || false
        $('.bootstrap-switch-id-light-switch').show();
    });

    socketio.on('low_water', function(msg) {
        low_water_value = msg.low_water
        console.log(msg);
    });

    socketio.on('water_full', function(msg) {
        water_full_value = msg.water_full
        console.log(msg);
    });

    socketio.on('pump_status', function(msg) {
        pump_on_value = msg.pump_on
        console.log(msg);
    });

    socketio.on('light_status', function(msg) {
        console.log(msg);
        lights_on = msg.lights_on
        $('#light-switch').bootstrapSwitch('state', lights_on); // true || false
    });

    $('#light-switch').on('switchChange.bootstrapSwitch', function (event, state) {
        console.log('lights_on: ' + state);
        socketio.emit('light_switch', {lights_on: state});
    });



});