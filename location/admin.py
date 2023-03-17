from django.contrib import admin

from location.models import Location, LocationImages


class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'company')
    search_fields = ['name', 'address']
    list_display_links = ['name', 'address']
    autocomplete_fields = ('employee',)
    ordering = ('id',)


class LocationImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'title', 'image')
    search_fields = ['title', 'location']
    list_display_links = ['location']
    ordering = ('id',)


admin.site.register(Location, LocationAdmin)
admin.site.register(LocationImages, LocationImagesAdmin)
