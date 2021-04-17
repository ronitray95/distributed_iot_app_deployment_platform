import socket, sys, os, threading, time
from _thread import *
import random

#global
# port = 8001
# host = "localhost"
buffer_size = 4096

#connection
def client_socket_creation(server_host, server_port):

    clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #connection
    try:
        clientsocket.connect((server_host,server_port))
    except:
        print("error in connecting to server !")
        exit()

    msg = "Hello from client !"
    clientsocket.send(msg.encode())
    msg = clientsocket.recv(buffer_size).decode()
    # print(msg,"Connection established!")
    while True:
        # msg = input("Enter msg: ")
        msg = str(random.randint(1,1000))
        # print(msg)
        clientsocket.send(msg.encode())
        msg = ""
        msg = clientsocket.recv(buffer_size).decode()
        # print(msg)

        time.sleep(1)

    clientsocket.close()


#functions
if __name__ == "__main__":
    # command line argument 'host:port'
    arg_list = sys.argv
    # print(arg_list)

    server_host = "127.0.0.1"
    server_port = 9000
    if len(arg_list) > 1:
        server_host_port = arg_list[1].split(":")
        server_host = server_host_port[0]
        server_port = int(server_host_port[1])
    # print(host,port)

    # thread for creating client socket
    t1 = threading.Thread(target = client_socket_creation,args=(server_host,server_port, ))

    t1.start()