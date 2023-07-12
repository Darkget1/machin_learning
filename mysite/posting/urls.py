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

    # # article_views.py
    # path('posting/create/', article_views.posting_create, name='posting_create'),
    # path('posting/modify/<int:posting_id>/', article_views.posting_modify, name='posting_modify'),
    # path('posting/delete/<int:posting_id>/', article_views.posting_delete, name='posting_delete'),

# articleComment_views.py
    path('comment/create/posting/<int:posting_id>/', comment_views.comment_create_posting, name='comment_create_posting'),
    path('comment/modify/posting/<int:comment_id>/', comment_views.comment_modify_posting, name='comment_modify_posting'),
    path('comment/delete/posting/<int:comment_id>/', comment_views.comment_delete_posting, name='comment_delete_posting'),
    # path('comment/create/article/<int:article_id>/', comment_views.comment_create_article, name='comment_create_article'),
    # path('comment/modify/article/<int:comment_id>/', comment_views.comment_modify_article, name='comment_modify_article'),
    # path('comment/delete/article/<int:comment_id>/', comment_views.comment_delete_article, name='comment_delete_article'),

    # vote_views.py
    path('vote/posting/<int:posting_id>/', vote_views.vote_posting, name='vote_posting'),
    # path('vote/article/<int:article_id>/', vote_views.vote_article, name='vote_article'),
]
