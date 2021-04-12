
from kafka import KafkaConsumer, KafkaProducer
import json
import threading


def send_message(topic,mess):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic, mess)
    producer.flush()
    producer.close()


def consume_msg(topic,handler_fun):

    consumer = KafkaConsumer(topic,bootstrap_servers='localhost:9092',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:
        th = threading.Thread(target=handler_fun,args=(mess.value,))
        th.start()
