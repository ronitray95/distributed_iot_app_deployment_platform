import sys
from commAPI import obj
import json

class sensorapi(object):

    def __init__(self):
        self.sensor_count = int()
        self.controller_count = int()
        #self.sensor = {"temp":"","ldr":"","ac":""}
        self.sensor = {}
        self.bindSensors()

    def setSensorCount(self, count):
        self.sensor_count = count

    def setControllerCount(self, count):
        self.controller_count = count

    def bindSensors(self):
        with open("conf.json", "r") as f:
            data = json.loads(f.read())
            for k,v in data.items():
                for j in v:
                    self.sensor[j] = v[j]
        #print(self.sensor["temp"])

    def getData(self, sensor):
        #print(self.sensor[sensor])
        return obj.getData(self.sensor[sensor])
        
    def setData(self, sensor, value):
        return obj.setData(self.sensor[sensor], value)
        
    def addSensorType(sensor):
        pass
    def removeSensorType(sensor):
        pass
    def addControllerType(sensor):
        pass
    def removeControllerType(sensor):
        pass
    def sendNotification(self, msg):
        obj.sendNotification(msg)