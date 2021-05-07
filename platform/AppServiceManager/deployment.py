import _thread
import requests
import json
from kafka import KafkaConsumer
import ServerLifeCycleManager as sl
import threading
import os
import sys 
import pandas as pd

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm

jobID = {}

def createList(idby, types):

    if idby[0] == 'location':
        index = 0
    else:
        index = 1
    df = pd.read_csv('../SensorManager/running_sensors.txt', delimiter = ",", header=None)
    sensorList = {}
    for i in types:
        sensorList[i] = list(df[(df[index] == idby[1]) & (df[2] == i)][3])

    return sensorList


def createConfig(conf, path):
    with open(path+'/conf.json', 'w') as f:
        data = {}
        """for i in sensorList:
            i = i.split('_')
            data[i[0]] = i[1]"""
        f.write(json.dumps(conf))


def appExe(action, jID, algoID, appID, userID, devID, RAM, CPU, path):
    global jobID
    ip, port = sl.running_runtime()
    if action == 'start':
        #ip ="127.0.0.1"
        #port = "5010"
        print("IP/port assign to job {} is {}/{}".format(jID, ip, port))
        jobID[jID] = [ip, port]
        status = requests.get("http://"+ip+':'+port+'/runapp', params={'app_id': appID, 'user_id': userID, 'ram_req': RAM,
                                                                       'cpu_req': CPU, 'algo_path': path+"/"+devID+"/"+appID, 'app_path': path+"/"+devID+"/"+appID+"/"+algoID+"/"+algoID+".py"})
        if status:
            print("Application:{} Started".format(appID))

    else:
        status = requests.get("http://"+jobID[jID][0]+':'+jobID[jID]
                              [1]+'/stopapp', params={'app_id': appID, 'user_id': userID})
        if status:
            del jobID[jID]
            print("Application:{} terminated".format(appID))


def handler_fun(message):

    action = message["action"]  # start/stop
    jID = message["jID"]
    appID = message["appID"]
    algoID = message["algoID"]
    types = message['types'] #[type1,type2...]
    idby = message["idby"] #value: [loc/placeholder, name]
    #sensorList = message["sensorList"]  # ["temp_t123","ac_a123"]
    userID = message["userID"]
    devID = message["devID"]
    RAM = message["RAM"]
    CPU = message["CPU"]
    path = '../Applications'

    sensorList = createList(idby, types)

    conf = {'sensors':sensorList,'userid':userID,'outputfile':userID+'_'+appID+'_'+algoID}
    createConfig(conf, path + "/"+devID+"/"+appID+"/"+algoID)
    appExe(action, jID, algoID, appID, userID, devID, RAM, CPU, path)


def schedular_service():
    consumer = KafkaConsumer('DP', bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:
        _thread.start_new_thread(handler_fun,(mess,))


def run_triggeredApp(path, jID):
    global jobID
    ip, port = sl.running_runtime()
    print("IP/port assign to job {} is {}/{}".format(jID, ip, port))
    jobID[jID] = [ip, port]
        
    status = requests.get("http://"+ip+':'+port+'/trigger', params={'app_path': path})
    if status:
        appName = path.split('/')[-1]
        print(f'Application:{appName} Started')


def trigger_service():
    jID = 1
    consumer = KafkaConsumer('trig', bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:
        run_triggeredApp(mess['path'], jID)   
        jID += 1

def main():

        _thread.start_new_thread(schedular_service,())
        _thread.start_new_thread(trigger_service,())

main()
