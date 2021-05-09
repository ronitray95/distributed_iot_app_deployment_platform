import API
import time
import os

min_threshold = 23
max_threshold = 26
dir_path = os.path.dirname(os.path.realpath(__file__))
print("Application on {} executed successfully".format(dir_path))
api = API.sensorapi()
flag = 0
while(True):
    data = api.getData("temp")
    print("*******************",data)
    if data < min_threshold or data > max_threshold: 
        #print("data set")
        if flag and data < 23:
            flag = 0
            api.setData("ac", -1)
            #api.sendNotification("Low({}) temperature detected AC has been turned off".format(data))
            print("Low({}) temperature detected AC has been turned off".format(data))
        if (not flag) and data > 26:
            flag = 1
            api.setData("ac", 20)
            #api.sendNotification("High({}) temperature detected AC has been turned on".format(data))
            print("High({}) temperature detected AC has been turned on".format(data))
        #time.sleep(500)
    time.sleep(1.5)