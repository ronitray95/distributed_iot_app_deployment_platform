import socket, sys, os, threading, time
from _thread import *

# global
# port = 8001
# host = "localhost"
buffer_size = 4096
data_list = [""]
index = 1


# connection
def sensors_interaction(socket, address):
    global data_list
    msg = socket.recv(buffer_size).decode()
    print("Sensor says: ", msg)
    response = "Received"
    socket.send(response.encode())
    while (1):
        data = socket.recv(buffer_size).decode()
        print("Sensor data: ", data)
        data_list.append(data)
        response = "Received"
        socket.send(response.encode())

    socket.close()


# function to start server socket
def server_socket_creation(sensor_host, sensor_port):
    # socket working
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binding socket
    try:
        serversocket.bind((sensor_host, sensor_port))
    except:
        print("Error in binding server socket")
        exit()

    # listen
    serversocket.listen(5)
    print("Server Listening...")
    while True:
        # accept
        (sensorsocket, address) = serversocket.accept()
        print("Connected sensor details: ", address)

        # opening thread for multiple clients interaction
        try:
            t = threading.Thread(target=sensors_interaction, args=(sensorsocket, address,))
            t.start()
        except:
            print("error in sensor server thread")

    serversocket.close()


def client_socket_creation(intmd_server_host, intmd_server_port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connection
    try:
        clientsocket.connect((intmd_server_host, intmd_server_port))
    except:
        print("error in connecting to server !")

    msg = "Hello from sensor server !"
    clientsocket.send(msg.encode())

    global data_list, index
    while True:
        time.sleep(1)
        # poll_msg = "want data?"
        # clientsocket.send(poll_msg.encode())
        # reply = clientsocket.recv(buffer_size).decode()
        # print(reply)
        # if reply == "1":
        while data_list[-1] == "":
            # time.sleep(2)
            continue

        # data = str(data_list[index:])[1:-1]
        data = str(data_list[-1])
        print(data)
        # index = len(data_list)
        clientsocket.send(data.encode())
        response = clientsocket.recv(buffer_size).decode()
        # print(response)

    clientsocket.close()


# functions
if __name__ == "__main__":
    # command line argument 'host:port'
    arg_list = sys.argv
    # print(arg_list)

    intmd_server_host = "127.0.0.1"
    intmd_server_port = 7000
    sensor_host = "127.0.0.1"
    sensor_port = 9000

    if len(arg_list) > 1:
        intmd_server_host_port_list = arg_list[1].split(":")
        intmd_server_host = intmd_server_host_port_list[0]
        intmd_server_port = int(intmd_server_host_port_list[1])

    if len(arg_list) > 2:
        sensor_server_host_port_list = arg_list[2].split(":")
        sensor_host = sensor_server_host_port_list[0]
        sensor_port = int(sensor_server_host_port_list[1])
    # print(host,port)

    # thread for creating client socket
    t1 = threading.Thread(target=client_socket_creation, args=(intmd_server_host, intmd_server_port,))
    # thread for creating server socket
    t2 = threading.Thread(target=server_socket_creation, args=(sensor_host, sensor_port,))

    t1.start()
    t2.start()