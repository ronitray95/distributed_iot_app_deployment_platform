import time
#import comm_module as cm
import requests
from kafka import KafkaProducer
import json
import pymongo as pm
from pymongo import *

 
class comm(object): 
    def __init__(self):
        pass

    def getData(self, id):
        #print(id)
        data = requests.post('http://localhost:5050/get-data', json={"sensor":id})
        return json.loads(data.content.decode('utf-8'))

    def setData(self, id, value):
        ack = requests.post('http://localhost:5050/set-data', json={"controller":{id:value}})
        #print(ack)
        return json.loads(ack.content.decode('utf-8'))

    def getEmailID(self, userID):
        client = MongoClient("mongodb+srv://admin:admin123@cluster0.ze4na.mongodb.net")
        db = client['IOT']
        userTable = db['user_details']
        x = userTable.find_one({"_id": userID})
        return x['email']

    def sendMail(self, emailID, msg):
        pass
        #add code for sending mail on 'emailID'


    def trigger(self, path, conf):
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        mess = {"path":path}
        producer.send("trig", mess)

obj = comm()
