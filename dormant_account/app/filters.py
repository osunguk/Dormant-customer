from django.contrib import admin


class AccountConversionAlertFilter(admin.SimpleListFilter):
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
            return queryset.filter(profile__conversion_check=True)
        elif value == 'No':
            return queryset.filter(profile__conversion_check=False)
        return queryset.all()


class TypeFilter(admin.SimpleListFilter):
    title = '고객 type'
    parameter_name = 'type_filter'

    def lookups(self, request, model_admin):
        return(
            (1, '1 : 비즈니스'),
            (2, '2 : 커스터멀'),
            (3, '3')
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '1':
            return queryset.filter(profile__role_profile=1)
        elif value == '2':
            return queryset.filter(profile__role_profile=2)
        elif value == '3':
            return queryset.filter(profile__role_profile=None)
        return queryset.all()


class CheckAlert(admin.SimpleListFilter):
    title = '휴면알림 유무'
    parameter_name = 'check_alert'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(profile__check_alert=True)
        elif value == 'No':
            return queryset.filter(profile__check_alert=False)
        return queryset.all()
