from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '프로젝트이름.settings')

from django.conf import settings

app = Celery('프로젝트이름',  # 첫번째 값은 현재 프로젝트의 이름을 설정하고
             broker='django://')  # broker: 브로커에 접속할 수 있는 URL을 설정.
# Django 데이터베이스 백엔드를 사용하려면 'django://'로 설정한다.

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(
    BROKER_URL='django://',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
)