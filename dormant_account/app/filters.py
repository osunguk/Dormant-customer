from django.contrib import admin
from django.contrib.auth.models import User

from app.models import Profile


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
