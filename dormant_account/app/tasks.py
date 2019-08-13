from __future__ import absolute_import

from dormant_account.celery import app


@app.task
def say_hello():     # 실제 백그라운드에서 작업할 내용을 task로 정의한다.
    print("Hello, celery!")