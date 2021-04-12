import random
import time
import comm_module as cm
from kafka import KafkaConsumer
import json


DATA = None
ac = -1


def dummy_ac(value):
    global ac
    ac = value


def temp_up(sensor_info):
    global ac
    temp = 18
    IncrementFactor = 0.1
    DecrementFactor = 0.2
    # controller_topic = sensor_info['controller_id']
    controller_topic = 'acc1_0'
    while True:

        # consumer = KafkaConsumer(controller_topic, bootstrap_servers='localhost:9092', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        # for message in consumer:
        #     data = message.value
        #     break
        print("AC",ac)
        if ac == -1:
            temp += IncrementFactor
            print(round(temp, 2))
            #print("****Temp:", round(temp, 2))
            msg = {'data': round(temp, 2)}
            cm.send_message(sensor_info['topic'], msg)
            time.sleep(4)
        else:
            temp -= DecrementFactor
            print(round(temp, 2))
            #print("****Temp:", temp)
            msg = {'data': round(temp, 2)}
            cm.send_message(sensor_info['topic'], msg)
            time.sleep(4)

    # ac = 1
    # print("SWITCHING ON AC")
    # while (temp > 15):
    #     temp -= DecrementFactor
    #     print(round(temp, 2))
    #     time.sleep(1)
    # ac = 0
    # print("Switching off AC")


def ac_up(sensor_info):
    msg = {'status': -1}
    cm.send_message(sensor_info['topic'], msg)


def simulate(sensor_info):

    sensor_type = sensor_info['type']

    if sensor_type == 'temp':
        temp_up(sensor_info)

    elif sensor_info == 'AC':
        ac_up(sensor_info)

    # global DATA
    # producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    # while True:
    #     DATA = random.randint(0, 10)
    #     msg = {'data': DATA}
    #     print("***DATA***", DATA)
    #     # TODO: Kafka producer.send_message(DATA, sensor_info['topic'])
    #     print("Topic",sensor_info['topic'])
    #     # producer.send(sensor_info['topic'], msg)
    #     cm.send_message(sensor_info['topic'], msg)
    #     print("Data sent to kafka topic")
    #     time.sleep(10)
