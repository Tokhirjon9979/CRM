from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'owner')
    search_fields = ['name', 'owner']
    list_display_links = ['name']


admin.site.register(Company, CompanyAdmin)
# Register your models here.
