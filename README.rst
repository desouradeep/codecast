CodeCast
========

An app which allows multiple people to hack on problems, collaboratively, in realtime.
The app will also support inbuilt analytics to ensure efficiency of the code.

Started as a final year project.

Dependencies:
-------------

Pythonic dependencies:

        1. gevent-socketio
        2. flask
        3. flask-socketio
        4. pika

Non-pythonic dependencies:

        1. rabbitmq-server


Run the app:
------------

1. Start the rabbitmq server with root priveledges::
        $ sudo rabbitmq-server

2. In a new tab, start the rabbitmq publisher::
        $ python publisher.py

3. In another tab, start the flask server::
        $ python server.py

4. Now, open a browser, and point to "localhost:5000", to fire up a client.

