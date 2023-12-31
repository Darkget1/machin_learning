from django.urls import path
from .views import base_views, posting_views, comment_views, vote_views

app_name = 'posting'

urlpatterns =[
    path('', base_views.main, name='index'),
    path('<int:posting_id>/', base_views.detail, name='detail'),

    # posting_views.py
    path('posting/create/', posting_views.posting_create, name='posting_create'),
    path('posting/modify/<int:posting_id>/', posting_views.posting_modify, name='posting_modify'),
    path('posting/delete/<int:posting_id>/', posting_views.posting_delete, name='posting_delete'),


    path('comment/create/posting/<int:posting_id>/', comment_views.comment_create_posting, name='comment_create_posting'),
    path('comment/modify/posting/<int:comment_id>/', comment_views.comment_modify_posting, name='comment_modify_posting'),
    path('comment/delete/posting/<int:comment_id>/', comment_views.comment_delete_posting, name='comment_delete_posting'),
    path('vote/posting/<int:posting_id>/', vote_views.vote_posting, name='vote_posting'),

]
