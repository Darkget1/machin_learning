from django.urls import path
from .views import project_list, project_create,project_detail

app_name = 'project'

urlpatterns = [
    path('', project_list, name='project_index'),
    path('create/', project_create, name='project_create'),
    path('<int:posting_id>/', project_detail, name='project_detail'),

]
