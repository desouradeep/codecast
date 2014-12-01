#!/usr/bin/python
from gevent import monkey
monkey.patch_all()

import gevent
import pika
import utils
import json

from _logging import consumer_file, log, create_log_dir
from publisher import push_to_queue

from flask import Flask, render_template, request, url_for
from flask.ext.socketio import SocketIO, emit, join_room, leave_room


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

all_nicks = []


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
    print "Connection to rabbitmq established"
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue='code-stream', durable=True)
    print "queue: %s" % ('code-stream')
    channel.basic_consume(callback, queue='code-stream')
    channel.start_consuming()


def callback(ch, method, properties, payload):
    '''
    callback() is called during message consumption.
    Function:
        Emits the data to the 'data' channel, logs the data and acknowledges
        the delivery.
    '''
    data, broadcast, nick = utils.validate_consumer_payload(payload)

    if data is not None:
        socketio.emit('output-code-stream', payload)

    log(payload, type="Recieved", file=consumer_file)
    ch.basic_ack(delivery_tag=method.delivery_tag)


###################################
########### Flask views ###########
###################################

@app.route('/nick', methods=('GET', 'POST'))
def nick():
    return render_template('login.html')


@app.route('/', methods=('GET', 'POST'))
def index():
    nick = utils.get_value_from_key('nick', request.form)

    if not nick:
        return render_template('login.html')

    if nick not in all_nicks:
        all_nicks.append(str(nick))
        socketio.emit("new-nick", nick)
    print "All nicks: ", all_nicks

    views = {
        1: url_for('left_pane'),
        2: url_for('right_pane'),
    }
    pagelets, ids = utils.pagelet_dict_generator(views)

    return_dict = {
        'pagelets': pagelets,
        'ids': ids,
        'nick': nick,
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
    payload = {
        'all_nicks': all_nicks,
    }

    return render_template('right_pane.html', **payload)


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
@socketio.on('logout')
def logout(nick):
    all_nicks.remove(nick)
    emit('nick-remove', str(nick), broadcast=True)


# Connection to a client lost
@socketio.on('input-code-stream')
def input_code_stream(payload):
    data = {
        'nick': str(payload['nick']),
        'data': str(payload['data']),
        'broadcast': True,
    }

    push_to_queue('code-stream', data)


def make_ready():
    '''
    Prepares external components to work with the server
    '''
    try:
        # spawn rabbitmq consumer gevent greenlet
        gevent.spawn(consumer)
        # create log dir if not present
        create_log_dir()
        return "Fire!"
    except Exception, e:
        print e

if __name__ == '__main__':
    ready_to_fire = make_ready()

    if ready_to_fire == "Fire!":
        app.debug = True
        socketio.run(app, host='0.0.0.0')
