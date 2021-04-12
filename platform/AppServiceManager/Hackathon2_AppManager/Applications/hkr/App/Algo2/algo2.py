import API
import time

min_threshold = 15
max_threshold = 28

api = API.sensorapi()
while(True):
    data = api.getData("temp")
    if data < min_threshold or data > max_threshold:
        ack = api.setData("ac", 20) 
        if data < 15:
            api.sendNotification("Low({}) temperature detected AC has been turned off".format(data))
        if data > 28:
            api.sendNotification("High({}) temperature detected AC has been turned on".format(data))
        time.sleep(20)
    time.sleep(5)