from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('announcements/<int:pk>/online-chat/', consumers.ChatConsumer),
]
