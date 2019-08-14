from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db.models.signals import post_save  # 장고의 signals로 특정 이벤트가 발생했을 때 신호를 통한 여러 작업들을 도와주는 모듈
from django.dispatch import receiver  # 위와 동문


class Content(models.Model):
    number = models.IntegerField('number', primary_key=True)
    title = models.CharField('title', max_length=100)
    contents = models.CharField(max_length=300)
    writer = models.CharField('writer', max_length=100)

    date_joined = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 기존 User 모델에 1:1 대응을 생성
    check = models.CharField('check', max_length=100, blank=True)
    dormant_cnt = models.IntegerField('dormant_cnt', default=0)

    def __str__(self):
        return str(self.dormant_cnt)


# @receiver 는 말그대로 수신기로 신호(signal)가 전송되면 실행되는 코드
# @receiver 의 파라미터는 (어떤 신호인지, 시그널을 보낸 곳이 어디인지(송신자가 누구인지))
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
