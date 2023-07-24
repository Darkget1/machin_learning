from django.urls import path
from . import views

app_name = 'project'
urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('naver/',views.naver_data,name='naver')
]
