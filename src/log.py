import os
from datetime import datetime

# Declaring standard log file names
consumer_file = 'consumer.log'
publisher_file = 'publisher.log'
webserver_file = 'webserver.log'
default_file = 'default.log'

DEFAULT_COLOR = '\033[0m'
NOTIFY_COLOR = '\033[93m'
TIMER_COLOR = '\033[94m'


def log(message, file=default_file):
    file_name = os.path.join(os.getcwd(), 'logs', file)
    fopen = open(file_name, 'a')
    now = datetime.now()
    fopen.write("%s%s:%s %s\n" % (NOTIFY_COLOR, now, DEFAULT_COLOR, message))
    fopen.close()
