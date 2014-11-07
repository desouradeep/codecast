#!/usr/bin/python
from gevent import monkey
monkey.patch_all()

import gevent
import pika
from log import consumer_file, log
from utils import pagelet_generator

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
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_consume(callback, queue='task_queue')
    channel.start_consuming()


def callback(ch, method, properties, body):
    '''
    callback() is called during message consumption.
    Function:
        Emits the data to the 'data' channel, logs the data and acknowledges
        the delivery.
    '''
    socketio.emit('data', body)
    log(body, file=consumer_file)
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
    pagelets, ids = pagelet_generator(views)

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


if __name__ == '__main__':
    print 'Listening on http://localhost:5000'
    app.debug = True

    # spawn rabbitmq consumer gevent greenlet
    gevent.spawn(consumer)
    socketio.run(app)
