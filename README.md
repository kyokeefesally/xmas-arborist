# xmas-arborist
A Raspberry Pi based Christmas tree watering and lighting control system with Flask Socket-IO web dashboard
## Getting Started
```bash
# Update/Upgrade
$ sudo apt-get update
$ sudo apt-get -y upgrade

# Install rmate
$ git clone https://github.com/kyokeefesally/rmatey
$ sudo bash rmatey/rmatey

# Clean Up rmatey
$ sudo rm -R rmatey

# Install Pip
$ sudo apt-get -y install python-pip

$ sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev
$ sudo apt-get -y install libevent-dev
$ sudo apt-get -y install python-all-dev

$ sudo apt-get -y install libnss-mdns

# Install Flask Socket-IO
$ sudo pip install flask-socketio

# install eventlet
$ sudo pip install eventlet

# install RPi.GPIO
$ sudo apt-get -y install python-dev python-rpi.gpio

$ sudo pip install socketIO-client-2

$ sudo apt-get remove python-pip
$ sudo easy_install pip

$ sudo pip install gevent-socketio

$ sudo pip uninstall gevent-socketio
$ sudo pip install python-socketio  # already installed

# export PYTHONPATH=$HOME/.local/lib/python/site-packages:$PYTHONPATH
# export PYTHONPATH=$HOME/.local/lib/python2.7/site-packages:$PYTHONPATH
# export PATH=$HOME/.local/bin:$PATH


```
