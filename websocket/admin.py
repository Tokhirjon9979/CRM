from django.contrib import admin

from websocket.models import Notifications


class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_seen')
    ordering = ('id',)
    readonly_fields = ('is_seen',)


admin.site.register(Notifications, NotificationsAdmin)
