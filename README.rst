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

Installation:

Create a virtual environment, ``codecast``, and install the dependencies::

    $ sudo pip install virtualenvwrapper
    $ mkvirtualenv codecast
    $ pip install -r requirements.txt


Non-pythonic dependencies:
^^^^^^^^^^^^^^^^^^^^^^^^^^

    1. rabbitmq-server

Installation::
    
    $ sudo yum install rabbitmq-server


Run the app:
------------

1. Switch to codecast virtualenv::

    $ workon codecast

2. Start the rabbitmq server with root priveleges::
  
    $ sudo rabbitmq-server

3. In a new tab, start the rabbitmq publisher:: 

    $ python publisher.py

4. In another tab, start the flask server::

    $ python server.py

5. Now, open a browser, and point to ``localhost:5000``, to fire up a client.

