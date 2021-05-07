import API
import math

def calculate_dist(gps, iiit_loc):
    return math.sqrt((gps[0]-iiit_loc[0]**2 + gps[1]-iiit_loc[1]**2))

barricades = [[20.34535, 41.34234], [18.42342, 35.45453], [24.42342, 56.45453], [27.42342, 60.45453], [10.42342, 21.45453]]
 
api = API.sensorapi()

min_dist = 10

while True:
    gps = api.getData["GPS"]["data"]
    #for i in gps:
    for b in barricades:
        len = calculate_dist(gps[1:], b)
        if len < min_dist:
            conf = {"email":api.getEmailID()}
            api.trigger("EmailService.py")
