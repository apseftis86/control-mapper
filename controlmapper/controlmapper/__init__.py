# If this file is not present, Celery is unable to communicate with the Django application
from .celery import app as celery_app

__all__ = ("celery_app",)
