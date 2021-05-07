#!/usr/bin/env python3

import bind_data
from kafka import KafkaConsumer, KafkaProducer
import threading
import json
import time
import sys
from simulators import *
import csv

# TODO: Uncomment next line
sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm


SENSOR_TYPES = {'TEMP': -1,'BIOMETRIC': -1, 'GPS': -1, 'LIGHT': -1}

sensor_objects = {}


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
    sensor_type = sensor_info['type']
    print("Type")
    if sensor_type == 'TEMP':
        topic = sensor_info['topic']
        obj = TempSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    elif sensor_type == 'LIGHT':
        topic = sensor_info['topic']
        obj = LuxSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    elif sensor_type == 'BIOMETRIC':
        topic = sensor_info['topic']
        obj = BiometricSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    elif sensor_type == 'GPS':
        topic = sensor_info['topic']
        obj = GPSSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    else:
        print("ERROR: Invalid Sensor Type")
        return

    # elif sensor_type == 'AC':
    #     ac_up(sensor_info)

    t = threading.Thread(target=bind_data.simulate, kwargs={"sensor_obj": obj})
    t.start()


def get_data(topic):
    # sensor_topic = msg['msg']
    print(topic)
    # with open("sensor_registry.txt", 'r') as f:
    #     instances = f.readlines()

    # for instance in instances:
    #     sinfo, nwinfo, topic = instance.split(':')

    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id=None, auto_offset_reset='earliest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for message in consumer:
        data = message.value
        break

    print("******",data,"******")
    return data['data']
    # producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # producer.send('SM_to_Deployer_data', data)
    # producer.flush()
    # producer.close()


def run_sensors():
    registry = open('sensor_registry.txt', 'r')

    running = open('running_sensors.txt', 'a', newline='')
    fieldnames = ['loc', 'desc', 'type', 'topic', 'ip', 'port']
    writer1 = csv.DictWriter(running, fieldnames=fieldnames)
    writer1.writeheader()
    running.close()

    global SENSOR_TYPES
    while True:

        sensors = registry.readlines()

        if len(sensors) > 0:
            for sensor in sensors:
                sensor = sensor.strip('\n')
                stype, locinfo, nwinfo = sensor.split(':')
                desc, loc = locinfo.split('_')
                ip, port = nwinfo.split('_')
                SENSOR_TYPES[stype] += 1
                topic = stype + "_" + str(SENSOR_TYPES[stype])

                sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic, 'desc': desc, 'loc':loc}
                bind_sensor(sensor_info)
                print(sensor_info)
                with open('running_sensors.txt', 'a', newline='') as f:
                    # line = sinfo + ":" + nwinfo + ":" + topic
                    # print(line)
                    # f.write(line + '\n')
                    writer2 = csv.DictWriter(f, fieldnames=fieldnames)
                    writer2.writerow(sensor_info)

        time.sleep(20)

        # Testing controller functioning
        # print("Turning off AC.......")
        # msg = {"type": 'temp_0', "value": 0}
        # controller(msg)

    registry.close()
    # running.close()


def set_data(msg):

    topic = msg['topic']
    status = msg['value']
    # msg = {"status": status}
    # bind_data.dummy_ac(status)
    # cm.send_message(topic, msg)
    obj = sensor_objects[topic]
    obj.controller = status


def start():
    #   Create a kafka topic to start sensor manager services
    t1 = threading.Thread(target=run_sensors)
    t1.start()

    # t2 = threading.Thread(target=dummy1, kwargs={'topicid': 'Deployer_to_SM_data', 'handler': get_data})
    # t2.start()
    #
    # t3 = threading.Thread(target=dummy1, kwargs={'topicid': 'Deployer_to_SM_get', 'handler': controller})
    # t3.start()
    # t2 = threading.Thread(target=dummy2, kwargs={'topicId': 'Sensor_Manager_to_Deployer', 'handler':get_sensor_id})
    # t2.start()
