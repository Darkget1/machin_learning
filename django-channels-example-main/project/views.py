from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
# Create your views here.
def index(request):
    return render(request,'project/index.html',{})

def room(request, room_name):
    # result = []
    # url = "https://kin.naver.com/qna/list.naver"
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='114.0.5735.90').install()))
    # driver.get(url)
    # data_list = driver.find_elements(By.CLASS_NAME, 'title')
    # for data in data_list:
    #     result.append(data.find_element(By.TAG_NAME, 'a').text)
    # driver.close()
    # print(result)
    return render(request, 'project/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def naver_data(request):
    result = []
    url = "https://kin.naver.com/qna/list.naver"
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    data_list = driver.find_elements(By.CLASS_NAME, 'title')
    for data in data_list:
        result.append(data.find_element(By.TAG_NAME, 'a').text)
    driver.close()
    print(result)
    return render(request,'project/room.html',{'result':result})

