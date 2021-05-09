import sys
from commAPI import obj
import json

class sensorapi(object):

    def __init__(self):
        self.sensor_count = int()
        self.controller_count = int()
        self.sensor = {"temp":"","ldr":"","ac":""}
        
    def setSensorCount(self, count):
        self.sensor_count = count

    def setControllerCount(self, count):
        self.controller_count = count

    def bindSensors(self):
        with open(self.clocation, "r") as f:
            data = json.loads(f.read())
            for i in data.keys():
                self.sensor[i] = data[i]

    def getData(self, sensor):
        return obj.getData(sensor, self.sensor[sensor])
        
    def setData(self, sensor, value):
        return obj.setData(sensor, self.sensor[sensor], value)
        
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