# -*- coding: utf-8 -*-
"""
Local Configurations

- Runs in Debug mode
- Uses console backend for emails
- Use Django Debug Toolbar
"""
from .common import *

# DEBUG
DEBUG = True
TEMPLATE_DEBUG = DEBUG
# END DEBUG

# INSTALLED_APPS
# INSTALLED_APPS +=
# END INSTALLED_APPS

# Mail settings MAILDUMP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend') VIA CONSOLE
EMAIL_HOST, EMAIL_PORT = '127.0.0.1', 1025  # Work with maildump
DEFAULT_FROM_EMAIL = 'victor@jvacx.com'
# End mail settings

# django-debug-toolbar
# MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar',)

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}


# CORS Protection
CORS_ORIGIN_ALLOW_ALL = True

# Development DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.dirname(BASE_DIR)+'/development.db',
    }
}