from django.urls import re_path

from .consumers import *

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<group_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path("ws/notifications/", NotificationConsumer.as_asgi())
]