#!/bin/usr/env python

from flask import Flask, render_template
from flask_socketio import SocketIO

import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM) 

# Start with a basic flask app
app = Flask(__name__)

# Flask configs
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

# Extra files to monitor for reloader
extra_files = ['static/js/app.js', 'templates/index.html',]

#turn the flask app into a socketio app
socketio = SocketIO(app, debug=True)


# Flask app route
@app.route('/')
def index():

    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')




if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=['static/js/app.js', 'templates/index.html',], port=5000)
    #socketio.run(app, host='0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=5000)


