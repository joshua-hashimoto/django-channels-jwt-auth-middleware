from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'username', 'date_joined',
                    'is_active', 'is_staff', 'is_superuser', )
    search_fields = ('email', 'username', )
    readonly_fields = ('id', 'date_joined', 'last_login', )

    fieldsets = (
        ('Main options', {
            'fields': ('id', 'profile_image', 'email', 'username', )
        }),
        ('Sub options', {
            'classes': ('collapse',),
            'fields': ('user_permissions', 'groups', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
