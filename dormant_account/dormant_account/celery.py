from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormant_account.settings')

app = Celery('dormant_accout')

# v4.0 이상 일 경우
# app.config_from_object('django.conf:settings', namespace='CELERY')
# v3.1 일 경우
app.config_from_object('django.conf:settings', namespace='CELERY')

# v4.0 이상 일 경우
# app.autodiscover_tasks()
# v3.1 일 경우
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.update(
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYBEAT_SCHEDULE = {
        'say_hello-every-seconds': {
            "task": "App.tasks.CheckSite",
            'schedule': timedelta(seconds=30),
            'args': ()
        },
    }
)