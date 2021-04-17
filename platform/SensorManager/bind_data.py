import random
import time
import comm_module as cm
from kafka import KafkaConsumer
import json
from simulators import *


ac = -1


def dummy_ac(value):
    global ac
    ac = value


def ac_up(sensor_info):
    # msg = {'status': -1}
    # cm.send_message(sensor_info['topic'], msg)
    print("Started AC controller")


def simulate(sensor_info):   # sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic}

    sensor_type = sensor_info['type']
    if sensor_type == 'temp':
        temp_sensor = TempSensor(sensor_info['topic'], ip=sensor_info['ip'], port=sensor_info['port'])
        while True:
            # consumer = KafkaConsumer(controller_topic, bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
            # for message in consumer:
            #     data = message.value
            #     break
            if ac == -1:
                temp_sensor.temp_up()
            else:
                temp_sensor.temp_down()

            output = temp_sensor.temp
            print("****Temp:", output)
            # msg = {'data': output}
            # cm.send_message(sensor_info['topic'], msg)
            time.sleep(4)

    elif sensor_type == 'AC':
        ac_up(sensor_info)

