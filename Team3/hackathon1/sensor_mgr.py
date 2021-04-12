#!/usr/bin/env python3

from _thread import *
import random
import time
import socket
import json
from flask import *

from sensor import Sensor

with open('sensor_repo.json') as f:
    sensor_list = json.loads(f.read())

app = Flask(__name__)
registered_sensors = []
INIT_STATE = False


@app.route('/')
def init_sensors():
    global INIT_STATE
    if INIT_STATE:
        return 'Success', 200
    for s in sensor_list:
        si = Sensor(s['id'], s['type'], s['name'],
                    s['ip'], s['port'], s['location'])
        #start_new_thread(si.main, (random.randint(1, 10)))
        registered_sensors.append(si)
    INIT_STATE = True
    return 'Success', 200


@app.route('/fetch')
def fetchSensorData():
    if request.method == 'POST':
        return 'Not supported', 401
    x = request.args.get('id')
    if x is None:
        return 'Sensor ID is absent', 400
    id = int(x)
    sensor_obj = None
    for si in registered_sensors:
        if id == si.id:
            sensor_obj = si

    if sensor_obj is None:
        return 'Invalid sensor ID', 400
    s = socket.socket()
    s.connect((si.ip, si.port))
    s.send('RECV'.encode('utf-8'))
    data = s.recv(100)
    data = data.decode('utf-8')
    #data = data.split(' ')[0]
    s.close()
    return {'low': data, 'high': data}, 200


@app.route('/modify')
def modifySensorData():
    if request.method == 'POST':
        return 'Not supported', 401
    x = request.args.get('id')
    if x is None:
        return 'Sensor ID is absent', 400
    id = int(x)
    l = request.args.get('low')
    h = request.args.get('high')
    if l is None and h is None:
        return 'Atleast one end of range needs to be provided', 400

    l = None if l is None else int(l)
    h = None if h is None else int(h)

    sensor_obj = None
    for si in registered_sensors:
        if id == si.id:
            sensor_obj = si

    if sensor_obj is None:
        return 'Invalid sensor ID', 400
    s = socket.socket()
    s.connect((si.ip, si.port))
    s.send(f'MOD {l} {h}'.encode('utf-8'))
    data = s.recv(100)
    data = data.decode('utf-8')
    #data = data.split(' ')[0]
    s.close()
    return {'status': data}, 200


if __name__ == '__main__':
    app.run(debug=True)
