from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile


class dormantNotice_day_filter(admin.SimpleListFilter):
    title = '휴면알림 60일 전'
    parameter_name = 'day_filter'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return  queryset.filter(profile__dormantNotice_day_filter= True)

        elif value == 'No':
            return queryset.filter(profile__dormantNotice_day_filter=False)

        return queryset.all()

class check_alert(admin.SimpleListFilter):
    title = '휴면알림 유무'
    parameter_name = 'd'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return  queryset.filter(profile__check_alert= True)

        elif value == 'No':
            return queryset.filter(profile__check_alert=False)

        return queryset.all()