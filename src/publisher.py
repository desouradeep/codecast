#!/usr/bin/env python
import pika
import json


def push_to_queue(queue, payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(payload),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )

    connection.close()
