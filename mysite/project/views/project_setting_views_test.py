from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from project.models import Project,Project_setting
from django.utils import timezone
from project.forms import ProjectForm ,Project_settingForm
from django.contrib import messages
def project_setting_modify(request, project_setting_id):
    project_setting = get_object_or_404(Project_setting, pk=project_setting_id)
    if request.user != project_setting.project.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('project:project_detail', prject_id=project_setting.project.id)
    if request.method == "POST":
        form = Project_settingForm(request.POST, instance=project_setting)
        if form.is_valid():
            project_setting_form = form.save(commit=False)
            project_setting_form.modify_date = timezone.now()  # 수정일시 저장
            project_setting_form.save()
            return redirect('project:project_detail', project_id=project_setting.project.id)
    else:
        form = Project_settingForm(instance=Project_setting)
    context = {'form': form}
    return render(request, 'project/project_setting_form.html', context)