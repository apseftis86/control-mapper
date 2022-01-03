from .settings import *
import os

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

STATIC_ROOT = '/app/static/'
MEDIA_ROOT = '/app/media/'

# CELERY_BROKER_URL = os.getenv('BROKER_URL')
# CELERY_DB_URL = os.getenv('DB_URL')
print('Im prod', CELERY_BROKER_URL)
