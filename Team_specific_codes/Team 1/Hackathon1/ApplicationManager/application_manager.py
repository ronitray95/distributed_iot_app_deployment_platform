import socket, os, sys, _thread, threading, time
from _thread import *
from AlgoRepo import Algorithm1

# global
# port = 8001
# host = "localhost"


buffer_size = 4096
thread_count = 0
sensor_data_flag = 1
data = ""

# functions
def client_interact(socket, address):
    while (1):
        global sensor_data_flag, data
        msg = socket.recv(buffer_size).decode()
        # print("Client says: ", msg)

        if msg == "get data":
            sensor_data_flag = 1
            while data == "":
                continue
            # data_list = data.split(" ")
            # socket.send(data_list[1].encode())
            socket.send(data.encode())
            print("data", data, "sent to client")
            data = ""
            sensor_data_flag = 0

        else:
            response = "command Received by server"
            socket.send(response.encode())

    socket.close()


# function to start server socket
def rpc_server_socket_creation(s1_host, s1_port):
    # socket working
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binding socket
    try:
        serversocket.bind((s1_host, s1_port))
    except:
        print("Error in binding server socket")
        exit()

    # listen
    serversocket.listen(5)
    print("Server Listening...")
    while True:
        # accept
        (clientsocket, address) = serversocket.accept()
        # print("Connected Client details: ", address)

        # opening thread for multiple clients interaction
        try:
            t1 = threading.Thread(target=client_interact, args=(clientsocket, address,))
            t1.start()
        except:
            print("error in thread")

    serversocket.close()


# function to start server socket
def sensor_server_socket_creation(s2_host, s2_port):
    # socket working
    sensor_serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binding socket
    try:
        sensor_serversocket.bind((s2_host, s2_port))
    except:
        print("Error in binding server socket")
        exit()

    # listen
    sensor_serversocket.listen(5)
    # print("Server Listening...")
    while True:
        global sensor_data_flag, data
        # accept
        (sensor_clientsocket, address) = sensor_serversocket.accept()
        # print("Connected sensor servor details: ", address)

        request = sensor_clientsocket.recv(buffer_size).decode()
        while True:
            # request = sensor_clientsocket.recv(buffer_size).decode()
            # if request == "want data?":
                # if sensor_data_flag == 0:
                #     sensor_clientsocket.send("0".encode())
                # elif sensor_data_flag == 1:
                # sensor_clientsocket.send("1".encode())
            response = sensor_clientsocket.recv(buffer_size).decode()
            data = response
            print("data received: ", data)
            sensor_clientsocket.send("Data Received by server".encode())
            status = Algorithm1.check_moisture(data)
            if status:
                # send_notif()
                print("Sending notification---> Need water!")

        sensor_clientsocket.close()

    sensor_serversocket.close()


if __name__ == "__main__":

    # command line argument 'host:port'
    arg_list = sys.argv
    # print(arg_list)

    # client server ip port
    s1_host = "127.0.0.1"
    s1_port = 8000
    # sensor server ip port
    s2_host = "127.0.0.1"
    s2_port = 7000
    if len(arg_list) > 1:
        s1_host_port = arg_list[1].split(":")
        s1_host = s1_host_port[0]
        s1_port = int(s1_host_port[1])

    if len(arg_list) > 2:
        s2_host_port = arg_list[2].split(":")
        s2_host = s2_host_port[0]
        s2_port = int(s2_host_port[1])

    # print(host,port)

    # creating server socket-1 for clients
    t1 = threading.Thread(target=rpc_server_socket_creation, args=(s1_host, s1_port,))

    # creating server socket-2 for sensor server
    t2 = threading.Thread(target=sensor_server_socket_creation, args=(s2_host, s2_port,))

    t1.start()
    t2.start()