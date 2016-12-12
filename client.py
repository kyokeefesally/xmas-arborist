#!/usr/bin/env python

from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import logging
import argparse
import json

import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM) 

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

SOCKETIO = SocketIO('xmas-arborist', 3000)

# GPIO 12 & 16 set up as inputs
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # low_water sensor
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # water_full sensor

low_water = ''
water_full = ''

def send_tree_update(*message):
    if low_water == '' or water_full == '':
        get_water_levels()
    else:
        SOCKETIO.emit('tree_update', {'low_water': low_water, 'water_full': water_full})

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
    print("low_water: " + str(low_water) + " water_full: " + str(water_full))

# define two threaded callback functions for two water level sensors
def low_water_callback(channel):  # GPIO 12
    global low_water

    if GPIO.input(12) == 1:
        # set low_water bool
        low_water = False

        SOCKETIO.emit('low_water', {'low_water': low_water})

        print("RISING: low_water == False code here (" + str(GPIO.input(12)) + ")")

    elif GPIO.input(12) == 0:
        low_water = True

        SOCKETIO.emit('low_water', {'low_water': low_water})

        print("FALLING: low_water == True code here (" + str(GPIO.input(12)) + ")")
  
# define two threaded callback functions for two water level sensors
def water_full_callback(channel):  # GPIO 16
    global water_full

    if GPIO.input(16) == 1:
        water_full = False

        SOCKETIO.emit('water_full', {'water_full': water_full})

        print("RISING: water_full == False code here (" + str(GPIO.input(16)) + ")")

    elif GPIO.input(16) == 0:  # code here when water is full
        water_full = True

        SOCKETIO.emit('water_full', {'water_full': water_full})

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

def create_socket(persistent):
    global SOCKETIO, USB_NAMESPACE, DATA

    if persistent:
        SOCKETIO.on('server_pull_tree_update', send_tree_update)
        SOCKETIO.wait()

    else:
        SOCKETIO.wait(seconds=2)

def main():
    global DATA

    parser = argparse.ArgumentParser(description=__doc__,
                   formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--persistent", dest="persistent",
        help="number of things", action='store_true', default=False)

    args = vars(parser.parse_args())

    persistent = args['persistent']

    create_socket(persistent)
    get_water_levels()
    send_tree_update('')


if __name__ == "__main__":
    main()