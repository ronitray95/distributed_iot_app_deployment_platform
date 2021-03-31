import socket
import random
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(),4003))
sen_id = 123
msg = "ab;"
s.send(msg.encode())
while True:    
    data = str(random.randint(0,10))
    s.send(str(data).encode())
    print(data)

s.close()