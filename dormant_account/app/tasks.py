from __future__ import absolute_import
from dormant_account.celery import app
from celery import shared_task
"""
@app.task
def say_hello():
    print("hellow world!")
"""
@shared_task
def add(x, y):
    return x + y