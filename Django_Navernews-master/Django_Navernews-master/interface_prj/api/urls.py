from django.urls import path, include
from api.views import LetterViewSet

app_name = 'api'

news_list = LetterViewSet.as_view({'get':'_list'})
news_detail = LetterViewSet.as_view({'get':'retrieve'})

urlpatterns = [
    path('',include('rest_framework.urls', namespace='rest_framework')),
    path('news/',news_list,name='news_list'),
    path('news/<str:sid1>',news_detail, name='news_detail')
]
