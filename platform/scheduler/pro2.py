from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm

# msg={"msg":"msg from app mgr"}

msg = {'schedule':
       {'start_time': '01:32',
        'end_time': '01:38',
        'request_type': 'cron',
        'priority': 'high',
        'days': 'monday',
        'interval': 'None',
        'duration': '30'
        },
       'userID': 'usr1',
       'appID': 'App',
       'algoID': 'Algo1',
       'form': 'run',
       'location': 'hyderabad',
       'devID': 'pawan',
       'sensorList': ["temp_0", "ac_0"],
       'RAM': '20',
       'CPU': '20'}

cm.send_message("AS", msg)

# cm.send_message_normal("AS",msg)


# producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

# def send_message(topic,msg):
# 		producer.send(topic, msg.encode('utf-8'))
# 		producer.flush()
# 		producer.close()

# msg="kafka"

# send_message('AS',msg)
