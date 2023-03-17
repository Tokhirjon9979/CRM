from django.contrib import admin
from .models import Company, Product


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'owner')
    ordering = ('id',)
    search_fields = ['name', 'owner']
    list_display_links = ['name']
    filter_horizontal = ('employees',)
    autocomplete_fields = ('owner',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company_id', 'price', 'description')
    ordering = ('id',)
    search_fields = ['name', 'company_id']
    list_display_links = ['name']
    list_filter = ['name', 'price']
    readonly_fields = ('created_at', )


admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)
