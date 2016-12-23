#!/usr/bin/env python

from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import logging
import argparse
import json
import os, sys

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

class GpioNamespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)

#SOCKETIO = SocketIO('10.0.1.81', 3000)
SOCKETIO = SocketIO('http://xmas-arborist.local', 3000)
GPIO_NAMESPACE = SOCKETIO.define(GpioNamespace, '/gpio')

# GPIO 12 & 16 set up as inputs
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # LOW_WATER sensor
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # WATER_FULL sensor


LOW_WATER = ''
WATER_FULL = ''
PUMP_ON = ''
LIGHTS_ON = ''


def send_tree_update(*message):
    global LOW_WATER, WATER_FULL, PUMP_ON, LIGHTS_ON
    if LOW_WATER == '' or WATER_FULL == '' or PUMP_ON == '' or LIGHTS_ON == '':
        LOW_WATER = is_water_low()
        WATER_FULL = is_water_full()
        PUMP_ON = is_pump_on()
        LIGHTS_ON = are_lights_on()
        GPIO_NAMESPACE.emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON})
    else:
        GPIO_NAMESPACE.emit('tree_update', {'low_water': LOW_WATER, 'water_full': WATER_FULL, 'pump_on': PUMP_ON, 'lights_on': LIGHTS_ON})


#####################################
####### WATER PUMP & LEVELS

def gpio_pump_setup():
    global PUMP_ON

    print("setting up output")
    # GPIO 18 set up as an output
    GPIO.setup(18, GPIO.OUT)

    # set relay to open --> PUMP_ON == False
    GPIO.output(18, 1) # PUMP OFF

    PUMP_ON = False

def is_water_low():
    global LOW_WATER

    if LOW_WATER == '':
        if GPIO.input(12) == 1:
            LOW_WATER = False
        elif GPIO.input(12) == 0:
            LOW_WATER = True

    return LOW_WATER

def is_water_full():
    global WATER_FULL

    if WATER_FULL == '':
        if GPIO.input(16) == 1:
            WATER_FULL = False
        elif GPIO.input(16) == 0:
            WATER_FULL = True

    return WATER_FULL
    #print("LOW_WATER: " + str(LOW_WATER) + " WATER_FULL: " + str(WATER_FULL))


def is_pump_on():
    global PUMP_ON

    #if PUMP_ON == '':
    # export pin
    os.system('echo 18 > /sys/class/gpio/export')

    with open('/sys/class/gpio/gpio18/value') as pin:
        status = pin.read(1)
        if status == 1:
            PUMP_ON = False
        elif status == 0:
            PUMP_ON = True

    return PUMP_ON


# define two threaded callback functions for two water level sensors
def low_water_callback(channel):  # GPIO 12
    global LOW_WATER

    if GPIO.input(12) == 1:
        # set LOW_WATER bool
        LOW_WATER = False

        GPIO_NAMESPACE.emit('low_water', {'low_water': LOW_WATER})

        print("RISING: LOW_WATER == False code here (" + str(GPIO.input(12)) + ")")

    elif GPIO.input(12) == 0:
        LOW_WATER = True
        start_pump()

        GPIO_NAMESPACE.emit('low_water', {'low_water': LOW_WATER})

        print("FALLING: LOW_WATER == True code here (" + str(GPIO.input(12)) + ")")
  
# define two threaded callback functions for two water level sensors
def water_full_callback(channel):  # GPIO 16
    global WATER_FULL, LOW_WATER

    if GPIO.input(16) == 1:
        WATER_FULL = False

        GPIO_NAMESPACE.emit('water_full', {'water_full': WATER_FULL})

        if LOW_WATER == True:
            start_pump()

        print("RISING: WATER_FULL == False code here (" + str(GPIO.input(16)) + ")")

    elif GPIO.input(16) == 0:  # code here when water is full
        WATER_FULL = True
        stop_pump()

        GPIO_NAMESPACE.emit('water_full', {'water_full': WATER_FULL})

        print("FALLING: WATER_FULL == True code here (" + str(GPIO.input(16)) + ")")


# rising edge detection on LOW_WATER pin 12
GPIO.add_event_detect(12, GPIO.BOTH, callback=low_water_callback, bouncetime=300)

# falling edge detection on WATER_FULL pin 16
GPIO.add_event_detect(16, GPIO.BOTH, callback=water_full_callback, bouncetime=300)

def start_pump():
    global PUMP_ON, WATER_FULL

    # double check water_full position
    os.system('echo 16 > /sys/class/gpio/export')

    with open('/sys/class/gpio/gpio16/value') as pin:
        status = pin.read(1)
        if status == 1:
            WATER_FULL = False
        elif status == 0:
            WATER_FULL = True

    if WATER_FULL == True:
        print("error: not starting pump - water is full")
    elif WATER_FULL == False:
        print("starting pump - water is not full")
        # set relay to closed --> PUMP_ON == True
        GPIO.output(18, 0) # PUMP ON
        PUMP_ON = True
        GPIO_NAMESPACE.emit('pump_status', {'pump_on': PUMP_ON})
    
def stop_pump():
    global PUMP_ON
    
    # set relay to open --> PUMP_ON == False
    GPIO.output(18, 1) # PUMP ON
    PUMP_ON = False
    GPIO_NAMESPACE.emit('pump_status', {'pump_on': PUMP_ON})


#####################################
####### LIGHTS

def gpio_lights_setup():
    global LIGHTS_ON

    print("setting up output")
    # GPIO 17 set up as an output
    GPIO.setup(17, GPIO.OUT)

    # set relay to open --> LIGHTS_ON == False
    GPIO.output(17, 1) # LIGHTS OFF

    LIGHTS_ON = False

def switch_lights(*message):
    global LIGHTS_ON

    message_string = json.dumps(message)
    message_dict = json.loads(message_string)[0]
    light_switch_command = message_dict['turn_lights_on']

    if light_switch_command == True:  # turn lights on
        GPIO.output(17, 0)
        LIGHTS_ON = True
        GPIO_NAMESPACE.emit('light_switch', {'lights_on': LIGHTS_ON})

    elif light_switch_command == False:  # turn lights off
        GPIO.output(17, 1)
        LIGHTS_ON = False
        GPIO_NAMESPACE.emit('light_switch', {'lights_on': LIGHTS_ON})

def are_lights_on():
    global LIGHTS_ON

    #if PUMP_ON == '':
    # export pin
    os.system('echo 17 > /sys/class/gpio/export')

    with open('/sys/class/gpio/gpio17/value') as pin:
        status = pin.read(1)
        if status == 1:
            LIGHTS_ON = False
        elif status == 0:
            LIGHTS_ON = True

    return LIGHTS_ON


def create_socket(persistent):
    global SOCKETIO, GPIO_NAMESPACE

    if persistent:
        GPIO_NAMESPACE.on('pull_tree_update', send_tree_update)
        GPIO_NAMESPACE.on('switch_lights', switch_lights)
        SOCKETIO.wait()

    else:
        SOCKETIO.wait(seconds=2)

def main():

    parser = argparse.ArgumentParser(description=__doc__,
                   formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("--persistent", dest="persistent",
        help="number of things", action='store_true', default=False)

    args = vars(parser.parse_args())

    persistent = args['persistent']

    is_water_full()
    is_water_low()
    gpio_pump_setup()
    gpio_lights_setup()
    is_pump_on()
    are_lights_on()

    create_socket(persistent)
    send_tree_update('')


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
