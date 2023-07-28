# Create your tasks here
from __future__ import absolute_import, unicode_literals

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from .models import operate_time,Crawling
from django.utils import timezone
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

#테스트
from django.core.signals import request_finished





@shared_task
def celery():
    print('celery_delay 작업 시작')
    click_command = "celery"
    click_time = timezone.now()
    done_time = timezone.now()
    time_gap = done_time - click_time
    form_new = operate_time(click_time=click_time, done_time=done_time, time_gap=time_gap, click_command=click_command)
    form_new.save()


@shared_task
def celery_delay():
    print('celery_delay 작업 시작')
    click_command = "celery_delay"
    click_time = timezone.now()
    time.sleep(10)
    done_time = timezone.now()
    time_gap = done_time - click_time
    form_new = operate_time(click_time=click_time, done_time=done_time, time_gap=time_gap, click_command=click_command)
    form_new.save()

@shared_task
def naver():
    print('크롤링 시작')
    url = "https://kin.naver.com/qna/list.naver"
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()))
    driver.get(url)
    data_list = driver.find_elements(By.CLASS_NAME, 'title')
    for data in data_list:
        content = data.find_element(By.TAG_NAME, 'a').text
        form_naver = Crawling(content=content,create_time=timezone.now())
        form_naver.save()
        time.sleep(1)

        async_to_sync(get_channel_layer().group_send)(
            #그룹네임은 나중에 새로 설정할 필요성이 있다.
            'chat_1',{
                'type': 'chat_message',
                'command' : 'message',
                'message': content
            }
        )
@shared_task
def add(x,y):
    return x+y