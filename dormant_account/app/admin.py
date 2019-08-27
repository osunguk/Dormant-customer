import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .models import (
    Profile, DormantUserInfo, UserB, UserC
)
from .filters import (
    TypeFilter, CheckAlert, AccountConversionAlertFilter
)


admin.site.site_header = 'ZEROWEB'
admin.site.site_title = 'Welcome '
admin.site.index_title = 'ZEROGO User'


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = '프로필'
    fk_name = 'user'


class UserCInline(admin.StackedInline):
    model = UserC
    can_delete = False
    verbose_name_plural = '세부정보'
    fk_name = 'user_c'
    extra = 0
    max_num = 1


class UserBInline(admin.StackedInline):
    model = UserB
    can_delete = False
    verbose_name_plural = '세부정보'
    fk_name = 'user_b'
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, UserBInline, UserCInline)
    list_display = ('username', 'type', '_email', 'phone_number', 'company_cnt', 'kakao_id',
                    'last_login', 'check_alert', 'conversion_check')
    actions = ['is_alert', 'is_unalert', 'add_memo']
    list_filter = [AccountConversionAlertFilter, TypeFilter, CheckAlert]
    date_hierarchy = 'last_login'
    search_fields = ['username', 'profile__email', 'profile__phone_number',
                     'userc__kakao_id', 'userb__company_name', 'userb__business_number', ]
    readonly_fields = ('dormant_cnt',)
    fieldsets = (
        (None, {'fields': ('username',)}),
        ('시간 정보', {'fields': ('last_login', 'date_joined', )}),
    )

    list_per_page = 10


    def dormant_cnt(self, obj):
        return Profile.objects.get(user=obj).dormant_cnt

    def conversion_check(self, obj):
        return Profile.objects.get(user=obj).conversion_check

    def _email(self, obj):
        return Profile.objects.get(user=obj).email

    def phone_number(self, obj):
        return Profile.objects.get(user=obj).phone_number

    def check_alert(self, obj):
        return Profile.objects.get(user=obj).check_alert

    def company_cnt(self, obj):
        return len(UserB.objects.filter(user_b=obj))

    def kakao_id(self, obj):
        return UserC.objects.get(user_c=obj).kakao_id

    def type(self, obj):
        return Profile.objects.get(user=obj).role_profile

    def is_alert(self, request, queryset):
        count = 0
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(check_alert=True)
            count += 1
        # queryset.update(check_alter = True)
        self.message_user(request, " {} 명의 휴면알림을 완료로 변경하였습니다 .".format(count))

    def is_unalert(self, request, queryset):
        count = 0
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(check_alert=False)
            count += 1
        self.message_user(request, " {} 명의 휴면알림을 미완료로 변경하였습니다 .".format(count))

    def add_memo(self, request, queryset):  # 코드 리펙토링 할 것!
        count = 0

        def _dormant_alert():
            user_list = User.objects.values()

            for users in user_list:
                last_login = users['last_login']
                if last_login is None:
                    last_login = users['date_joined']
                return datetime.timedelta(days=275) + last_login  # 계정 전환 남은기간 계산
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(
                memo=Profile.objects.get(user_id=x).memo+'\n 사전알림 날짜 : ' + str(_dormant_alert()))
            count += 1
        self.message_user(request, " {} 명의 사전알림 날짜를 추가하였습니다.".format(count))

    is_unalert.short_description = '휴면알림 미완료'
    is_alert.short_description = '휴면알림 완료'
    add_memo.short_description = '사전알림 날짜 추가'

    conversion_check.short_description = '휴면전환 60일 전'
    check_alert.boolean = True
    conversion_check.boolean = True

    type.short_description = '타입'
    _email.short_description = '메일주소'
    phone_number.short_description = '전화번호'
    check_alert.short_description = '알림 유무'
    company_cnt.short_description = '사업장 갯수'


class UserCAdmin(admin.ModelAdmin):
    list_display = ['user_c', 'kakao_id', 'mining_point']


class UserBAdmin(admin.ModelAdmin):
    list_display = ['user_b', 'company_name', 'business_number', 'star_point']


class DormantUserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_login', 'dormant_date', 'delete_date']


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(UserC, UserCAdmin)
admin.site.register(UserB, UserBAdmin)
admin.site.register(DormantUserInfo, DormantUserInfoAdmin)
