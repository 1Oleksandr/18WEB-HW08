from datetime import datetime
from mongoengine import *
import connect
import json
import random
import pika
from faker import Faker

from model_contact import Contacts


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='send_info', exchange_type='direct')
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='phone_queue', durable=True)

channel.queue_bind(exchange='send_info', queue='email_queue')
channel.queue_bind(exchange='send_info', queue='phone_queue')


def main():
    # fake = Faker()
    # send_by = ("email", "phone")
    # for i in range(10):
    #     Contacts(email=fake.email(), name=fake.name(),
    #              phone=fake.phone_number(), send_type=random.choice(send_by)).save()

    contacts = Contacts.objects(done=False)
    for contact in contacts:
        message = {
            "ObjectId": f"{contact.id}",
            "date": datetime.now().isoformat(),
            "sent": f"{contact.send_type}"
        }

        if contact.send_type == 'email':

            channel.basic_publish(
                exchange='send_info',
                routing_key='email_queue',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent by email %r" % message)
        else:
            channel.basic_publish(
                exchange='send_info',
                routing_key='phone_queue',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ))
            print(" [x] Sent by SMS %r" % message)
        contact.update(done=True)
    connection.close()


if __name__ == '__main__':
    main()
