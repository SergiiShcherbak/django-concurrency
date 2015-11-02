import os
import sys
from tempfile import mktemp
import django

DEBUG = True
STATIC_URL = '/static/'

SITE_ID = 1
ROOT_URLCONF = 'demo.urls'
SECRET_KEY = 'abc'
STATIC_ROOT = mktemp('static')
MEDIA_ROOT = mktemp('media')

INSTALLED_APPS = ['django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.admin',
                  'concurrency',
                  # 'reversion',
                  'demo']

if django.VERSION[:2] != (1,9):
    INSTALLED_APPS += ['reversion']

# # current reversion does not work with django 1.9
# # so we install it only on when django < 1.9
# # this can be removed when next version will be released
# if sys.version_info[:2] >= (3, 3):
#     if sys.version_info[:2] >= (3, 4):
#         from importlib.util import find_spec as importlib_find
#     else:
#         from importlib import find_loader as importlib_find
#
#     try:
#         importlib_find('reversion')
#         # INSTALLED_APPS += ['reversion']
#     except ImportError as e:
#         print(111, 1111111, e)
#         INSTALLED_APPS.remove('reversion')
#
# else:
#     import imp
#     try:
#         imp.find_module('reversion')
#         # INSTALLED_APPS += ['reversion']
#     except ImportError:
#         INSTALLED_APPS.remove('reversion')

MIGRATION_MODULES = {
    'demo': 'demo.migrations',
    'auth': 'demo.auth_migrations',
}

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if django.VERSION[1] >= 7:
    MIDDLEWARE_CLASSES += ['django.contrib.auth.middleware.SessionAuthenticationMiddleware', ]

TEMPLATE_DIRS = ['demo/templates']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'full': {
            'format': '%(levelname)-8s: %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'verbose': {
            'format': '%(levelname)-8s: %(asctime)s %(name)-25s %(message)s'
        },
        'simple': {
            'format': '%(levelname)-8s %(asctime)s %(name)-25s %(funcName)s %(message)s'
        },
        'debug': {
            'format': '%(levelno)s:%(levelname)-8s %(name)s %(funcName)s:%(lineno)s:: %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'debug'
        }
    },
    'loggers': {
        'concurrency': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG'
        }
    }
}

db = os.environ.get('DBENGINE', 'pg')
dbname = os.environ.get('DBNAME', 'concurrency')
if db == 'pg':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': dbname,
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'postgres',
            'PASSWORD': ''}}
elif db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': dbname,
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'root',
            'PASSWORD': '',
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci'}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3'}}