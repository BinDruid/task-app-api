import socket

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'django.local']
INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS += ['.'.join(ip.split('.')[:-1] + ['1']) for ip in ips]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': ['debug_toolbar.panels.redirects.RedirectsPanel'],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# Development Logging setting

LOGGING['handlers']['kafka'] = {
    'level': DJANGO_LOG_LEVEL,
    'class': 'config.loggers.KafkaHandler',
    'topic': 'django',
    'security_protocol': 'PLAINTEXT'
}

LOGGING['loggers']['django'] = {
    'handlers': ['console', 'kafka'],
    'level': DJANGO_LOG_LEVEL,
    'propagate': True,
}
