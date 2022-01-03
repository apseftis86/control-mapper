from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

app = Celery('controlmapper', broker=os.getenv('CELERY_BROKER_URL'), database=os.getenv('CELERY_DB_URL'))
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
