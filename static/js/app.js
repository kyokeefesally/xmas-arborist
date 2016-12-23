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
        /*
        var low_water = msg.low_water.toString()
        var water_full = msg.water_full.toString()
        var pump_on = msg.pump_on.toString()
        */
        var low_water = msg.low_water
        var water_full = msg.water_full
        var pump_on = msg.pump_on
        var lights_on = msg.lights_on

        console.log(low_water);
        console.log(water_full);
        console.log(pump_on);

        /*
        $('dd.low_water').html(low_water.toString());
        $('dd.water_full').html(water_full.toString());
        $('dd.pump_on').html(pump_on.toString());
        */
        
        $('#light-switch').bootstrapSwitch('state', lights_on); // true || false
        $('.bootstrap-switch-id-light-switch').show();

        /*
        if (low_water == false && water_full == false && pump_on == false && lights_on == false) {
            console.log('low_water FALSE')
        }
        */

        // off-medium
        if (low_water == false && water_full == false && pump_on == false && lights_on == false) {
            console.log('off-medium');
            $('#tree').attr('src','static/img/off-medium.png');

        // on-medium
        } else if (low_water == false && water_full == false && pump_on == false && lights_on == true) {
            console.log('on-medium');
            $('img#tree').attr('src','static/img/on-medium.png');

        // off-medium-pumping
        } else if (low_water == false && water_full == false && pump_on == true && lights_on == false) {
            console.log('off-medium-pumping');
            $('img#tree').attr('src','static/img/off-medium-pumping.png');

        // on-medium-pumping
        } else if (low_water == false && water_full == false && pump_on == true && lights_on == true) {
            console.log('on-medium-pumping');
            $('img#tree').attr('src','static/img/on-medium-pumping.png');

        // off-low
        } else if (low_water == true && water_full == false && pump_on == false && lights_on == false) {
            console.log('off-low');
            $('img#tree').attr('src','static/img/off-low.png');

        // on-low
        } else if (low_water == true && water_full == false && pump_on == false && lights_on == true) {
            console.log('on-low');
            $('img#tree').attr('src','static/img/on-low.png');

        // off-low-pumping
        } else if (low_water == true && water_full == false && pump_on == true && lights_on == false) {
            console.log('off-low-pumping');
            $('img#tree').attr('src','static/img/off-low-pumping.png');

        // on-low-pumping
        } else if (low_water == true && water_full == false && pump_on == true && lights_on == true) {
            console.log('on-low-pumping');
            $('img#tree').attr('src','static/img/on-low-pumping.png');

        // off-full
        } else if ((low_water == false || low_water == true) && water_full == true && pump_on == false && lights_on == false) {
            console.log('off-full');
            $('img#tree').attr('src','static/img/off-full.png');

        // on-full
        } else if ((low_water == false || low_water == true) && water_full == true && pump_on == false && lights_on == true) {
            console.log('on-full');
            $('img#tree').attr('src','static/img/on-full.png');

        // off-full-pumping
        } else if (low_water == false && water_full == true && pump_on == true && lights_on == false) {
            console.log('off-full-pumping');
            $('img#tree').attr('src','static/img/off-full-pumping.png');

        // on-full-pumping
        } else if (low_water == false && water_full == true && pump_on == true && lights_on == true) {
            console.log('on-full-pumping');
            $('img#tree').attr('src','static/img/on-full-pumping.png');
        }

        console.log(msg)
    });

    socketio.on('low_water', function(msg) {
        //low_water = msg.low_water.toString()
        low_water = msg.low_water
        //$('dd.low_water').html(low_water);
        console.log(msg);
    });

    socketio.on('water_full', function(msg) {
        //water_full = msg.water_full.toString()
        water_full = msg.water_full
        //$('dd.water_full').html(water_full);
        console.log(msg);
    });

    socketio.on('pump_status', function(msg) {
        //pump_on = msg.pump_on.toString()
        pump_on = msg.pump_on
        //$('dd.pump_on').html(pump_on);
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