from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from project.models import Project
from django.utils import timezone
from project.forms import ProjectForm


# Create your views here.

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.create_date = timezone.now()
            project.save()
            return redirect('project:project_index')
    else:
        form = ProjectForm()
    context = {'form': form}
    return render(request, 'project/project_form.html', context)

def project_list(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    #정렬

    if so == 'recommend':
        project_list = Project.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        project_list = Project.objects.annotate(
            num_comment=Count('comment')).order_by('-num_comment', '-create_date')
    else:
        project_list = Project.objects.order_by('-create_date')

    if kw:
        project_list = project_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(comment__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(project_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'project_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'project/project_list.html', context)