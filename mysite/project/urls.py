from django.urls import path
from project.views.project_views import project_list, project_create,project_detail
from project.views.project_setting_views import project_setting_modify
from project.views.project_url_viws import project_url_list_viws

app_name = 'project'

urlpatterns = [
    path('', project_list, name='project_index'),
    path('create/', project_create, name='project_create'),
    path('<int:project_id>/', project_detail, name='project_detail'),
    path('project_setting/<int:project_setting_id>/', project_setting_modify, name='project_setting_modify'),
    path('url_list/<int:project_id>',project_url_list_viws,name='project_url_list')


]
