import random
import time
import sys

# TODO: Uncomment next line
sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm
from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
from simulators import *


# ac = -1
#
#
# def dummy_ac(value):
#     global ac
#     ac = value
#
#
# def ac_up(sensor_info):
#     # msg = {'status': -1}
#     # cm.send_message(sensor_info['topic'], msg)
#     print("Started AC controller")


def simulate(sensor_obj):   # sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic}

    # sensor_type = sensor_obj.type

    # if sensor_type == 'temp':
        # temp_sensor = TempSensor(sensor_info['topic'], ip=sensor_info['ip'], port=sensor_info['port'])
    topic = sensor_obj.id
    while True:
        # consumer = KafkaConsumer(controller_topic, bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        # for message in consumer:
        #     data = message.value
        #     break
        data, controller = sensor_obj.genRandom()

        # output = sensor_obj.temp
        # controller = sensor_obj.controller
        print(f"{sensor_obj.id} ---> Data:", data)
        # print(f"{sensor_obj.id} ---> Controller:", controller)
        msg = {'data': data}

        # TODO: Uncomment next line
        #cm.send_message(topic, msg)
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(topic, msg)
        time.sleep(1)

    # elif sensor_type == 'AC':
    #     ac_up(sensor_info)

