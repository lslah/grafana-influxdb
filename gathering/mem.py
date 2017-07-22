#!/usr/bin/python

# A little script to send test data to an influxdb installation
# Attention, the non-core library 'requests' is used. You'll need to install it first:
# http://docs.python-requests.org/en/master/user/install/

import json
import math
import requests
import sys
import psutil
import subprocess
import os
from threading import Timer

IP = "influxdb"        # The IP of the machine hosting your influxdb instance
DB = "wadus"               # The database to write to, has to exist
USER = os.getenv('INFLUXDB_USER')
PASSWORD = os.getenv('INFLUXDB_PASS')
TIME = 0.1                  # Delay in seconds between two consecutive updates

def send(data):
    r = requests.post("http://%s:8086/write?db=%s" %(IP, DB), auth=(USER, PASSWORD), data=data)
    if r.status_code != 204:
        print("Failed to add point to influxdb (%d) - aborting." % r.status_code)
        sys.exit(1)

def schedule(time, cmd):
    def repeat():
        Timer(time, repeat).start()
        cmd()
    repeat()

def main():
    schedule(1.0, lambda: send('cpu_percent value=%s' % psutil.cpu_percent()))
    schedule(1.0, lambda: send('mem_available value=%s' % psutil.virtual_memory().available))
    schedule(1.0, lambda: send('google.ping_time value=%s' % ping_google()))

def ping_google():
    ping_result = subprocess.check_output(['ping', '-c', '1', 'google.com']).decode()
    return ping_result.split('\n')[4].split('/')[4]

if __name__ == '__main__':
    main()
