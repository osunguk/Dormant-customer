from django.db import models
from django.utils import timezone

# Create your models here.

class Content(models.Model):
    number = models.IntegerField('number', primary_key=True)
    title = models.CharField('title', max_length=100)
    contents = models.CharField(max_length=300)
    writer = models.CharField('writer', max_length=100)

    date_joined = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
