#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO

import eventlet

import time

extra_files = ['static/js/app.js', 'templates/index.html',]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# Flask app route
@app.route('/')
def index():

    #only by sending this page first will the client be connected to the socketio instance
    #return 'Ok'
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', use_reloader=True, debug=True, extra_files=extra_files, port=3000)