import os
from commAPI import obj
import json
 
class sensorapi(object): 

    def __init__(self):
        self.sensor = {}
        self.emailID = ''
        self.outputfile = ''
        self.binder()

    def binder(self):
        with open("conf.json", "r") as f:
            data = json.loads(f.read())
            for i in data.keys():
                self.sensor = data['sensors']
                self.userID = data['userID']
                self.emailID = obj.getEmailID(self.userID)
                self.outputfile = data['outputfile']

    def getData(self, sensor):
        return obj.getData(sensor, self.sensor[sensor])
        
    def setData(self, index, sensor, value):
        return obj.setData(self.sensor[sensor][index], value)
        
    def sendMail(self, msg):
        obj.sendMail(self.emailID, msg)

    def display(self, line):
        with open(self.outputfile, 'a') as f:
            f.write(line + '\n')

    def getEmailID(self):
        return self.emailID

    def trigger(self, algo):
        path = os.path.abspath(algo)
        obj.trigger(path)