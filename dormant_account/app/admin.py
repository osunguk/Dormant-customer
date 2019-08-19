from django.contrib import admin
from .models import Content, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import messages
admin.site.site_header = 'ZEROWEB'
admin.site.site_title = 'Welcome '
admin.site.index_title = 'ZEROGO User'
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'last_login', 'is_staff')
    actions = ['grant_is_staff', 'revoke_is_staff']
    inlines = (ProfileInline, )
    def grant_is_staff(self, request, queryset):
        queryset.update(is_staff = True)
        self.message_user(request, " changed successfully ." )
    grant_is_staff.short_description = '스태프권한 부여'

    def revoke_is_staff(self, request, queryset):
        queryset.update(is_staff = False)
        self.message_user(request, " changed successfully ." )
    revoke_is_staff.short_description = '스태프권한 제거'

class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_editable = ('permission',)
    list_filter = ('permission',)
    search_fields = ('username',)


"""
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    list_select_related = ('profile', )

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)
"""

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'check', 'dormant_cnt')
    list_filter = ('user', )
    actions = ['Test']
    #search_fields = ('dormant_cnt')

    def get_user(self, obj):
        return obj.description
    get_user.short_description = 'ID'

    def Test(self, request, queryset):
        queryset.update(dormant_cnt = 365)
        #self.message_user((request, 'changed successfully'))
    Test.short_description = '휴면계정 날짜 초기화'




admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Content)
admin.site.register(Profile,ProfileAdmin)

