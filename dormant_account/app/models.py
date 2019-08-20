from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, PermissionsMixin

from django.db.models.signals import post_save  # 장고의 signals로 특정 이벤트가 발생했을 때 신호를 통한 여러 작업들을 도와주는 모듈
from django.dispatch import receiver  # 위와 동문
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


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
    BUSINESS = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer')
    )
    # 기본 정보
    email = models.CharField('이메일', max_length=100, blank=True)
    phoneNumber = models.CharField('핸드폰 번호', max_length=11, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 기존 User 모델에 1:1 대응을 생성
    check = models.CharField('check', max_length=100, blank=True)
    dormant_cnt = models.IntegerField('dormant_cnt', default=0)
    memo = models.TextField('memo', max_length=300, blank=True)
    check_alert = models.BooleanField('check_alter', default=False, blank=True)
    role_profile = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class UserC(models.Model):
    user_c = models.ForeignKey(User, on_delete=models.CASCADE)
    kakao_Id = models.CharField('카카오톡 아이디', max_length=100)
    mining_point = models.IntegerField('보유 포인트', default=0)


class UserB(models.Model):
    user_b = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField('사업장 이름', max_length=100)
    business_number = models.IntegerField('사업자 번호',)
    star_point = models.IntegerField('보유 포인트', default=0)


class DormantUserInfo(models.Model):
    username = models.CharField('username', max_length=100, blank=True)
    BUSINESS = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer')
    )
    role_dormant = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    lastLogin = models.DateTimeField(blank=True)
    dormantDate = models.DateTimeField(default=timezone.now)
    deleteDate = models.DateTimeField(blank=True)
    checkNotice = models.BooleanField(default=False)


# @receiver 는 말그대로 수신기로 신호(signal)가 전송되면 실행되는 코드
# @receiver 의 파라미터는 (어떤 신호인지, 시그널을 보낸 곳이 어디인지(송신자가 누구인지))
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()