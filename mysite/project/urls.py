from django.urls import path
from .views import project_list,project_create
app_name = 'project'

urlpatterns = [
    path('', project_list, name='project_index'),
    path('create/',project_create,name='project_create')

]
