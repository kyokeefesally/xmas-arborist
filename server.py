#!/usr/bin/env python


import socketio
import eventlet
from flask import Flask, render_template, url_for, copy_current_request_context, session, request
from flask_socketio import SocketIO, emit, send

#import RPi.GPIO as GPIO  
#GPIO.setmode(GPIO.BCM) 

# Start with a basic flask app
app = Flask(__name__)

# Flask configs
#app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Extra files to monitor for reloader
extra_files = ['static/js/app.js', 'templates/index.html',]

#turn the flask app into a socketio app
socketio = SocketIO(app, debug=True, engineio_options={'logger': True}, engineio_logger=True)

'''
# GPIO 12 & 16 set up as inputs
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # low_water sensor
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # water_full sensor

low_water = ''
water_full = ''

def get_water_levels():
    global low_water, water_full

    if low_water == '':
        if GPIO.input(12) == 1:
            low_water = False
        elif GPIO.input(12) == 0:
            low_water = True
    if water_full == '':
        if GPIO.input(16) == 1:
            water_full = False
        elif GPIO.input(16) == 0:
            water_full = True

# define two threaded callback functions for two water level sensors
def low_water_callback(channel):  # GPIO 12
    global low_water

    if GPIO.input(12) == 1:
        # set low_water bool
        low_water = False

        #emit_low_water_value()
        #web_pull('hey')
        #socketio.emit('test', broadcast=True)
        #socketio.emit('low_water', {'low_water': low_water}, broadcast=True, namespace='/web')
        socketio.emit('tree_update', {'low_water': low_water, 'water_full': water_full}, broadcast=True)

        print("RISING: low_water == False code here (" + str(GPIO.input(12)) + ")")

    elif GPIO.input(12) == 0:
        low_water = True

        #emit_low_water_value()
        #socketio.emit('low_water', {'low_water': low_water}, broadcast=True, namespace='/web')
        socketio.emit('tree_update', {'low_water': low_water, 'water_full': water_full}, broadcast=True)

        print("FALLING: low_water == True code here (" + str(GPIO.input(12)) + ")")
  
# define two threaded callback functions for two water level sensors
def water_full_callback(channel):  # GPIO 16
    global water_full

    if GPIO.input(16) == 1:
        water_full = False

        #emit_water_full_value()
        socketio.emit('water_full', {'water_full': water_full}, broadcast=True, namespace='/web')

        print("RISING: water_full == False code here (" + str(GPIO.input(16)) + ")")

    elif GPIO.input(16) == 0:  # code here when water is full
        water_full = True

        #emit_water_full_value()
        socketio.emit('water_full', {'water_full': water_full}, broadcast=True, namespace='/web')

        print("FALLING: water_full == True code here (" + str(GPIO.input(16)) + ")")


# rising edge detection on low_water pin 12
GPIO.add_event_detect(12, GPIO.BOTH, callback=low_water_callback, bouncetime=300)

# falling edge detection on water_full pin 16
GPIO.add_event_detect(16, GPIO.BOTH, callback=water_full_callback, bouncetime=300)


def emit_low_water_value():
    global low_water

    if low_water == '':
        get_water_levels()
        socketio.emit('low_water', {'low_water': low_water})
    else:
        socketio.emit('low_water', {'low_water': low_water})


def emit_water_full_value():
    global water_full

    if water_full == '':
        get_water_levels()
        socketio.emit('water_full', {'water_full': water_full})
    else:
        socketio.emit('water_full', {'water_full': water_full})
'''

# Flask app route
@app.route('/')
def index():

    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

'''
#####################################################################
#  Events when server comes online (no namespace)
#####################################################################
@socketio.on('connect')
def on_connect():
    print("Client Connected")
'''

#####################################################################
#  Events when web clients connect to server (namespace='/web')
#####################################################################
@socketio.on('connect')
def web_connect():
    print('Web Client Connected')

'''
@socketio.on('web_pull')
def web_pull(message):
    global low_water, water_full
    
    print(message)

    if low_water == '' or water_full == '':
        get_water_levels()
        emit('tree_update', {'low_water': low_water, 'water_full': water_full}, broadcast=True)

    else:
        emit('tree_update', {'low_water': low_water, 'water_full': water_full}, broadcast=True)
        emit('low_water', {'low_water': low_water}, broadcast=True)
        emit('water_full', {'water_full': water_full}, broadcast=True)
'''

@socketio.on('test')
def test(message):
    print("TEST SUCCESSFUL!!!!!!!!")



if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=['static/js/app.js', 'templates/index.html',], port=5000)
    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)


