CodeCast
========

An app which allows multiple people to hack on problems, collaboratively, in realtime.
The app will also support inbuilt analytics to ensure efficiency of the code.

Started as a final year project.

Dependencies:
-------------

Pythonic dependencies:
^^^^^^^^^^^^^^^^^^^^^^

    1. gevent-socketio
    2. flask
    3. flask-socketio
    4. pika
    5. ipdb (for debugging purposes)

Installation:

Install python-dev libxml2-dev libxslt-dev::
    
    $ sudo yum install python-dev libxml2-dev libxslt-dev


Create a virtual environment, ``codecast``, and install the dependencies::

    $ sudo pip install virtualenvwrapper
    $ export WORKON_HOME=~/Envs
    $ mkdir -p $WORKON_HOME
    $ source /usr/bin/virtualenvwrapper.sh
    $ mkvirtualenv codecast

Run in the project directory::

    $ pip install -r requirements.txt


Non-pythonic dependencies:
^^^^^^^^^^^^^^^^^^^^^^^^^^

    1. rabbitmq-server

Installation::
    
    $ sudo yum install rabbitmq-server


Run the app:
------------

1. Start the rabbitmq server with root priveleges::
  
    $ sudo rabbitmq-server

2. In a new terminal, switch to codecast virtualenv::

    $ workon codecast

4. Start the flask server::

    $ python server.py

5. Now, open a browser, and point to ``localhost:5000``, to fire up a client.


Optional
--------

1. Enable the RabbitMQ management plugin::

      $ sudo rabbitmq-plugins enable rabbitmq_management

   Browse to ``localhost:15672`` to have a look at the RabbitMQ dashboard.

2. Tail the log files (log directory: ``src/logs/``)::

    $ tail -f consumer.log
    $ tail -f publisher.log

