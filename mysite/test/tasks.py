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
#
# #ceat_coupnag
# from ..src.ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify import ceat_coupang
#
# from ..src.ceat_crawling.ceat_data_collector.ceat_data_collector_scpecify.ceat_comparison_list import comparison_list
#
#


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
def naver(room_name):
    print('크롤링 시작')
    url = "https://kin.naver.com/qna/list.naver"
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    options.add_argument("headless")
    driver = webdriver.Chrome()
    driver.get(url)
    data_list = driver.find_elements(By.CLASS_NAME, 'title')
    for data in data_list:
        content = data.find_element(By.TAG_NAME, 'a').text
        form_naver = Crawling(content=content,create_time=timezone.now())
        form_naver.save()
        time.sleep(1)

        async_to_sync(get_channel_layer().group_send)(
            #그룹네임은 나중에 새로 설정할 필요성이 있다.
            room_name,{
                'type': 'chat_message',
                'command' : 'message',
                'message': content
            }
        )
# @shared_task
# def coupang(room_name):
#     brand_list = []
#     #수집 데이터 리스트
#     def ceat_collector_data_init():
#         print("========================================")
#         init_data = dict()
#         print("Target Mall Name (Coupang or Naver) : ")
#         init_data["target_mall"] = 'Naver'
#         print("Search Key : ")
#         init_data["search_key"] = '마스크'
#         print('Start Date (YYYY.MM.DD) : ')
#         init_data["start_t"] = '2023.07.01'
#         print("End Date (YYYY.MM.DD) : ")
#         init_data["end_t"] = '2023.07.31'
#         print("========================================")
#         return init_data
#     collector_data_info = ceat_collector_data_init()
#
#     comparison_name_list = comparison_list(collector_data_info, comparison_list_cnt_max=10).scenario_run()
#     ceat_coupang.coupang_scenario.coupang_get_link_to_DB(comparison_name_list)
# coupang(1)