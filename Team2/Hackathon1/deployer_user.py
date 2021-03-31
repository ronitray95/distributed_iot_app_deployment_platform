import sys   
import socket
import threading
import os

host="127.0.0.1"
port=7004

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    
    print("Choose the category")
    print("1. Application Deployer\n2. End user")

    cat = input()
    
    print("1. Signup\n2. Login")
    stat = input()
    
    print("Enter user id: ")
    uid = input()

    print("Enter password: ")
    pswd = input()

    tosend = cat+';'+stat+';'+uid+';'+pswd

    s.sendall(tosend.encode())

    while True:
        data = s.recv(1024)

        data = data.decode()
        mylst = data.split(';')
        if(mylst[1]=='1'):
            print(mylst[0])
            if cat=='1':
                print('Enter zip file name:')

                zip_file=input()
                f=open(zip_file,'rb')
                content=f.read()
                s.sendall(content)
            else:
                print("Enter the usecase")
                data = s.recv(1024).decode()
                print(data)
                usecase = input()
                s.sendall(usecase.decode())
                data = ""
                while True:
                    data += s.recv(1024).decode()
                print(data)

        else:
            print(mylst[0])
            print("1. Signup\n2. Login")
            stat = input()

            print("Enter user id: ")
            uid = input()

            print("Enter password: ")
            pswd = input()

            tosend = cat+';'+stat+';'+uid+';'+pswd

            s.sendall(tosend.encode())

