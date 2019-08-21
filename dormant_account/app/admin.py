from django.contrib import admin
from django.utils import timezone
from .models import Content, Profile, DormantUserInfo, UserB, UserC
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import datetime


admin.site.site_header = 'ZEROWEB'
admin.site.site_title = 'Welcome '
admin.site.index_title = 'ZEROGO User'


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'last_login', 'check_alter', 'type')
    actions = ['is_alert', 'is_unalert', 'add_memo']
    list_filter = ['groups', 'last_login',]
    # search_fields = ('username','email','dormant_cnt','last_login',)
    date_hierarchy = 'last_login'

    def check_alter(self, obj):
        return Profile.objects.get(user=obj).check_alert

    check_alter.boolean = True
    check_alter.short_description = '휴면알림 유무'

    def is_alert(self, request, queryset):
        count = 0
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(check_alert=True)
            count += 1
        # queryset.update(check_alter = True)
        self.message_user(request, " {} 명의 휴면알림을 완료로 변경하였습니다 .".format(count))

    is_alert.short_description = '휴면알림 완료'

    def type(self, obj):
        return Profile.objects.get(user=obj).role_profile

    def is_unalert(self, request, queryset):
        count = 0
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(check_alert=False)
            count += 1

        self.message_user(request, " {} 명의 휴면알림을 미완료로 변경하였습니다 .".format(count))
    is_unalert.short_description = '휴면알림 미완료'

    def add_memo(self, request, queryset):  # 코드 리펙토링 할 것!
        count = 0

        def dormant_Alert():
            user_list = User.objects.values()

            for users in user_list:

                last_login = users['last_login']

                if last_login is None:
                    last_login = users['date_joined']

                return (datetime.timedelta(days=335) + last_login ) # 계정 전환 남은기간 계산

        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(memo='사전알림 날짜 : ' + str(dormant_Alert()))
            count += 1
        self.message_user(request, " {} 명의 사전알림 날짜를 추가하였습니다.".format(count))
    add_memo.short_description = '사전알림 날짜 추가'


class UserCAdmin(admin.ModelAdmin):
    list_display = ['user_c', 'kakao_Id', 'mining_point']
class UserBAdmin(admin.ModelAdmin):
    list_display = ['user_b', 'company_name', 'business_number', 'star_point']
class DormantUserInfoAdmin(admin.ModelAdmin):
    list_display = ['username','lastLogin','dormantDate','deleteDate']

'''
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_editable = ('permission',)
    list_filter = ('permission',)
    search_fields = ('username',)


    list_display = ['username','id','date_joined','dormant_date']

    def dormant_date(self,obj):
        return Profile.objects.get(user=obj).dormant_cnt


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'check', 'dormant_cnt','check_alert')
    list_filter = ('user', 'check_alert')
    actions = ['Test','is_check', 'is_uncheck']
    #search_fields = ('dormant_cnt')

    def get_user(self, obj):
        return obj.description
    get_user.short_description = 'ID'

    def Test(self, request, queryset):
        queryset.update(dormant_cnt = 365)
        #self.message_user((request, 'changed successfully'))
    Test.short_description = '휴면계정 날짜 초기화'

    def is_check(self, request, queryset):
        queryset.update(check_alert = True)
        self.message_user(request, " changed successfully ." )
    is_check.short_description = '휴면알림 O'

    def is_uncheck(self, request, queryset):
        queryset.update(check_alert = False)
        self.message_user(request, " changed successfully ." )
    is_uncheck.short_description = '휴면알림 X'

    def check_alert(self, check_alert):
        return check_alert.description

    check_alert.short_description = "휴면알림 유무"

admin.site.register(Content)
admin.site.register(Profile,ProfileAdmin)
'''

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserC, UserCAdmin)
admin.site.register(UserB, UserBAdmin)
admin.site.register(DormantUserInfo,DormantUserInfoAdmin)
