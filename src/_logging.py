import os
from datetime import datetime

# Declaring standard log file names
consumer_file = 'consumer.log'
publisher_file = 'publisher.log'
webserver_file = 'webserver.log'
default_file = 'default.log'

DEFAULT_COLOR = '\033[0m'
NOTIFY_COLOR = '\033[93m'
TYPE_COLOR = '\033[94m'


def log(message, type='', file=default_file):
    file_name = os.path.join(os.getcwd(), 'logs', file)
    fopen = open(file_name, 'a')
    now = datetime.now()
    fopen.write("[x] %s%s: %s%s:%s %s\n" % (TYPE_COLOR, type, NOTIFY_COLOR,
                                            now, DEFAULT_COLOR, message))
    fopen.close()


def create_log_dir():
    log_dir_name = 'logs'
    cwd = os.getcwd()
    log_dir_path = os.path.join(cwd, log_dir_name)
    if not os.path.isdir(log_dir_path):
        os.makedirs(log_dir_path)
