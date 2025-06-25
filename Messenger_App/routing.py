from django.urls import path 
from .consumers import ChatConsumer

ws_urlpatterns = [
    path('ws/chat/<int:group_pk>/', ChatConsumer.as_asgi()),
]