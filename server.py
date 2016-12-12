#!/usr/bin/env python


import socketio
import eventlet
from flask import Flask, render_template, url_for, copy_current_request_context, session, request
from flask_socketio import SocketIO, emit, send

'''
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM) 
'''

# Start with a basic flask app
app = Flask(__name__)

# Flask configs
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Extra files to monitor for reloader
extra_files = ['static/js/app.js', 'templates/index.html',]

#turn the flask app into a socketio app
socketio = SocketIO(app, debug=True, engineio_options={'logger': True}, engineio_logger=True)

LOW_WATER = ''
WATER_FULL = ''

'''
# GPIO 12 & 16 set up as inputs
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # LOW_WATER sensor
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # WATER_FULL sensor

LOW_WATER = ''
WATER_FULL = ''

def get_water_levels():
    global LOW_WATER, WATER_FULL

    if LOW_WATER == '':
        if GPIO.input(12) == 1:
            LOW_WATER = False
        elif GPIO.input(12) == 0:
            LOW_WATER = True
    if WATER_FULL == '':
        if GPIO.input(16) == 1:
            WATER_FULL = False
        elif GPIO.input(16) == 0:
            WATER_FULL = True

# define two threaded callback functions for two water level sensors
def low_water_callback(channel):  # GPIO 12
    global LOW_WATER

    if GPIO.input(12) == 1:
        # set LOW_WATER bool
        LOW_WATER = False

        #emit_low_water_value()
        #web_pull('hey')
        #socketio.emit('test', broadcast=True)
        socketio.emit('low_water', {'low_water': LOW_WATER}, broadcast=True, namespace='/web')
        #socketio.emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')

        print("RISING: LOW_WATER == False code here (" + str(GPIO.input(12)) + ")")

    elif GPIO.input(12) == 0:
        LOW_WATER = True

        #emit_low_water_value()
        socketio.emit('low_water', {'low_water': LOW_WATER}, broadcast=True, namespace='/web')
        #socketio.emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')

        print("FALLING: LOW_WATER == True code here (" + str(GPIO.input(12)) + ")")
  
# define two threaded callback functions for two water level sensors
def water_full_callback(channel):  # GPIO 16
    global WATER_FULL

    if GPIO.input(16) == 1:
        WATER_FULL = False

        #emit_water_full_value()
        socketio.emit('water_full', {'water_full': WATER_FULL}, broadcast=True, namespace='/web')

        print("RISING: WATER_FULL == False code here (" + str(GPIO.input(16)) + ")")

    elif GPIO.input(16) == 0:  # code here when water is full
        WATER_FULL = True

        #emit_water_full_value()
        socketio.emit('water_full', {'water_full': WATER_FULL}, broadcast=True, namespace='/web')

        print("FALLING: WATER_FULL == True code here (" + str(GPIO.input(16)) + ")")


# rising edge detection on LOW_WATER pin 12
GPIO.add_event_detect(12, GPIO.BOTH, callback=low_water_callback, bouncetime=300)

# falling edge detection on WATER_FULL pin 16
GPIO.add_event_detect(16, GPIO.BOTH, callback=water_full_callback, bouncetime=300)


def emit_low_water_value():
    global LOW_WATER

    if LOW_WATER == '':
        get_water_levels()
        socketio.emit('low_water', {'low_water': LOW_WATER})
    else:
        socketio.emit('low_water', {'low_water': LOW_WATER})


def emit_water_full_value():
    global WATER_FULL

    if WATER_FULL == '':
        get_water_levels()
        socketio.emit('water_full', {'water_full': WATER_FULL})
    else:
        socketio.emit('water_full', {'water_full': WATER_FULL})
'''

# Flask app route
@app.route('/')
def index():

    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


#####################################################################
#  Events when server comes online (no namespace)
#####################################################################
@socketio.on('connect', namespace='/gpio')
def on_connect():
    global LOW_WATER, WATER_FULL

    print("Client Connected")

    if LOW_WATER == '' or WATER_FULL == '':
        emit('pull_tree_update', broadcast=True, namespace='/gpio')
    else:
        emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')

#####################################################################
#  Events when web clients connect to server (namespace='/web')
#####################################################################
@socketio.on('connect', namespace='/web')
def web_connect():
    global LOW_WATER, WATER_FULL

    print('Web Client Connected')

    if LOW_WATER == '' or WATER_FULL == '':
        emit('pull_tree_update', broadcast=True, namespace='/gpio')
    else:
        emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')


@socketio.on('web_pull', namespace='/web')
def web_pull(message):
    global LOW_WATER, WATER_FULL
    emit('pull_tree_update', broadcast=True, namespace='/gpio')
    
    print(message)
'''
    if LOW_WATER == '' or WATER_FULL == '':
        get_water_levels()
        emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')

    else:
        emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')
        #emit('low_water', {'low_water': LOW_WATER}, broadcast=True)
        #emit('water_full', {'water_full': WATER_FULL}, broadcast=True)
'''

@socketio.on('tree_update', namespace='/gpio')
def tree_update(message):
    global LOW_WATER, WATER_FULL

    LOW_WATER = message['low_water']
    WATER_FULL = message['water_full']

    emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL}, broadcast=True, namespace='/web')


@socketio.on('low_water', namespace='/gpio')
def tree_update(message):
    global LOW_WATER

    LOW_WATER = message['low_water']

    emit('low_water', {'low_water': LOW_WATER}, broadcast=True, namespace='/web')


@socketio.on('water_full', namespace='/gpio')
def tree_update(message):
    global WATER_FULL

    WATER_FULL = message['water_full']

    emit('water_full', {'water_full': WATER_FULL}, broadcast=True, namespace='/web')

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=['static/js/app.js', 'templates/index.html',], port=5000)
    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)


