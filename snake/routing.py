from django.urls import re_path

from . import snake_consumer

websocket_urlpatterns = [
    re_path(r'ws/snake/connect/$', snake_consumer.SnakeConsumer.as_asgi()),
]
