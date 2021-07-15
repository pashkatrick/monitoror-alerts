import os
import re
import subprocess
import time

from decouple import config
from pynotifier import Notification

PATH = os.path.dirname(os.path.abspath(__file__))
APP = config('APP_NAME')
BIN = config('BIN_PATH')


def check_log(log_line):
    # todo: remove
    notify(log_line)
    match = re.search('status:(\d+)', log_line)
    if match:
        if match.group(1) != '200':
            notify(log_line)


def notify(string):
    msg = f'Can\'t response one of your instance: {string}'
    Notification(
        title='Monitoror Alert',
        description=msg,
        # icon_path='/absolute/path/to/image/icon.png',  # On Windows .ico is required, on Linux - .png
        duration=5,  # Duration in seconds
        urgency='normal'
    ).send()


def run_server():
    cmd = f'{BIN} --debug > {PATH}/{APP}.log'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)


def follow(file):
    file.seek(0, os.SEEK_END)

    while True:
        line = file.readline()
        check_log(line)
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == '__main__':
    run_server()
    time.sleep(2)
    log_file = open(f'{PATH}/{APP}.log', 'r')
    log_lines = follow(log_file)
    # iterate over the generator - not needed
    for line in log_lines:
        pass
