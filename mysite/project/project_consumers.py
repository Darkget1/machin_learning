from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
# from .tasks import naver
import json
from project.tasks import naver


class projectConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'project_%s' % self.room_name


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

        # Send message to room group
        # task 전달
        print(text_data_json)
        if text_data_json['command']=='naver':
            print('naver')

            naver.delay(self.room_group_name,self.room_name)

        else:
            message = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )



    # Receive message from room group
    def chat_message(self, event):
        cnt = event['cnt']
        message = event['message']
        print(message)
        print(cnt)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'cnt': cnt,
        }))

