from django.shortcuts import render
from django.utils.safestring import mark_safe
from .models import operate_time
from django.utils import timezone
import time
import json

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
    return render(request,'project/room.html')


def app_core(request):
    operate_list = operate_time.objects.order_by('-id').all()
    if (request.GET.get('operate')):
        click_command = "operate"
        click_time = timezone.now()
        done_time = timezone.now()
        time_gap = done_time-click_time
        form_new = operate_time(click_time=click_time, done_time=done_time, time_gap=time_gap, click_command=click_command)
        form_new.save()

    if (request.GET.get('operate_delay')):
        click_time = timezone.now()
        time.sleep(100)
        done_time = timezone.now()
        time_gap = done_time-click_time
        click_command = "operate"
        form_new = operate_time(click_time=click_time, done_time=done_time, time_gap=time_gap, click_command=click_command)
        form_new.save()

    return render(request, 'project/django_celery_main.html', {'operate_list': operate_list})
