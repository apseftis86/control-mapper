from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = Celery('controlmapper', broker=os.getenv('BROKER_URL'), database=os.getenv('DATABASE_URL'))

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
