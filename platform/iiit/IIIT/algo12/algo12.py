import API 
import math
import time

temp_threshold_max = 30
temp_threshold_min = 20
lux_threshold_max = 15
lux_threshold_min = 5

rate = 10 

api = API.sensorapi()

iiit_loc= [30.44523, 40.54232]

def calculate_fare(gps, iiit_loc):
    return math.sqrt((gps[0]-iiit_loc[0]**2 + gps[1]-iiit_loc[1]**2))*rate

while True:
    #timestamp = time.ctime()
    biometric = api.getData("BIOMETRIC")["data"] #{data:[placeholderID, x, y]}
    gps = api.getData("GPS")["data"] #{data:[placeholderID, personID]}
    
    print(biometric)
    print(gps)
    
    if gps != iiit_loc:
        
        if len(biometric) != 0:
            fare = calculate_fare(gps[1:], iiit_loc)
            api.display(f'{time.ctime()} :: {gps[0]}:{biometric[0]} => Fare : {fare}')
            api.sendMail(f'{time.ctime()} :: {gps[0]}:{biometric[0]} => Fare : {fare}')
            print(fare)

        temp = api.getData("TEMP")["data"]
        lux = api.getData("LIGHT")["data"]

        if temp > 30:
            ack = api.setData(0, "TEMP",20)["data"]
            if ack == 1:
                api.display(f'{time.ctime()} :: {gps[0]}:High temperature({temp}C) detected! AC has been Turned ON')
        if temp < 20:
            ack = api.setData(0, "TEMP",-1)
            if ack == 1:
                api.display(f'{time.ctime()} :: {gps[0]}:Low temperature({temp}C) detected! AC has been Turned OFF')
        if lux < 5:
            ack = api.setData(0, "LIGHT",1)
            if ack == 1:
                api.display(f'{time.ctime()} :: {gps[0]}:Low intensity light({lux}) detected! Lights has been Turned ON')
        if lux > 15:
            ack = api.setData(0, "LIGHT",-1)
            if ack == 1:
                api.display(f'{time.ctime()} :: {gps[0]}:High intensity light({lux}) detected! Lights has been Turned OFF')

