from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import signals
from django.dispatch import receiver
from requests import Response
from rest_framework import status

from websocket.models import Notifications
from .models import Product


# post_save method
@receiver(signals.post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    print(instance)
    #
    # async_to_sync(get_channel_layer().group_send)(
    #     'notifications', {"type": "product_changed"}
    # )

    async_to_sync(get_channel_layer().group_send)(
        f"{instance.company_id.owner.id}-message", {"type": "send_last_message"}
    )
    print(instance.company_id.owner)
