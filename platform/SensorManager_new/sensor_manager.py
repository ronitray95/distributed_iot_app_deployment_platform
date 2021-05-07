#!/usr/bin/env python3

from _thread import *
import random
import time
import socket
import json
from flask import *

from sensor import *

sensor_list = []

f=open('registry.txt')
sensor_list = f.readlines()

app = Flask(__name__)
registered_sensors = []
INIT_STATE = False


@app.route('/')
def init_sensors():
	global INIT_STATE
	if INIT_STATE:
		return 'Success', 200
	for s in sensor_list:
		sensor_details=s.split(' ')
		obj=None
		if sensor_details[0]=='temperature':
			obj=TemperatureSensor(sensor_details[1],sensor_details[0],sensor_details[3],sensor_details[4],sensor_details[2])
		elif sensor_details[0]=='lux':
			obj=LuxSensor(sensor_details[1],sensor_details[0],sensor_details[3],sensor_details[4],sensor_details[2])
		elif sensor_details[0]=='gps':
			obj=GPSSensor(sensor_details[1],sensor_details[0],sensor_details[3],sensor_details[4],sensor_details[2])
		elif sensor_details[0]=='biometric':
			obj=BiometricSensor(sensor_details[1],sensor_details[0],sensor_details[3],sensor_details[4],sensor_details[2])
		#start_new_thread(si.main, (random.randint(1, 10)))
		registered_sensors.append(obj)
	INIT_STATE = True
	return 'Success', 200


@app.route('/fetch')
def fetchSensorData():
	if not INIT_STATE:
		init_sensors()
	if request.method == 'POST':
		return 'Not supported', 401
	x = request.args.get('sensor')
	if x is None:
		return 'Sensor ID is absent', 400
	data=[]
	for id in x:
		sensorObj=None
		for sensor in registered_sensors:
			if sensor.id == id:
				sensorObj = sensor
				break
		if sensorObj is None:
			return 'Invalid sensor ID', 400

		s = socket.socket()
		s.connect((sensorObj.ip, sensorObj.port))
		s.send('RECV'.encode('utf-8'))
		d = s.recv(100)
		d = d.decode('utf-8')
		data.append(d)
		s.close()
	return {'sensor': data}, 200


@app.route('/modify')
def modifySensorData():
	if not INIT_STATE:
		init_sensors()
	if request.method == 'POST':
		return 'Not supported', 401
	x = request.args.get('controller')
	if x is None:
		return 'Controller ID is absent', 400
	d = dict(x)
	key = list(d.keys())[0]
	sensorObj = None
	for sensor in registered_sensors:
		if sensor.id == key:
			sensorObj = sensor
			break
	if sensorObj is None:
		return 'Invalid sensor ID', 400
	l = int(d[key])
	s = socket.socket()
	s.connect((sensorObj.ip, sensorObj.port))
	s.send(f'MOD {l}'.encode('utf-8'))
	data = s.recv(100)
	data = data.decode('utf-8')
	#data = data.split(' ')[0]
	s.close()
	return {'status': 'Success'}, 200


if __name__ == '__main__':
	app.run(debug=True,port=9000)
