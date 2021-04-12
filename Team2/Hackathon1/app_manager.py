import socket
import json
import select
import sys
import threading
from zipfile import ZipFile 



host = "127.0.0.1"
port = 7004
mysensortypes = ["Temperature", "Ultrasonic"]
outputtype = ["File","Terminal"]
myalgos = {}
myobjlst = []

dvlprid = {}
userid = {}

dep_count=0

configData={}

algodict = {}

def createsensorinstance(conn,sen_type,sen_instance):

    # for types in sen_type:
    #     for ids in sen_instance[types]:
    #         obj1 = sensorfile.{}.format(types)
    import sensorfile
    obj1 = sensorfile.Temperature('Temperature','a')
    myobjlst.append(obj1)

def validate(conn, content):

    for type in content["sensorTyes"] :
        if type not in mysensortypes :
            conn.sendall("Undefined sensor types;0")
            return 0
    
    for otype in content["outputFormat"]:
        if otype not in outputtype:
            conn.sendall("Undefined output type;0")
            return 0
    
    myalgos["applicationName"] = content["algorithm"]
    return 1
    


def getData(conn):
    global dep_count
    global configData

    f1=open('config.json','r')
    content=json.load(f1)

    # configData=content
    value = validate(conn, content)
    if value == True :
        sen_dict = {}
        for idx,types in enumerate(content["sensorTypes"]):
            sen_dict[types] = content["sensorInstances"][idx]
        createsensorinstance(conn,content["sensorTypes"], sen_dict)
    # print(configData)
    # print(type(configData))


def addFile(conn):
    global dep_count
    content=b''
    while True:
        data=conn.recv(1024)
        content+=data
        if len(data)<1024:
            break
    
    f=open('al'+str(dep_count)+'.zip','wb')
    f.write(content)
    f.close()
    file_name = 'al'+str(dep_count)+'.zip'
    print(file_name)
    file_name='al0.zip'
  
    with ZipFile(file_name, 'r') as zip: 
    
        zip.printdir() 
    
        print('Extracting all the files now...') 
        zip.extractall() 
        print('Done!') 

    getData(conn)



def generateoutput(conn, myalgo):
    
    conn.sendall(myobjlst[0].readsensordata())



def handleuser(conn):
    conn.sendall(str(myalgos.keys()).encode())
    data = conn.recv(1024).decode
    generateoutput(conn, [myalgosdata])



def login(id, passw, prsn,conn):

    if prsn == '1':
        if id not in dvlprid:
            conn.sendall("Developer does not exist.;0".encode())
        else:
            if dvlprid[id] == passw:
                conn.sendall("Succesfully logged in.;1".encode())
                addFile(conn)

        # Upload file
            else:
                conn.sendall("Incorrect Password.;0".encode())
    else:
        if id not in userid:
            conn.sendall("Developer does not exist.;0".encode())
        else:
            if userid[id] == passw:
                conn.sendall("Succesfully logged in.;1".encode())
                handleuser(conn)
            else:
                conn.sendall("Incorrect Password.;0".encode())

    

def signup(id, passw, prsn,conn):
    if prsn == '1' :
        if id not in dvlprid :
            dvlprid[id]=passw
            conn.sendall("Successfullly registered.;1".encode())
            addFile(conn)
        else:
            conn.sendall("id exist;0".encode())
    else :
        if id not in userid :
            dvlprid[id]=passw
            conn.sendall("Successfullly registered.;1".encode())
        else:
            conn.sendall("id exist;0".encode())




def new_client(conn, addr):
    while True:
        data = conn.recv(1024)
        if data:
            data = data.decode()
            mylst = data.split(';')

            if mylst[1]=='2':
                login(mylst[2],mylst[3],mylst[0],conn)
            else:
                signup(mylst[2],mylst[3],mylst[0],conn)
        else:
            continue


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    s.listen()
    while True:

        conn, addr = s.accept()
        #conn_clients.append(conn)

        # print(conn)
        print('Connected to ', addr)

        t1 = threading.Thread(target=new_client, args=(conn, addr))

        t1.start()
