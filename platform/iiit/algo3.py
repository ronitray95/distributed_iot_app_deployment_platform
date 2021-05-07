import API
import time
import math
 
def calculate_dist(gps, iiit_loc):
    return math.sqrt((gps[0]-iiit_loc[0]**2 + gps[1]-iiit_loc[1]**2))

api = API.sensorapi()

min_radius = 10

gps = api.getData("GPS")["data"]  #{data:[[placeholderID,x,y],[placeholderID,x,y]]}

i=0
while i<len(gps):
    j=i+1
    while j<len(gps):
        k=j+1
        len1 = calculate_dist(gps[i][1:],gps[j][1:])
        while k<len(gps):
            len2 = calculate_dist(gps[j][1:],gps[k][1:])
            if len1 < min_radius and len2 < min_radius:
                ack = api.setData(k, "GPS", 1)
                if ack:
                    api.display(f'{time.ctime()} :: Buses found close!! Buzzer sent to {gps[i][0]} {gps[j][0]}')

