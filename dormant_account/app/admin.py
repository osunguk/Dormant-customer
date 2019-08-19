from django.contrib import admin
from .models import Content, Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

    list_display = ['username','id','date_joined','dormant_date']

    def dormant_date(self,obj):
        return Profile.objects.get(user=obj).dormant_cnt


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Content)
admin.site.register(Profile)

