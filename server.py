#!/usr/bin/env python

#import socketio
from flask import Flask, render_template, redirect, url_for, request, copy_current_request_context, session
from functools import wraps

from flask_socketio import SocketIO, emit
import eventlet
import socketio

'''
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM) 
'''

from datetime import datetime
from pytz import timezone

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient

import imp
config = imp.load_source('config', '/home/pirate/CODE/secrets/config.py')
from config import ACCOUNT_SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER


# Start with a basic flask app
app = Flask(__name__)

# Flask configs
#app.config['SECRET_KEY'] = 'secret!'
app.secret_key = "secrettttt!"
app.config['DEBUG'] = True

# Extra files to monitor for reloader
extra_files = ['static/js/app.js', 'templates/index.html',]

#turn the flask app into a socketio app
socketio = SocketIO(app, debug=True, engineio_options={'logger': True}, engineio_logger=True)

LOW_WATER = ''
WATER_FULL = ''
PUMP_ON = ''
LIGHTS_ON = ''
LOW_SMS = False
FULL_SMS = False

'''
# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap
'''

# Flask app route
@app.route('/')
#@login_required
def home():

    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

'''
# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
'''


#####################################################################
#  Events when server comes online (no namespace)
#####################################################################
@socketio.on('connect', namespace='/gpio')
def on_connect():
    global LOW_WATER, WATER_FULL, PUMP_ON, LIGHTS_ON

    print("Client Connected")

    if LOW_WATER == '' or WATER_FULL == '' or PUMP_ON == '' or LIGHTS_ON == '':
        emit('pull_tree_update', broadcast=True, namespace='/gpio')
    else:
        emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')

#####################################################################
#  Events when web clients connect to server (namespace='/web')
#####################################################################
@socketio.on('connect', namespace='/web')
def web_connect():
    global LOW_WATER, WATER_FULL, PUMP_ON, LIGHTS_ON

    print('Web Client Connected')

    if LOW_WATER == '' or WATER_FULL == '' or PUMP_ON == '' or LIGHTS_ON == '':
        emit('pull_tree_update', broadcast=True, namespace='/gpio')
    else:
        emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')


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
    global LOW_WATER, WATER_FULL, PUMP_ON, LIGHTS_ON

    LOW_WATER = message['low_water']
    WATER_FULL = message['water_full']
    PUMP_ON = message['pump_on']
    LIGHTS_ON = message['lights_on']

    print(message)

    emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')


@socketio.on('low_water', namespace='/gpio')
def low_water_message(message):
    #global LOW_WATER
    global LIGHTS_ON, PUMP_ON, LOW_WATER, WATER_FULL

    LOW_WATER = message['low_water']

    #emit('low_water', {'low_water': LOW_WATER}, broadcast=True, namespace='/web')
    emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')


@socketio.on('water_full', namespace='/gpio')
def water_full_message(message):
    #global WATER_FULL
    global LIGHTS_ON, PUMP_ON, LOW_WATER, WATER_FULL

    WATER_FULL = message['water_full']

    #emit('water_full', {'water_full': WATER_FULL}, broadcast=True, namespace='/web')
    emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')

@socketio.on('pump_status', namespace='/gpio')
def pump_status_message(message):
    #global PUMP_ON
    global LIGHTS_ON, PUMP_ON, LOW_WATER, WATER_FULL

    print('PUUUMPPP')

    PUMP_ON = message['pump_on']

    #emit('pump_status', {'pump_on': PUMP_ON}, broadcast=True, namespace='/web')
    emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')
    send_sms(PUMP_ON)

def send_sms(PUMP_ON):
    global LOW_SMS, FULL_SMS, ACCOUNT_SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER

    # Find these values at https://twilio.com/user/account

    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    to_number = TO_NUMBER
    from_number = FROM_NUMBER
    client = TwilioRestClient(account_sid, auth_token)

    fmt = "(%a %b %-d | %-I:%M %p)"
    now_time = datetime.now(timezone('US/Eastern'))
    ts = now_time.strftime(fmt)

    PUMP_ON = PUMP_ON

    if PUMP_ON == True:
        if LOW_SMS == False:
            message = client.messages.create(to=to_number, from_=from_number, body="Low water! Pump started. " + ts)
            LOW_SMS = True
            FULL_SMS = False

    elif PUMP_ON == False:
        if FULL_SMS == False:
            message = client.messages.create(to=to_number, from_=from_number, body="Water full. Pump stopped. " + ts)
            FULL_SMS = True
            LOW_SMS = False

@socketio.on('light_switch', namespace='/web')
def light_switch_command(message):
    #global LIGHTS_ON
    print("RECEIVED WEB LIGHT SWITCH")

    turn_lights_on = message['lights_on']

    emit('switch_lights', {'turn_lights_on': turn_lights_on}, broadcast=True, namespace='/gpio')


@socketio.on('light_switch', namespace='/gpio')
def light_switch_response(message):
    global LIGHTS_ON, PUMP_ON, LOW_WATER, WATER_FULL

    LIGHTS_ON = message['lights_on']

    #emit('light_status', {'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')
    emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON}, broadcast=True, namespace='/web')

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=['static/js/app.js', 'templates/index.html',], port=5000)
    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)


