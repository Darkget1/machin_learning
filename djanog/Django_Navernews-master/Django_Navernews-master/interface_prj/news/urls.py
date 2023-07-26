from django.urls import path


from news import views

app_name='news'
urlpatterns = [
    path('',views.news_list, name='news_list'),
    path('news/search/', views.news_search, name='news_search'),
    path('news/sports/', views.news_category_sports, name='news_category_sports'),   #추가
    path('news/sports/<str:sports>/', views.news_sports, name='news_sports'),
    path('news/<str:sid1>/', views.news_category_list, name='news_category_list'), #추가
    path('news/<str:sid1>/<str:sid2>/', views.news_detail, name='news_detail'),
]
