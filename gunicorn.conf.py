import os

bind = '127.0.0.1:8000'
workers = 8
backlog = 2048
worker_class = "gevent"
debug = True
proc_name = 'gunicorn.gd'
pidfile = '/tmp/gunicorn.pid'
logfile = '/tmp/gunicorn.log'
loglevel = 'debug'
