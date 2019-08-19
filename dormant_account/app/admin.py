from django.contrib import admin
from .models import Content, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import messages
admin.site.site_header = 'ZEROWEB'
admin.site.site_title = 'Welcome '
admin.site.index_title = 'ZEROGO Management'
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'last_login', 'check_alter')
    actions = ['grant_is_staff', 'revoke_is_staff']

    list_filter = ['groups', 'last_login',]
    filter_horizontal = ()
    #search_fields = ('username','email','dormant_cnt','last_login',)

    def check_alter(self,obj):

        return Profile.objects.get(user=obj).check_alert

    check_alter.boolean = True
    check_alter.short_description ='휴면알림 유무'
    def grant_is_staff(self, request, queryset):

        for z in queryset:

            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id= x).update(check_alert=True)
        #queryset.update(check_alter = True)
        self.message_user(request, " changed successfully ." )
    grant_is_staff.short_description = '휴면알림 완료'

    def revoke_is_staff(self, request, queryset):
        for z in queryset:
            x = User.objects.get(username=z).id
            Profile.objects.filter(user_id=x).update(check_alert=False)
        # queryset.update(check_alter = True)
        self.message_user(request, " changed successfully .")
    revoke_is_staff.short_description = '휴면알림 미완료'

'''
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_editable = ('permission',)
    list_filter = ('permission',)
    search_fields = ('username',)



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


