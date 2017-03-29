from __future__ import absolute_import
from celery import Celery
app = Celery('Tasks', include=['Tasks.tasks'])
app.config_from_object('Tasks.config')