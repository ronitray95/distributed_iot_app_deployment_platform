#!/usr/bin/env python3

from _thread import *
import random
import time
import socket
import json
import socket


class TemperatureSensor:
    def __init__(self, id, name, ip, port, location):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = location
        self.listenSocket = socket.socket()
        self.low = 15
        self.high = 45
        self.delay = 1
        self.isIncreasing = 1
        self.temp = 25

        try:
            self.listenSocket.bind((ip, port))
        except Exception as e:
            print('Bind Failed. Exception occured:', str(e))
            return
        self.listenSocket.listen(4)  # max queued clients=4
        print('Listening on http://' + ip + ':' + str(port))
        start_new_thread(self.startListen, ())
        self.start()

    def genRandom(self):
        #id = random.randint(l, h)
        time.sleep(self.delay)
        value = self.temp
        self.temp = self.temp+1 if self.isIncreasing == 1 else self.temp-1
        if self.temp < self.low:
            self.temp = self.low
        if self.temp > self.high:
            self.temp = self.high
        return value

    def startListen(self):
        while True:
            c, a = self.listenSocket.accept()
            instruction = c.recv(100).decode('utf-8')
            if instruction == 'RECV':
                c.send(str(self.genRandom()).encode('utf-8'))
                c.close()
            elif instruction.startswith('MOD'):
                params = instruction.split(' ')
                resp = ''
                if params[1] != 'None':
                    self.isIncreasing = int(params[1])
                    resp += 'Changed temperature controller'
                c.send(resp.encode('utf-8'))
                c.close()

            #print('Client', a[0], ':', a[1], 'connected')

        listenSocket.close()

    def start(self):
        print(
            f'Started sensor {self.name} with ID {self.id} at {self.ip}:{self.port}')
        #input('Press ENTER to quit simuation\n')

    def stop(self):
        self.listenSocket.close()
        quit()


class LuxSensor:
    def __init__(self, id, name, ip, port, location):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = location
        self.listenSocket = socket.socket()
        self.low = 5
        self.high = 500
        self.delay = 1
        self.isOn = 1

        try:
            self.listenSocket.bind((ip, port))
        except Exception as e:
            print('Bind Failed. Exception occured:', str(e))
            return
        self.listenSocket.listen(4)  # max queued clients=4
        print('Listening on http://' + ip + ':' + str(port))
        start_new_thread(self.startListen, ())
        self.start()

    def genRandom(self):
        #id = random.randint(l, h)
        time.sleep(self.delay)
        value = random.randrange(self.low, self.high)
        return 0 if self.isOn == 0 else value

    def startListen(self):
        while True:
            c, a = self.listenSocket.accept()
            instruction = c.recv(100).decode('utf-8')
            if instruction == 'RECV':
                c.send(str(self.genRandom()).encode('utf-8'))
                c.close()
            elif instruction.startswith('MOD'):
                params = instruction.split(' ')
                resp = ''
                if params[1] != 'None':
                    self.isOn = 0 if int(params[1]) == -1 else 1
                    resp += '\nChanged lux sensor'
                c.send(resp.encode('utf-8'))
                c.close()

            #print('Client', a[0], ':', a[1], 'connected')

        listenSocket.close()

    def start(self):
        print(
            f'Started sensor {self.name} with ID {self.id} at {self.ip}:{self.port}')
        #input('Press ENTER to quit simuation\n')

    def stop(self):
        self.listenSocket.close()
        quit()


list_of_people = list(range(50))
list_of_people_boarded = []


class BiometricSensor:
    def __init__(self, id, name, ip, port, location):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = location
        self.listenSocket = socket.socket()
        self.delay = 1

        try:
            self.listenSocket.bind((ip, port))
        except Exception as e:
            print('Bind Failed. Exception occured:', str(e))
            return
        self.listenSocket.listen(4)  # max queued clients=4
        print('Listening on http://' + ip + ':' + str(port))
        start_new_thread(self.startListen, ())
        self.start()

    def genRandom(self):
        #id = random.randint(l, h)
        time.sleep(self.delay)
        ch = random.choice(list_of_people)
        while ch in list_of_people_boarded:
            ch = random.choice(list_of_people)
        list_of_people_boarded.append(ch)
        return [self.location, ch]
        # value = random.randrange(self.low, self.high)
        # return value

    def startListen(self):
        while True:
            c, a = self.listenSocket.accept()
            instruction = c.recv(100).decode('utf-8')
            if instruction == 'RECV':
                c.send(str(self.genRandom()).encode('utf-8'))
                c.close()
            elif instruction.startswith('MOD'):
                params = instruction.split(' ')
                resp = ''
                if params[1] != 'None':
                    bioID = int(params[1])
                    if bioID in list_of_people_boarded:
                        resp += f'Person with id {bioID} left the bus'
                        list_of_people_boarded.remove(bioID)
                c.send(resp.encode('utf-8'))
                c.close()

            #print('Client', a[0], ':', a[1], 'connected')

        listenSocket.close()

    def start(self):
        print(
            f'Started sensor {self.name} with ID {self.id} at {self.ip}:{self.port}')
        #input('Press ENTER to quit simuation\n')

    def stop(self):
        self.listenSocket.close()
        quit()


iiit_loc = [30.44523, 40.54232]
barricades = [[20.34535, 41.34234], [18.42342, 35.45453], [
    24.42342, 56.45453], [27.42342, 60.45453], [10.42342, 21.45453]]
places = [[12.34535, 23.34234], [15.42342, 17.45453], [19.42342, 43.45453], [
    27.321, 60.314], [10.4346, 46.332], [33.4346, 32.332], [10.2, 19.332], [23.12, 49.55]]

gps_weights = [0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2]


class GPSSensor:
    def __init__(self, id, name, ip, port, location):
        self.id = id
        self.name = name
        self.ip = ip
        self.port = port
        self.location = location
        self.listenSocket = socket.socket()
        self.delay = 1

        try:
            self.listenSocket.bind((ip, port))
        except Exception as e:
            print('Bind Failed. Exception occured:', str(e))
            return
        self.listenSocket.listen(4)  # max queued clients=4
        print('Listening on http://' + ip + ':' + str(port))
        start_new_thread(self.startListen, ())
        self.start()

    def genRandom(self):
        #id = random.randint(l, h)
        time.sleep(self.delay)
        ch = random.choice(gps_weights)
        # if ch == 0:
        #     return [self.location, iiit_loc]
        # elif ch == 1:
        #     return [self.location, random.choice(barricades)]
        # else:
        return [self.location, random.choice(places)]
        # value = random.randrange(self.low, self.high)
        # return value

    def startListen(self):
        while True:
            c, a = self.listenSocket.accept()
            instruction = c.recv(100).decode('utf-8')
            if instruction == 'RECV':
                c.send(str(self.genRandom()).encode('utf-8'))
                c.close()
            elif instruction.startswith('MOD'):
                pass  # GPS canno be modded
                # params = instruction.split(' ')
                # resp = ''
                # if params[1] != 'None':
                #     self.low = int(params[1])
                #     resp += 'Changed low variable'
                # if params[2] != 'None':
                #     self.high = int(params[1])
                #     resp += '\nChanged high variable'
                # c.send(resp.encode('utf-8'))
                # c.close()

            #print('Client', a[0], ':', a[1], 'connected')

        listenSocket.close()

    def start(self):
        print(
            f'Started sensor {self.name} with ID {self.id} at {self.ip}:{self.port}')
        #input('Press ENTER to quit simuation\n')

    def stop(self):
        self.listenSocket.close()
        quit()
