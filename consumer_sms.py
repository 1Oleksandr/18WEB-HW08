import time
import json

import connect
from mongoengine import *
import pika

from model_contact import Contacts

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='phone_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    time.sleep(1)
    contact = Contacts.objects(id=message['ObjectId']).first()
    contact.update(done=True)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='phone_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()
