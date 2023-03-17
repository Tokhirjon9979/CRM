from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'email_verified', 'type')
    ordering = ('id',)
    search_fields = ['username', 'first_name']
    list_filter = ['type', 'email_verified']  # email verified
    list_display_links = ['id', 'username']
    exclude = ('password', 'groups', 'user_permissions')
    readonly_fields = (
        'id', 'email', 'email_verified', 'type', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
    list_per_page = 50


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
