#!/usr/bin/python
from gevent import monkey
monkey.patch_all()

import gevent
import ipdb
import pika
from log import consumer_file, log
from utils import pagelet_dict_generator, validate_consumer_payload
from publisher import push_to_queue

from flask import Flask, render_template, request, url_for
from flask.ext.socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None


###################################
##### RabbitMQ specific codes #####
###################################
# This has to done here because we are
# mostly emitting using the socketio object

def consumer():
    '''
    RabbitMQ consumer.
    This is spawned in a greenlet using gevent.spawn in __init__
    '''
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='code-stream', durable=True)
    channel.basic_consume(callback, queue='code-stream')
    channel.start_consuming()


def callback(ch, method, properties, payload):
    '''
    callback() is called during message consumption.
    Function:
        Emits the data to the 'data' channel, logs the data and acknowledges
        the delivery.
    '''
    data, broadcast = validate_consumer_payload(payload)
    if data is not None:
        socketio.emit('output-code-stream', data)

    log(payload, file=consumer_file)
    ch.basic_ack(delivery_tag=method.delivery_tag)


###################################
########### Flask views ###########
###################################

@app.route('/')
def index():
    views = {
        1: url_for('left_pane'),
        2: url_for('right_pane'),
    }
    pagelets, ids = pagelet_dict_generator(views)

    return_dict = {
        'pagelets': pagelets,
        'ids': ids,
    }

    return render_template('index.html', **return_dict)


###################################
####### Flask pagelet views #######
###################################

@app.route('/left-pane')
def left_pane():
    return render_template('left_pane.html')


@app.route('/right-pane')
def right_pane():
    return render_template('right_pane.html')


###################################
#### Socket io specific codes #####
###################################

# Connection established with a new client
@socketio.on('connect')
def connect():
    print 'Client connected'


# Connection to a client lost
@socketio.on('disconnect')
def disconnect():
    print 'Client disconnected'


# Connection to a client lost
@socketio.on('input-code-stream')
def input_code_stream(data):
    payload = {
        'data': data,
        'broadcast': True,
    }

    push_to_queue('code-stream', payload)


if __name__ == '__main__':
    app.debug = True
    # spawn rabbitmq consumer gevent greenlet
    gevent.spawn(consumer)
    socketio.run(app, host='0.0.0.0')
