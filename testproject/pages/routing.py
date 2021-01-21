from django.urls import path

from .consumers import ChatConsumer

app_name = 'chats'

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
]
