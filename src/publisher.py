#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ''

try:
    while message != 'exit':
        message = raw_input(">>> ")
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
except:
    connection.close()
