import socket
import os
import threading
data = ""
host="127.0.0.1"
port=7004

class Temperature:

    def __init__(self,sen_type,sen_id ):
        self.sen_id = sen_id
        self.sen_type = sen_type
        self.f1 = open(str(sen_type),'w')
        

    def getsensordata(self,conn,addr):
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as st:
                st.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                st.bind((host,int(7010)))
                st.listen()
            
            while True:
                connt, addr = st.accept()
                while True:
                    data = connt.recv()
                    self.f1.write(data.decode())
                    if os.stat(str(self.sen_type)).st_size > 1024 :
                        self.f1.truncate(0)

    def readsensordata(self):
        return self.f1.readlines()



obj1 = Temperature(2,3)
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((host,port))
    while True:
        conn, addr = s.accept()
        #conn_clients.append(conn)

        # print(conn)
        print('Connected to ', addr)

        t1 = threading.Thread(target=obj1.getsensordata, args=(conn, addr))

        t1.start()

#     def getdata(self, ):
        
        
#         while(True):
#             data = s.recv(1024)
#             self.conn.sedall(data)

#     def savesensordata(conn, senfile, addr):

#         conn.send(senfile.readlines())
#         senfile.truncate(0)


#     def getsensordata(cur_sen_id):

#         senfile = open('sen_'+str(cur_sen_id),'r')
        
#         # t1 = threading.Thread(target=savesensordata, args=(conn, senfile, addr))

#         # t1.start()


# class Ultrasonic:

#     def __init__(self,conn, sen_id ):
#         self.conn = conn
#         self.sen_id = sen_id

#     def getdata(self, ):
        
#         while(True):
#             data = s.recv(1024)
#             self.conn.sedall(data)

#     def savesensordata(self, conn, senfile, addr):

#         conn.send(senfile.readlines())
#         senfile.truncate(0)


#     def getsensordata(self, conn, cur_sen_id):

#         senfile = open('sen_'+str(cur_sen_id),'r')
        
#         # t1 = threading.Thread(target=savesensordata, args=(conn, senfile, addr))

#         # t1.start()


            
