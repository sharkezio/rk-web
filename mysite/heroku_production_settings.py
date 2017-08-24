from settings import *

import os
# Parse database configuration from $DATABASE_URL
import dj_database_url

# DATABASES['default'] = dj_database_url.config()
# DATABASES = {'default': dj_database_url.config(
#     default='postgres://localhost')}
DATABASES = {'default': dj_database_url.config()}

# SECRET_KEY = os.environ['SECRET_KEY']  # for deploy
SECRET_KEY = os.environ.get('SECRET_KEY')  # for deploy

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = 'staticfiles'
# STATIC_URL = '/static/'

# STATICFILES_DIRS = os.path.join(BASE_DIR, 'static')


# -----mail service settings for production-----
# mail backend service for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
# EMAIL_HOST_USER = 'wmsback@gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  # for deploy
# EMAIL_HOST_PASSWORD = 'uvcirpodxateyhtp'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # for deploy

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'required_debug_false': {  # filter only debug is false
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # mail to administrator when msg is error and debug != false
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['required_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        # django.request would set server error to ERROR
        # 400, 404 level WARNING
        # mail_admins handler would deal with level > ERROR
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': 'True',
        },
    }
}

# ADMINS = (  # error 500
#     ('admin', 'wemism27@gmail.com'),
# )
ADMINS = os.environ.get('ADMINS')  # error 500 mail

# MANAGERS = (  # error 404
#     ('manager1', 'wemism27@gmail.com'),
# )
MANAGERS = os.environ.get('MANAGERS')  # error 404 mail
