import API 
import math
import time
import threading

temp_threshold_max = 30
temp_threshold_min = 20
lux_threshold_max = 15
lux_threshold_min = 5

rate = 10 

count = 0

api = API.sensorapi()

iiit_loc= [30.44523, 40.54232]

def calculate_fare(gps, iiit_loc):
    return math.sqrt((float(gps[0])-iiit_loc[0])**2 + (float(gps[1])-iiit_loc[1])**2)*rate

def checkBIO():
    global count
    global gps
    while count <= 15:
    
        biometric = api.getData("BIOMETRIC")["data"][0]
        print(gps)
        fare = calculate_fare(gps[1], iiit_loc)
        api.display(f'{time.ctime()} :: {gps[0]}:{biometric[1]} => Fare : {fare}')
        api.sendMail(f'{time.ctime()} :: {gps[0]}:{biometric[1]} => Fare : {fare}')
        print(fare)
        count += 1

gps = api.getData("GPS")["data"][0]
t1 = threading.Thread(target=checkBIO)
t1.start()


while True:
    #timestamp = time.ctime()
    #{data:[[placeholderID, personID]]}
    #print(biometric)
    gps = api.getData("GPS")["data"][0] #{data:[[placeholderID, [x, y]]}
    print(gps[1])
    
    #print(biometric)
    #print(gps)
    
    if gps[1] != iiit_loc and count > 0:
        
        #if len(biometric) != 0:
        #    fare = calculate_fare(gps[1], iiit_loc)
        #    api.display(f'{time.ctime()} :: {gps[0]}:{biometric[0]} => Fare : {fare}')
        #    api.sendMail(f'{time.ctime()} :: {gps[0]}:{biometric[0]} => Fare : {fare}')
        #    print(fare)
    
        temp = api.getData("TEMP")["data"][0]
        lux = api.getData("LIGHT")["data"][0]

        if temp > 30:
            ack = api.setData(0, "TEMP",1)["data"]
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
