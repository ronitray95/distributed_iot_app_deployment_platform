#!/usr/bin/env python3

import bind_data
from kafka import KafkaConsumer, KafkaProducer
import threading
import json
import time
import sys
from flask import *
from _thread import *

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm


SENSOR_TYPES = {'temp': -1,'AC': -1}

app = Flask(__name__)

def dummy1(topicid, handler):
    cm.consume_msg(topicid, handler)


def get_sensor_id(msg):
    # Todo: kafka consumer to sensor topic
    # msg = {sensor_type = 'temp', loc = 'l1', count = 5}
    pass


'''
Binds the sensor data to a topic
:param sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic} 

'''


def bind_sensor(sensor_info):
    t = threading.Thread(target=bind_data.simulate, kwargs={'sensor_info': sensor_info})
    t.start()


def get_data(msg):
    sensor_topic = msg['msg']
    print(sensor_topic)
    # with open("sensor_registry.txt", 'r') as f:
    #     instances = f.readlines()

    # for instance in instances:
    #     sinfo, nwinfo, topic = instance.split(':')

    consumer = KafkaConsumer(sensor_topic, bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for message in consumer:
        data = message.value
        print("***************************************************",data)
        break

    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('SM_to_Deployer_data', data)
    producer.flush()
    producer.close()


def run_sensors():
    registry = open('sensor_registry.txt', 'r')
    global SENSOR_TYPES
    while True:

        sensors = registry.readlines()

        if len(sensors) > 0:
            for sensor in sensors:
                sensor = sensor.strip('\n')
                sinfo, nwinfo = sensor.split(':')
                stype = sinfo.split('_')[0]
                ip, port = nwinfo.split('_')
                SENSOR_TYPES[stype] += 1
                topic = stype + "_" + str(SENSOR_TYPES[stype])

                sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic}
                bind_sensor(sensor_info)

                with open('running_sensors.txt', 'a') as f:
                    line = sinfo + ":" + nwinfo + ":" + topic
                    print(line)
                    f.write(line + '\n')

        time.sleep(10)

        # Testing controller functioning
        # print("Turning off AC.......")
        # msg = {"type": "ac", "value": 0}
        # controller(msg)

    registry.close()


def controller(msg):

    topic = msg['type']
    status = msg['value']
    msg = {"status": status}
    bind_data.dummy_ac(status)
    # cm.send_message(topic, msg)


def start():
    #   Create a kafka topic to start sensor manager services
    t1 = threading.Thread(target=run_sensors)
    t1.start()

    t2 = threading.Thread(target=dummy1, kwargs={'topicid': 'Deployer_to_SM_data', 'handler': get_data})
    t2.start()

    t3 = threading.Thread(target=dummy1, kwargs={'topicid': 'Deployer_to_SM_get', 'handler': controller})
    t3.start()
    # t2 = threading.Thread(target=dummy2, kwargs={'topicId': 'Sensor_Manager_to_Deployer', 'handler':get_sensor_id})
    # t2.start()

def simulateSensors():
    for x in server_list:
        #app = Flask(__name__)
        # print(json.dumps(x))
        print(x['ip'], x['port'])
        server_load[x['id']] = (
            Server(x['id'], x['ip'], x['port'], x['active'], x['health'], x['applications'], x['username'], x['password']))
        last_port = x['port']
        producer.send(KAFKA_TOPIC_SERVER_LIST, json.dumps(x))

        start_new_thread(app.run, (x['ip'], x['port']))