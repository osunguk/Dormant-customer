from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dormant_count = models.DateField(null=True, blank=True)
    nickname = models.CharField('nickname', max_length=100, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()