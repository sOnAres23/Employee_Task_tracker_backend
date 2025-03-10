from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CUser(UserAdmin):
    model = User
    list_display = ('email', 'phone_number', 'is_staff', 'is_active', 'tg_chat_id')
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone_number', 'avatar', 'tg_chat_id')}),

        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name',
                       'phone_number', 'avatar', 'is_staff', 'is_active', 'tg_chat_id')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CUser)
