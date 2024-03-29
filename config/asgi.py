"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from websocket.consumer import  PracticeConsumer
from websocket.middlewares import WebSocketJWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
aaa = get_asgi_application()
application = ProtocolTypeRouter({
    'http': aaa,
    'websocket': WebSocketJWTAuthMiddleware(
        URLRouter([
            path('ws', PracticeConsumer.as_asgi())
        ])
    )
})
