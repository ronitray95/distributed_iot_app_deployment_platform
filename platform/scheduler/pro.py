from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm


# msg={"msg":"msg from app mgr"}

msg = {
    "action": "start",
    "jID": "j12",
    "appID": "App",
    "algoID": "Algo1",
    "sensorList": ["temp_0", "ac_0"],
    "userID": "usr1",
    "devID": "pawan",
    "RAM": "20",
    "CPU": "12"
}
cm.send_message("DP", msg)

# cm.send_message_normal("AS",msg)


# producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

# def send_message(topic,msg):
# 		producer.send(topic, msg.encode('utf-8'))
# 		producer.flush()
# 		producer.close()

# msg="kafka"

# send_message('AS',msg)
