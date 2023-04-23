"""
https://raw.githubusercontent.com/benoitc/gunicorn/master/examples/example_config.py
"""

bind = "127.0.0.1:8080"
backlog = 2048

workers = 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

loglevel = "info"
errorlog = "-"
accesslog = "-"
access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'"

# spew = False
# 
# daemon = False
# raw_env = [
#     "DJANGO_SECRET_KEY=something",
#     "SPAM=eggs",
# ]
# pidfile = None
# umask = 0
# user = None
# group = None
# tmp_upload_dir = None
# 
# proc_name = None
