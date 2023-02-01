from django.contrib import admin
from .models import User
from django.contrib.admin import FieldListFilter


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone')
    search_fields = ['username', 'first_name']
    list_filter = ['type', 'first_name'] #email verified
    list_display_links = ['id', 'username']


admin.site.register(User, UserAdmin)
# admin.site.register(User, PersonAdmin)
