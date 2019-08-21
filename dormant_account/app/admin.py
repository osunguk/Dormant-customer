from django.contrib import admin

from .models import Content, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

admin.site.site_header = 'ZEROWEB'
admin.site.site_title = 'Welcome '
admin.site.index_title = 'ZEROGO User'


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'last_login', 'check_alter')
    actions = ['is_alert', 'is_unalert', 'add_memo']
    list_filter = ['groups', 'last_login', ]

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

    def is_unalert(self, request, queryset):
        count = 0
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(check_alert=False)
            count += 1
        # queryset.update(check_alter = True)
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

                return last_login + datetime.timedelta(days=335)

        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(memo='사전알림 날짜 : ' + str(dormant_Alert()))
            count += 1
        self.message_user(request, " {} 명의 사전알림 날짜를 추가하였습니다.".format(count))

    add_memo.short_description = '사전알림 날짜 추가'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)