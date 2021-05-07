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

    def temp_up(self):
        inc = round(random.uniform(0, 1))
        self.temp += inc

    def temp_down(self):
        dec = round(random.uniform(1, 2))
        self.temp -= dec

    def bind_controller(self, obj):
        self.controller = obj
