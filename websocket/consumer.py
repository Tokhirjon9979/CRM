import asyncio
import json
from channels.consumer import AsyncConsumer
from random import randint
from time import sleep

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from websocket.models import Notifications


class PracticeConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        if self.scope["user"] is not AnonymousUser:
            self.user_id = self.scope["user"].id
            await self.channel_layer.group_add(f"{self.user_id}-message", self.channel_name)
            await self.send_all_unread_notifications()

    async def send_last_message(self, event):
        last_msg = await self.get_last_message(self.user_id)
        await self.send(text_data=json.dumps(last_msg))

    @database_sync_to_async
    def get_last_message(self, user_id):
        notification = Notifications.objects.filter(is_seen=False, company__owner__id=user_id).last()
        data = {}
        s = 'last_change'
        data[s] = {
            'title': notification.title,
            'description': notification.description,
            'company': notification.company_id,
            'is_seen': notification.is_seen,
            'created_at': str(notification.created_at),
        }
        return data

    async def send_all_unread_notifications(self):
        notifications = await self.get_all_unread_notifications(self.user_id)
        await self.send(text_data=json.dumps(notifications))

    @database_sync_to_async
    def get_all_unread_notifications(self, user_id):
        notifications = Notifications.objects.filter(is_seen=False, company__owner__id=user_id)
        data = {}
        k = 1
        for i in notifications:
            data[k] = {'title': i.title,
                       'description': i.description,
                       'company': i.company_id,
                       'is_seen': i.is_seen,
                       'created_at': str(i.created_at),
                       }
            k += 1

        return data

    async def websocket_receive(self, event):
        # when messages is received from websocket
        print("receive", event)

    async def websocket_disconnect(self, event):
        # when websocket disconnects
        print("disconnected", event)
