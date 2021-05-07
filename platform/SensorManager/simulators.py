import random


class ACController:
    def __init__(self, id, name=None, loc=None, status=-1, ip='0.0.0.0', port='1234'):
        self.type = 'ac'
        self.id = id
        self.name = name
        self.location = loc
        self.status = status
        self.ip = ip
        self.port = port

    def turn_on(self):
        self.status = 0

    def turn_off(self):
        self.status = -1


class TempSensor:
    def __init__(self, id, name=None, loc=None, temp=20, ip='0.0.0.0', port='1234'):
        self.type = 'temp'
        self.id = id
        self.name = name
        self.location = loc
        self.temp = temp
        self.ip = ip
        self.port = port
        self.controller = -1
        self.low = 15
        self.high = 45

    def temp_up(self):
        inc = round(random.uniform(0, 1))
        self.temp += inc

    def temp_down(self):
        dec = round(random.uniform(1, 2))
        self.temp -= dec

    def bind_controller(self, obj):
        self.controller = obj

    def genRandom(self):
        value = self.temp
        if self.controller == -1:
            self.temp_up()
        else:
            self.temp_down()
        # return value
        return value, self.controller


class LuxSensor:
    def __init__(self, id, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'lux'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.low = 5
        self.high = 500
        self.controller = -1
        self.lux = 0

    def genRandom(self):
        self.lux = random.randrange(self.low, self.high)
        return 0 if self.controller == -1 else self.lux, self.controller


list_of_people = list(range(50))
list_of_people_boarded = []


class BiometricSensor:
    def __init__(self,  id, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'biometric'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.controller = -1

    def genRandom(self):
        ch = random.choice(list_of_people)
        while ch in list_of_people_boarded:
            ch = random.choice(list_of_people)
        list_of_people_boarded.append(ch)
        return [self.location, ch], self.controller


iiit_loc = [30.44523, 40.54232]
barricades = [[20.34535, 41.34234], [18.42342, 35.45453], [
    24.42342, 56.45453], [27.42342, 60.45453], [10.42342, 21.45453]]
places = [[12.34535, 23.34234], [15.42342, 17.45453], [19.42342, 43.45453], [
    27.321, 60.314], [10.4346, 46.332], [33.4346, 32.332], [10.2, 19.332], [23.12, 49.55]]

gps_weights = [0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]


class GPSSensor:
    def __init__(self,  id, name=None, loc=None, ip='0.0.0.0', port='1234'):
        self.type = 'gps'
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = loc
        self.controller = -1

    def genRandom(self):
        ch = random.choice(gps_weights)
        # if ch == 0:
        #     return [self.location, iiit_loc]
        # elif ch == 1:
        #     return [self.location, random.choice(barricades)]
        # else:
        return [self.location, random.choice(places)], self.controller

