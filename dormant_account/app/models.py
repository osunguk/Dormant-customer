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

    date_joined = models.DateTimeField(default=timezone.localtime())
    last_edit = models.DateTimeField(default=timezone.localtime())

    def __str__(self):
        return self.title


class Profile(models.Model):
    objects = None
    BUSINESS = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer')
    )
    # 기본 정보
    role_profile = models.PositiveSmallIntegerField('사용자 유형', choices=ROLE_CHOICES, null=True, blank=True)
    email = models.EmailField('이메일', max_length=100, blank=True)
    phoneNumber = models.CharField('핸드폰 번호', max_length=11, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 기존 User 모델에 1:1 대응을 생성
    dormant_cnt = models.IntegerField('휴면전환 남은 일자', default=0)
    memo = models.TextField('Memo', max_length=1000, blank=True)
    check_alert = models.BooleanField('사전알림 여부', default=False, blank=True)
    dormantNotice_day_filter = models.BooleanField('휴면전환 60전', default=False, blank=True)
    check = models.CharField('비고란', max_length=100, blank=True)

    def __str__(self):
        return str(self.user.username)


class UserC(models.Model):
    class Meta:
        verbose_name_plural = "커스텀 사용자"
    user_c = models.ForeignKey(User, on_delete=models.CASCADE)
    kakao_Id = models.CharField('카카오톡 아이디', max_length=100)
    mining_point = models.IntegerField('보유 포인트', default=0)

    def __str__(self):
        return str(self.user_c.username)

class UserB(models.Model):
    class Meta:
        verbose_name_plural = "비즈니스 사용자"
    user_b = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField('사업장 이름', max_length=100)
    business_number = models.IntegerField('사업자 번호',)
    star_point = models.IntegerField('보유 별', default=0)

    def __str__(self):
        return str(self.user_b.username)

class DormantUserInfo(models.Model):  # 휴면계정 모델
    class Meta:
        verbose_name_plural = "휴면 계정"
    BUSINESS = 1
    CUSTOMER = 2
    ROLE_CHOICES = (
        (BUSINESS, 'Business'),
        (CUSTOMER, 'Customer')
    )
    # 공통 속성
    username = models.CharField('username', max_length=100, blank=True)
    role_dormant = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    lastLogin = models.DateTimeField(blank=True, default=timezone.localtime())
    email = models.EmailField('이메일', max_length=100, blank=True)
    phoneNumber = models.CharField('핸드폰 번호', max_length=11, blank=True, null=True)
    memo = models.TextField('memo', max_length=1000, blank=True)
    
    # 휴면계정 속성
    dormantDate = models.DateTimeField(default=timezone.localtime())
    deleteDate = models.DateTimeField(blank=True, default=timezone.localtime())
    checkNotice = models.BooleanField(default=False)
    
    # B 속성
    company_name = models.CharField('사업장 이름', max_length=100, blank=True, null=True)
    business_number = models.IntegerField('사업자 번호', blank=True, null=True)
    star_point = models.IntegerField('보유 별', blank=True, null=True)
    
    # C 속성
    kakao_Id = models.CharField('카카오톡 아이디', max_length=100, blank=True, null=True)
    mining_point = models.IntegerField('보유 포인트', blank=True, null=True)


# @receiver 는 말그대로 수신기로 신호(signal)가 전송되면 실행되는 코드
# @receiver 의 파라미터는 (어떤 신호인지, 시그널을 보낸 곳이 어디인지(송신자가 누구인지))
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
