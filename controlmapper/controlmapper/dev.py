from .settings import *
import os

DEBUG = True

CELERY_BROKER_URL = os.getenv('DEV_BROKER_URL')
print('Im dev')
CELERY_DB_URL = os.getenv('DEV_DB_URL')

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'access-control-allow-headers',
    'access-control-expose-headers',
    'content-type',
    'content-disposition',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_EXPOSE_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'access-control-allow-headers',
    'access-control-expose-headers',
    'content-type',
    'content-disposition',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DEV_DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

STATIC_ROOT = '/opt/control-mapper/controlmapper/static'
MEDIA_ROOT = '/opt/control-mapper/controlmapper/media'