from .settings import *
from dotenv import load_dotenv, find_dotenv
import os

LOGGING_CONFIG = None

load_dotenv(find_dotenv())
SECRET_KEY = os.environ.get("SECRET_KEY")
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

STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'