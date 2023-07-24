from django.urls import re_path

from . import consumers
from project import project_consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/project/(?P<room_name>\w+)/$', project_consumers.projectConsumer.as_asgi()),
]

# websocket_urlpatterns = [
#     path('ws/chat/<str:room_name>', consumers.ChatConsumer.as_asgi()),
# ]
