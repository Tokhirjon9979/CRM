from rest_framework import serializers

from websocket.models import Notifications


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ['id', 'title', 'description', 'company_id', 'is_seen', 'created_at']
