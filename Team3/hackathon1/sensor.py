#!/usr/bin/env python3

from _thread import *
import random
import time
import socket
import json
import socket


class Sensor:
    def __init__(self, id, type, name, ip, port, location):
        self.id = id
        self.type = type
        self.name = name
        self.ip = ip
        self.port = port
        self.location = location
        self.listenSocket = socket.socket()
        self.low = 5
        self.high = 500
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
        value = random.randrange(self.low, self.high)
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
                    self.low = int(params[1])
                    resp += 'Changed low variable'
                if params[2] != 'None':
                    self.high = int(params[1])
                    resp += '\nChanged high variable'
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

# if __name__ == '__main__':
#     #start_new_thread(main, (1, 5, 5))
#     start_new_thread(main, (6, 10, 10))
#     input('Press ENTER to quit simuation\n')
