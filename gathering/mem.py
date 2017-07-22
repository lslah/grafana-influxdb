#!/usr/bin/python

# A little script to send test data to an influxdb installation
# Attention, the non-core library 'requests' is used. You'll need to install it first:
# http://docs.python-requests.org/en/master/user/install/

import requests
import sys
import psutil
import subprocess
import os
from threading import Timer

INFLUX_HOST = os.getenv('INFLUXDB_HOST')
INFLUX_DB = os.getenv('INFLUXDB_DB')
INFLUX_USER = os.getenv('INFLUXDB_USER')
INFLUX_PASS = os.getenv('INFLUXDB_PASS')

def send(data):
    r = requests.post("http://%s:8086/write?db=%s" %(INFLUX_HOST, INFLUX_DB), auth=(INFLUX_USER, INFLUX_PASS), data=data)
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
