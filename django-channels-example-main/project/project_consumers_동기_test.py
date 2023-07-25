# chat/consumers.py
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

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
        data_type = list(text_data_json.keys())[0]
        if data_type=='message_up':
            message = text_data_json['message_up']
            print('메세지 보냄')
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_up': message
                }
            )
        elif data_type=='naver':
            message = text_data_json['naver']
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_naver',
                    'naver': '진행'
                }
            )


    # Receive message from room group
    def chat_message(self, event):
        message = event['message_up']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message_up': message
        }))

    def chat_naver(self,event):
        message = event['naver']
        print(message)
        result = []
        url = "https://kin.naver.com/qna/list.naver"
        #버전 이슈 !!
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()))
        driver.get(url)
        data_list = driver.find_elements(By.CLASS_NAME, 'title')
        for data in data_list:
            message = data.find_element(By.TAG_NAME, 'a').text
            self.send(text_data=json.dumps({
                'message_up': message
            }))
            time.sleep(1)

        driver.close()
        print(result)