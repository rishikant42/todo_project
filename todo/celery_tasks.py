from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')

PROJECT_NAME = settings.CELERY_PROJECT_NAME
BROKER_URL = settings.CELERY_BROKER_URL
RESULT_BACKEND = settings.CELERY_RESULT_BACKEND

app = Celery(PROJECT_NAME, broker=BROKER_URL, backend=RESULT_BACKEND)
app.autodiscover_tasks()

@app.task
def task_alert(task_id, task_title):
    return "A task with id '{}' having title '{}' is pending".format(task_id, task_title)
