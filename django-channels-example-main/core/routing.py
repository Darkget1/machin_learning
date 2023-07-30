from django.urls import re_path
from chat import consumers
from project import project_consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/project/room/(?P<room_name>\w+)/$', project_consumers.projectConsumer.as_asgi()),
]
