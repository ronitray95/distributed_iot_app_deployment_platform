import time
import comm_module as cm
from kafka import KafkaConsumer
import json 

class comm(object):
    def __init__(self):
        pass

    def handler_function(self, msg):
        #print(msg)
        data = msg["data"]
        return data

    def getData(self, id):
        
        data = {"msg":id}
        cm.send_message("Deployer_to_SM_data",data)
        #x = cm.consume_msg_once('SM_to_Deployer_data',self.handler_function)
        consumer = KafkaConsumer('SM_to_Deployer_data',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        #print(x)
        for msg in consumer:
            return msg.value["data"]

    def setData(self, typ, value):
        #print(typ,value)
        data = {"type":typ, "value":value}
        cm.send_message("Deployer_to_SM_get",data)

    def sendNotification(self, msg):
        pass

obj = comm()