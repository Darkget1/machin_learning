from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from project.models import Project,Project_url
from django.utils import timezone
from project.forms import ProjectForm
#필터 적용
from django.template.defaulttags import register

# def project_url_list_viws(request, project_id):
#     project = get_object_or_404(Project, pk=project_id)
#     project_url = Project_url.

