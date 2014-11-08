#!/usr/bin/env python
import pika
import json

from _logging import log, publisher_file


def push_to_queue(queue, payload):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    payload = json.dumps(payload)
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=payload,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    log(payload, type="Sent", file=publisher_file)
    connection.close()
