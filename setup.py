from setuptools import setup

setup(
    name='CodeCast',
    version='1.0',
    description='Team collaboration in realtime',
    author='desouradeep',
    author_email='souradeep.2011@gmail.com',
    install_requires=[
        'gevent-socketio',
        'flask',
        'flask-socketio',
        'pika',
        'ipdb',
        'gevent-websocket',
    ],
)
