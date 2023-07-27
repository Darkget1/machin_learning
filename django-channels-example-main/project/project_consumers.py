# chat/consumers.py
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Crawling
from .tasks import naver
import json


@receiver(post_save, sender=Crawling)
def naver_to_receive(sender, instance, created, **kwargs):
    if created:
        message = Crawling.objects.get(id=instance.id).content
        print(message)

        async_to_sync(get_channel_layer().group_send)(
            #그룹네임은 나중에 새로 설정할 필요성이 있다.
            'chat_1',{
                'type': 'chat_message',
                'command' : 'message',
                'message': message
            }
        )


class projectConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name


        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()






    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )



    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

