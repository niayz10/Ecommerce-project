from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from . import models
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'phone_number',
                'user_type',
            )
        }),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    pass

admin.site.register(models.CustomUser, CustomUserAdmin)

