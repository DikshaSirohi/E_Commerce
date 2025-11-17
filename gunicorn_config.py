import os

# Gunicorn configuration
bind = '0.0.0.0:8000'
workers = 3
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'ecommerce_store'

# Server mechanics
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Environment variables
raw_env = [
    'DJANGO_SETTINGS_MODULE=ecommerce_store.settings',
]
