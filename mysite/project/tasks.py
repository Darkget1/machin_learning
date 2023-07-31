# Create your tasks here
from __future__ import absolute_import, unicode_literals

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from test.models import operate_time, Crawling
from project.models import Project
from django.utils import timezone
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 테스트
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
def naver(group_name,room_name):
    print('크롤링 시작')
    print(group_name)
    #크롤링 시작시 스테이터스 1(진행중)
    project = Project.objects.get(pk=room_name)
    project.crawling_status = '1'
    project.save()


    url = "https://kin.naver.com/qna/list.naver"
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")
    driver = webdriver.Chrome()
    driver.get(url)
    data_list = driver.find_elements(By.CLASS_NAME, 'title')
    data_all_count = len(data_list) + 1
    for data, i in zip(data_list, range(1, data_all_count)):
        content = data.find_element(By.TAG_NAME, 'a').text
        form_naver = Crawling(content=content, create_time=timezone.now())
        form_naver.save()
        time.sleep(1)
        now_propress = int(i) / int(data_all_count - 1) * 100
        print(now_propress)
        async_to_sync(get_channel_layer().group_send)(
            group_name, {
                'type': 'chat_message',
                'command': 'message',
                'message': content,
                'cnt': now_propress,

            }
        )
    #종료시 0으로 변경
    project.crawling_status = '0'
    project.save()


@shared_task
def add(x, y):
    return x + y
