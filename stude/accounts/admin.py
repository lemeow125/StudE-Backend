from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('student_id_number',
         'year_level', 'semester', 'avatar', 'is_banned')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
