
# Gunicorn configuration
bind = '0.0.0.0:9000'
workers = 3
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
reload = True