# chat/consumers.py
import time

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import asyncio


class projectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)


        print('메세지 보냄')
        # Send message to room group
        if text_data_json['command']=='naver':
            print('네이버 크롤링 진행')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'naver',
                    'order': '명령 타입'
                }
            )
        else:
            message = text_data_json['message_up']
            await self.channel_layer.group_send(

                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_up': message,
                }
            )
        # elif data_type == 'naver':
        #     message = text_data_json['naver']
        #     print(message)
        #     if message == 'test':
        #         url = "https://kin.naver.com/qna/list.naver"
        #         # 버전 이슈 !!
        #         # 옵션 생성
        #         options = webdriver.ChromeOptions()
        #         # 창 숨기는 옵션 추가
        #         options.add_argument("headless")
        #
        #         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()),options=options)
        #         driver.get(url)
        #         data_list = driver.find_elements(By.CLASS_NAME, 'title')
        #         for data in data_list:
        #             message = data.find_element(By.TAG_NAME, 'a').text
        #             print(message)
        #             await asyncio.sleep(1)
        #             await self.channel_layer.group_send(
        #                 self.room_group_name,
        #                 {
        #                     'type': 'chat_message',
        #                     'message_up': message
        #                 }
        #             )
        #
        #         driver.close()



    # Receive message from room group
    async def chat_message(self, event):
        print('받는중!!!')
        message = event['message_up']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message_up': message
        }))

    # async def chat_naver(self, event):
    #     message = event['naver']
    #     print(message)
    #     if message=='진행':
    #         url = "https://kin.naver.com/qna/list.naver"
    #         # 버전 이슈 !!
    #         driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()))
    #         driver.get(url)
    #         data_list = driver.find_elements(By.CLASS_NAME, 'title')
    #         for data in data_list:
    #             message = data.find_element(By.TAG_NAME, 'a').text
    #             await self.send(text_data=json.dumps({
    #                 'message_up': message
    #             }))
    #             time.sleep(1)
    #
    #     driver.close()
    async def naver(self,event):
        print(event)
        print('테스트')
        url = "https://kin.naver.com/qna/list.naver"
        # 버전 이슈 , 멀티스레딩으로 두군대서 진행한다.. 문제 !!방에서 받는쪽 + 내꺼 ..
        # 옵션 생성
        options = webdriver.ChromeOptions()
        # 창 숨기는 옵션 추가
        options.add_argument("headless")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()))
        driver.get(url)
        data_list = driver.find_elements(By.CLASS_NAME, 'title')
        for data in data_list:
            message = data.find_element(By.TAG_NAME, 'a').text
            print(message)
            # await self.send(text_data=json.dumps({
            #     'message_up': message
            # }))
            await asyncio.sleep(1)



